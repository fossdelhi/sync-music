#!/usr/bin/env python3
import click
import subprocess
import os
import json
import dropbox
import requests
import attachmeta

def find_new_songs(dirs):
    """
    This function calls bash script "generate_temp_files.sh" which
    finds newly added(that are not uploaded) songs in given
    directories. If new songs are found "added.tmp" is generated
    otherwise not.

    :param dirs: tuple of directories.

    :returns: False, if directory given is null string.
    :returns: False, when bash script could not find the required
              directory.
    :returns: 0, if Index is not updated and added.tmp is successfully
              generated.
    :returns: 3, if Index is already updated and no added.tmp is
              generated.
    """

    if dirs == ('',):
        print("\nNull directory!")
        return False

    # calling bash scirpt with given directories as arguments.
    script_path = os.path.expanduser(
        '~/.sync-music/scripts/generate_temp_files.sh'
    )
    call_script = list(dirs)
    call_script.insert(0, script_path)

    res = subprocess.call(call_script)
    # res = 0 if new songs are found and added.tmp is generated and
    # res = 3 if no new song is found and added.tmp not generated.
    if res is 0:
        return True
    else:
        return res


def update_user_config_in_file(config,
                               config_file='~/.sync-music/config/keys.json'):
    """
    This function writes configuration in keys.json, for the field
    whose "key" and "value" is given by user as arguments.

    :param config: tuple consist of ("field of configuration", "value")
    :param config_file: path to configuration file (keys.json).
                        Default path is setup by executing "setup.sh"

    :returns: False, if "field of configuration" is invalid.
    :returns: True, if keys.json is found and configurations are
              updated.
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


def get_user_config_from_file(config_file='~/.sync-music/config/keys.json'):
    """
    This function brings the configration from keys.json. And if
    configurations are not present, then it also give a user friendly
    message to first update their configurations and then try again.

    :param config_file: path to configuration file. Default path is
                        setup by executing "setup.sh".

    :returns: False, if either keys.json is empty or not found.
    :returns: API token, if configurations are successfully read from
              the file.
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
    This function creates a dropbox object to make requests to
    dropbox API.

    :returns: a valid dropbox object.
    :returns: False, if dropbox object is not created successfully.
    """

    app_token = get_user_config_from_file()

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


def upload_to_dropbox():
    """
    This function uploads songs, whose path is available in the file
    "added.tmp".

    :returns: True, if songs get uploaded successfully.
    :returns: False, if user denies to proceed for uploading.
                     if dropbox object not created successfully.
                     if uploading stops due to Connectivity/Auth error.
    """

    if ask_to_proceed("uploading") is False:
        return False

    dbx = get_dropbox_object()
    if dbx is False:
        return False

    # added.tmp: file having paths of newly added songs to be uploaded.
    songs_file = os.path.expanduser('~/.sync-music/tmpfiles/added.tmp')
    Index_file = os.path.expanduser('~/.sync-music/tmpfiles/Index')
    print('Attaching metadata')
    attachmeta.set_data(songs_file)
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


def download_from_dropbox(download):
    """download music files from dropbox

    This function downloads your songs from dropbox.

    :returns: True, if songs get downloaded successfully.
    :returns: False, if user gives invalid option,
                     if user denies to proceed with downloading,
                     if dropbox object not created successfully,
                     if ~/Music not found,
                     if downloading stops due to any Connectivity or
                     Auth error.
    """

    home_dir = os.path.expanduser('~')

    if download == 'all':
        downloadable_songs = home_dir+'/.sync-music/tmpfiles/Index'
    else:
        print("\nCouldn't recognize \"%s\" option. See: sync-music --help" %
              download)
        return False

    print("\n\033[1;33mFollowing songs are available to download:\033[0m\n")
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
    This function prompts for user permission, for whether to
    upload/download songs.

    :param reason: it can be "uploading" or "downloading".
    :returns: True, if user grants the permission to upload/download.

    :returns: False, if user denies the permission to upload/download.
    """

    choice = ""
    while choice not in ('y', 'Y', 'n', 'N'):
        choice = input(
            "\n\033[1;32mWould you like to proceed with %s (y/n)?:\033[0m " %
            reason
        )
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
@click.option('--download', '-d',
              help="To download all your songs back: --download all")
@click.option('--meta', '-m', is_flag=True,
              help="To download metadata only, no upload\n")
def main(dirs, config, download, meta):
    if config and update_user_config_in_file(config):
        print("Configured successfully.")
    # gen_index(dirs) == 0, if songs are available to upload.
    elif dirs and find_new_songs(dirs):
        if upload_to_dropbox():
            print("\nSongs uploaded successfully.")
    elif download:
        if download_from_dropbox(download):
            print("\nSongs downloaded successfully.")
    elif meta:
        print("Attaching Metadata only")
        songs_file = os.path.expanduser('~/.sync-music/tmpfiles/added.tmp')
        attachmeta.set_data(songs_file)
    else:
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
