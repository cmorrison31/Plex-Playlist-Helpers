import configparser

from plexapi.myplex import MyPlexAccount


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

    plex = account.resource(config.get('DEFAULT', 'server name')).connect()

    playlist = plex.playlist(config.get('DEFAULT', 'playlist name'))

    playlist.copyToUser(config.get('DEFAULT', 'user'))


if __name__ == '__main__':
    main()
