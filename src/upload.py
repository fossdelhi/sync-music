#!/usr/bin/env python3
import sys
import dropbox

def upload_to_dbx(song):
    """
    This function uploads the song, whose complete path is given as an argument

    Returns True: if it gets uploaded successfully.
    Returns False: if it encounters any error.
    """
    try:
        with open(song, 'rb') as mp3file:
            dbx.files_upload(bytes(mp3file.read()), '/my_test.mp3')
        return True
    except dropbox.exceptions.AuthError as err:
        sys.exit("ERROR: While uploading the song.")
        return False


if __name__ == '__main__':
    # Accepting access token
    app_token=input("Enter API token: ")

    # Checking if access token is added
    if not len(app_token):
        sys.exit("No tokens are configured.")

    # Creating a Dropbox object to make requests to the API.
    dbx = dropbox.Dropbox(app_token)

    # Checking token's validity.
    try:
        dbx.users_get_current_account()
    except dropbox.exceptions.AuthError as err:
        sys.exit("ERROR: Invalid access token")

    song=input("Enter path to the file to be uploaded: ")

    if upload_to_dbx(song):
        print("Successfully uploaded the song.")
    else:
        print("Uploading failed!")
