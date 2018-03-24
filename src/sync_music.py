#!/usr/bin/env python3
import click
import subprocess
import os
import json
import dropbox
import requests


def gen_index(dirs):
    """generates index.tmp

    This function calls bash script "generate_index.sh" to generate file
    "index.tmp" to store address of all mp3 files from directories that are
    passed as argument.

    arg1 dirs: tuple of directories.

    Return False: if directory given is null string.
    Return False: when bash script couldn't find the required directory.
    Return 0: if Index is not updated and added.tmp is successfully generated.
    Return 3: if Index is already updated and no added.tmp is generated.
    """

    if dirs == ('',):
        print("\nNull directory!")
        return False

    # calling bash scirpt with given directories as arguments.
    script_path = os.path.expanduser('~/.sync-music/scripts/generate_index.sh')
    call_script = list(dirs)
    call_script.insert(0, script_path)

    # res = 0 if added.tmp is found, and res = 3 if Index is already updated.
    res = subprocess.call(call_script)
    if res not in (0, 3):
        return False
    else:
        return res


def update_config(config,
                  config_file='~/.sync-music/config/keys.json'):
    """update user configuration

    This function writes configuration in keys.json, for the field whose "key"
    and "value" is given by user as arguments.

    arg1 config: tuple consist of ("field of configuration", "value").
    arg2 config_file: path to configuration file (keys.json). Default path is
    setup by executing "setup.sh"

    Return Flase: if "field of configuration" is invalid.
    Return True: if keys.json is found and configurations are updated.
    """

    if config[0] != 'dropbox.key':
        print("\nCouldn't recognize \"%s\" option. See: sync-music --help" %
              config[0])
        return False

    else:
        config_file = os.path.expanduser(config_file)
        try:
            if not os.path.isfile(config_file):
                raise AttributeError
            with open(config_file, mode='w') as f:
                json.dump(dict({config}), f)
        except AttributeError:
            print("\nkeys.json is unavailable.")
            return False
        return True


def get_config(config_file='~/.sync-music/config/keys.json'):
    """get user configurations from keys.json

    This function brings the configration from keys.json. And if
    configurations are not present, then it also give a user friendly message
    to first update their configurations and then try again.

    arg1 config_file: path to configuration file. Default path is setup by
                      executing "setup.sh".

    Return False: If either keys.json is empty or not found.
    Return API token: If configurations are successfully read from the file.
    """

    config_file = os.path.expanduser(config_file)
    try:
        if os.path.isfile(config_file) is False:
            raise AttributeError
        with open(config_file, mode='r') as f:
            keys = json.loads(f.read())
            if os.stat(config_file).st_size != 0 and keys['dropbox.key'] != '':
                return keys['dropbox.key']
            else:
                print("\nPlease config sync-music with dropbox API_token.\n"
                      "See: sync-music --help")
                return False
    except AttributeError:
        print("\nkeys.json is unavailable.")
        return False


def upload_dbx():
    """upload music files

    This function uploads songs, whose path is available in the file
    "added.tmp".

    Returns True: if songs get uploaded successfully.
    Returns False: if uploading encounters any Connectivity or Auth issues.
    """

    app_token = get_config()

    if app_token is False:
        return False

    # Creating a Dropbox object to make requests to the API.
    dbx = dropbox.Dropbox(app_token)

    # Checking token's validity.
    try:
        dbx.users_get_current_account()
    except dropbox.exceptions.AuthError as err:
        print("**AuthError: ", err)
        return False
    except requests.exceptions.ConnectionError as er:
        print("**ConnectionError: ", er)
        return False

    # added.tmp is the file having paths of newly added songs to be uploaded.
    songs_file = os.path.expanduser('~/.sync-music/tmpfiles/added.tmp')
    Index_file = os.path.expanduser('~/.sync-music/tmpfiles/Index')

    with open(songs_file, 'r') as f:
        for song in f:
            song = song.rstrip('\n')

            song_name = (song.split('/'))[-1]
            try:
                with open(song, 'rb') as mp3file:
                    dbx.files_upload(bytes(mp3file.read()), '/'+song_name)
                # main "Index" is getting updated with songs that are
                # successfully uploaded.
                with open(Index_file, 'a') as index:
                    index.write(song)
                    index.write('\n')
            except dropbox.exceptions.AuthError as err:
                print("**AuthError: ", err)
                return False
            except requests.exceptions.ConnectionError as er:
                print("**ConnectionError: ", er)
                return False
    return True


def ask_to_upload():
    """
    This function prompts for user permission, for whether to upload newly
    found songs or not.

    arg1: None

    Return True: if songs are successfully uploaded or if user denies to
                 upload them.
    Return False: if songs are not uploaded successfully.
    """

    choice = ""
    while choice not in ('y', 'Y', 'n', 'N'):
        choice = input("\nWould you like to upload these songs on"
                       " dropbox (y/n)?: ")
        if choice in ('y', 'Y'):
            if upload_dbx():
                return True
            else:
                return False
        elif choice == 'n' or choice == 'N':
            return True
        else:
            print("\nIncorrect input!")


@click.command()
@click.argument('dirs', nargs=-1, required=False)
@click.option('--config',  nargs=2, type=str,
              help="To set configurations e.i:\n"
              "--config dropbox.key <API_key>")
def main(dirs, config):

    if config and update_config(config):
        print("Configured successfully.")
    elif dirs and gen_index(dirs) == 0:
        if ask_to_upload():
            print("\nSongs uploaded successfully.")
        else:
            exit(1)
    else:
        exit(1)


if __name__ == '__main__':
    main()
