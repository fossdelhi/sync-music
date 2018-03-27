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


def get_dropbox_object():
    """
    This function creates a dropbox object to make requests to dropbox API.

    arg1: none

    Return: a valid dropbox object.
    Return False: if dropbox object is not created successfully.
    """

    app_token = get_config()

    if app_token is False:
        return False

    # Creating a Dropbox object
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
    return dbx


def upload_dbx():
    """upload music files to dropbox

    This function uploads songs, whose path is available in the file
    "added.tmp".

    Returns True: if songs get uploaded successfully.
    Returns False: if user denies to proceed for uploading.
                   if dropbox object not created successfully.
                   if uploading encounters any Connectivity or Auth issues.
    """

    if ask_to_proceed("uploading") is False:
        return False

    dbx = get_dropbox_object()
    if dbx is False:
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


def download_dbx(download):
    """download music files from dropbox

    This function downloads your songs from dropbox.

    Returns True: if songs get downloaded successfully.
    Returns False: if user gives invalid option.
                   if user denies to proceed with downloading.
                   if dropbox object not created successfully.
                   if ~/Music not found.
                   if downloading encounters any Connectivity or Auth issues.
    """

    home_dir = os.path.expanduser('~')

    if download == 'all':
        downloadable_songs = home_dir+'/.sync-music/tmpfiles/Index'
    else:
        print("\nCouldn't recognize \"%s\" option. See: sync-music --help" %
              download)
        return False

    print("Following songs are available to download.")
    subprocess.call(['cat', downloadable_songs])

    if ask_to_proceed("downloading") is False:
        return False

    dbx = get_dropbox_object()
    if dbx is False:
        return False

    if os.path.isdir(home_dir+'/Music'):
        saving_dir = home_dir+'/Music/'
    else:
        print("~/Music not found."
              "Please make the directory and then try again.")
        return False

    with open(downloadable_songs, 'r') as f:
        for song in f:
            song = song.rstrip('\n')

            song_name = (song.split('/'))[-1]
            try:
                dbx.files_download_to_file(
                    saving_dir+song_name, '/'+song_name
                )
                print("Downloaded: ", song_name)
            except dropbox.exceptions.HttpError as err:
                print("**HttpError: ", err)
                return False
            except requests.exceptions.ConnectionError as er:
                print("**ConnectionError: ", er)
                return False
    return True


def ask_to_proceed(reason=""):
    """
    This function prompts for user permission, for whether to upload/download
     songs.

    arg1 reason: it can be "uploading" or "downloading".
    Return True: if user grants the permission to upload/download.

    Return False: if user denies the permission to upload/download.
    """

    choice = ""
    while choice not in ('y', 'Y', 'n', 'N'):
        choice = input("Would you like to proceed with %s (y/n)?: " % reason)
        if choice in ('y', 'Y'):
            return True
        elif choice in ('n', 'N'):
            return False
        else:
            print("\nIncorrect input!")


@click.command()
@click.argument('dirs', nargs=-1, required=False)
@click.option('--config', '-c',  nargs=2, type=str,
              help="To set API token: "
              "--config dropbox.key 'token'")
@click.option('--download', '-d', help="Download all you songs back.\n")
def main(dirs, config, download):
    if config and update_config(config):
        print("Configured successfully.")
    # gen_index(dirs) == 0, if songs are available to upload.
    elif dirs and gen_index(dirs) == 0:
        if upload_dbx():
            print("\nSongs uploaded successfully.")
    elif download:
        if download_dbx(download):
            print("\nSongs downloaded successfully.")
    else:
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
