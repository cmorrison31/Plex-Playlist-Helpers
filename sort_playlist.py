import configparser
import re

from plexapi.myplex import MyPlexAccount


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
        sanitized = track.originalTitle.lower()
        sanitized = re.sub(r'/', ', ', sanitized)
        sanitized = re.sub(r'feat', ', ', sanitized)
        sanitized = re.sub(r'\.', '', sanitized)

        artist_list = re.split(r'[&,]', sanitized)

        for artist in artist_list:
            album_artists.add(artist.strip())

    key = ''.join(sorted(list(album_artists)))

    return key


def get_track_sort_key(track, album):
    key = ''
    number_of_tracks = max(len(album.tracks()), 1)

    if track.grandparentTitle.startswith('Various'):
        key += get_various_artists_album_sort_key(album)
    else:
        key += track.grandparentTitle.lower()

    if album.year is not None:
        key += str(album.year)

    key += album.titleSort.lower()

    if track.index is not None:
        key += '{:0{width}.0f}'.format(int(track.index),
                                       width=len(str(number_of_tracks)))

    key += track.titleSort.lower()

    return key


def main():
    config = load_config()

    account = MyPlexAccount(config.get('DEFAULT', 'username'),
                            config.get('DEFAULT', 'password'))

    plex = account.resource(config.get('DEFAULT', 'server name')).connect()

    albums = {a.key: a for a in plex.library.section('Music').albums()}
    playlist = plex.playlist(config.get('DEFAULT', 'playlist name'))
    items = playlist.items()

    sort_structure = []

    for track in items:
        album = albums[track.parentKey]

        key = get_track_sort_key(track, album)

        sort_structure.append((key, track))

    sort_structure.sort(key=lambda item: item[0])

    items = [item[1] for item in sort_structure]

    for item in items:
        playlist.removeItem(item)

    playlist.addItems(items)


if __name__ == '__main__':
    main()
