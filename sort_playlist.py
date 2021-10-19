import configparser
import re

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer


def load_config(configuration_file_path='config.ini'):
    configuration = configparser.ConfigParser()

    # Set default values
    configuration['DEFAULT'] = \
        {'username': '', 'password': '', 'server': '', 'playlist': '',
         'user': ''}

    configuration.read(configuration_file_path)

    return configuration


def get_various_artists_album_sort_key(album):
    album_artists = set()

    for track in album.tracks():
        if track.originalTitle is not None:
            sanitized = track.originalTitle.lower()
        else:
            sanitized = track.titleSort.lower()

        sanitized = re.sub(r'/', ', ', sanitized)
        sanitized = re.sub(r'feat', ', ', sanitized)
        sanitized = re.sub(r'\.', '', sanitized)

        artist_list = re.split(r'[&,]', sanitized)

        for artist in artist_list:
            album_artists.add(artist.strip())

    key = ''.join(sorted(list(album_artists)))

    return key


def get_track_sort_key_length(track):
    return track.duration


def get_track_sort_key(track, album):
    key = ''
    number_of_tracks = max(len(album.tracks()), 1)
    number_of_discs = 1

    for t in album.tracks():
        if t.parentIndex is not None:
            number_of_discs = max(int(t.parentIndex), number_of_discs)

    if track.grandparentTitle.startswith('Various'):
        key += get_various_artists_album_sort_key(album)
    else:
        key += track.grandparentTitle.lower()

    if album.year is not None:
        key += str(album.year)

    key += album.titleSort.lower()

    if track.parentIndex is not None:
        key += '{:0{width}.0f}'.format(int(track.parentIndex),
                                       width=len(str(number_of_discs)))

    if track.index is not None:
        key += '{:0{width}.0f}'.format(int(track.index),
                                       width=len(str(number_of_tracks)))

    key += track.titleSort.lower()

    return key


def main():
    config = load_config()

    account = MyPlexAccount(config.get('DEFAULT', 'username'),
                            config.get('DEFAULT', 'password'))

    admin_server = account.resource(config.get('DEFAULT',
                                               'server name')).connect()

    if config.get('DEFAULT', 'user') == account.username:
        user_server = admin_server
    else:
        user = account.user(config.get('DEFAULT', 'user'))

        # Get the token for the machine.
        token = user.get_token(admin_server.machineIdentifier)

        # Get the user server. We access the base URL by requesting a URL for a
        # blank key.
        user_server = PlexServer(admin_server.url(''), token=token)

    albums = {a.key: a for a in user_server.library.section('Music').albums()}
    playlist = user_server.playlist(config.get('DEFAULT', 'playlist name'))
    items = playlist.items()

    sort_structure = []

    for track in items:
        album = albums[track.parentKey]

        key = get_track_sort_key(track, album)
        # key = get_track_sort_key_length(track)

        sort_structure.append((key, track))

    sort_structure.sort(key=lambda item: item[0])

    items = [item[1] for item in sort_structure]

    for item in items:
        playlist.removeItem(item)

    playlist.addItems(items)


if __name__ == '__main__':
    main()
