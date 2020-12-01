import configparser
import math
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


def main():
    config = load_config()

    account = MyPlexAccount(config.get('DEFAULT', 'username'),
                            config.get('DEFAULT', 'password'))

    admin_server = account.resource(config.get('DEFAULT',
                                               'server name')).connect()

    user = account.user(config.get('DEFAULT', 'user'))

    # Get the token for the machine.
    token = user.get_token(admin_server.machineIdentifier)

    # Get the user server. We access the base URL by requesting a URL for a
    # blank key.
    user_server = PlexServer(admin_server.url(''), token=token)

    playlist = user_server.playlist(config.get('DEFAULT', 'playlist name'))
    items = playlist.items()

    with open('{}.m3u8'.format(config.get('DEFAULT', 'playlist name')),
              'w', encoding="utf-8") as f:
        f.write('#EXTM3U\n')

        for track in items:
            f.write('#EXTINF:{},{} - {}\n{}\n'
                    .format(math.floor(track.duration / 1e3),
                            re.sub(r'\s*-\s*', ' ', track.grandparentTitle),
                            re.sub(r'\s*-\s*', ' ', track.title),
                            track.media[0].parts[0].file))


if __name__ == '__main__':
    main()
