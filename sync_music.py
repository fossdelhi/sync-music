#!/usr/bin/env python3
import click
import subprocess
import os
import json
import dropbox
import requests
from src import attachmeta
from src import manage_dbx_conf


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


def get_dropbox_object():
    """
    This function creates a dropbox object to make requests to
    dropbox API.

    :returns: a valid dropbox object.
    :returns: False, if dropbox object is not created successfully.
    """

    app_token = manage_dbx_conf.get_dbx_oauth2_token()

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
    print('Attaching metadata:')
    attachmeta.set_data(songs_file)
    print('\nUploading:')
    with open(songs_file, 'r') as f:
        for song in f:
            song = song.rstrip('\n')

            song_name = (song.split('/'))[-1]
            try:
                print("[*] {0}".format(song_name), end='\r')
                with open(song, 'rb') as mp3file:
                    dbx.files_upload(bytes(mp3file.read()), '/'+song_name)
                # main "Index" is getting updated with songs that are
                # successfully uploaded.
                with open(Index_file, 'a') as index:
                    index.write(song)
                    index.write('\n')
                tick_mark = '\u2713'
                print("[\033[0;32m{0}\033[0m] {1}".format(
                      tick_mark, song_name))
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
    with open(downloadable_songs, 'r') as file:
        for absolute_path in file:
            print("{0}".format(
                  click.format_filename(absolute_path, shorten=True)))

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
@click.argument('dirs', nargs=-1, required=False,
                type=click.Path(exists=True, dir_okay=True, resolve_path=True))
@click.option('--config', '-c',  nargs=2, type=str,
              help="To set API token: "
              "--config dropbox.key 'token'")
@click.option('--download', '-d',
              help="To download all your songs back: --download all")
@click.option('--meta', '-m', type=click.Path(exists=True, resolve_path=True),
              help="To download metadata only, no upload\n")
def main(dirs, config, download, meta):
    if config:
        if manage_dbx_conf.check_dbx_env_var():
            print("\nOverwriting previous token.")
        if manage_dbx_conf.update_dbx_oauth2_token(config):
            print("Configured successfully.")
            print("\nNow please restart pipenv with: 1)exit 2)pipenv shell")
    elif dirs and find_new_songs(dirs):
        if upload_to_dropbox():
            print("\nSongs uploaded successfully.")
    elif download:
        if download_from_dropbox(download):
            print("\nSongs downloaded successfully.")
    elif meta:
        print("Attaching Metadata only to the songs in file: "
              "{0}".format(click.format_filename(meta, shorten=True)))
        attachmeta.set_data(meta)
    else:
        exit(1)
    exit(0)


if __name__ == '__main__':
    main()
