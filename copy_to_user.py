import configparser

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

    playlist.create(admin_server, playlist.title, playlist.items())

    # playlist.copyToUser(config.get('DEFAULT', 'to user'))


if __name__ == '__main__':
    main()
