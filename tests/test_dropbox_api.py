#!/usr/bin/env python3
import unittest
import dropbox
import os
import requests
import project
import sync_music


class TestDropboxAPI(unittest.TestCase):

    """
    This module is used to test dropbox API calls, with configurations stored
    in keys.json.

    For this test series make sure you have configured sync-music with Dropbox
    API token with command " $ sync-music --config dropbox.key "API_token" "

    Note: Naming of tests is significant here.
    """

    def test_api_key(self):
        """
        This test case checks the validity of API key.
        """

        app_token = sync_music.get_config()
        if not app_token:
            print("API token is not available in keys.json.")
            self.assertTrue(False)
        else:
            dbx = dropbox.Dropbox(app_token)
            # testing dropbox object validity.
            try:
                dbx.users_get_current_account()
                self.assertTrue(True)
            except dropbox.exceptions.AuthError as err:
                print("ERROR: Invalid access token."
                      "Please add correct API token.\n", err)
                self.assertTrue(False)

    def test_create_file(self):
        """
        Creating a temporary file for this test series.
        """

        try:
            with open("testing_dropbox.tmp", 'w'):
                self.assertTrue(True)
        except AttributeError:
            self.assertTrue(True)

    def test_dropbox_upload(self):
        """
        Case: to upload a file to dropbox.
        """

        app_token = sync_music.get_config()
        dbx = dropbox.Dropbox(app_token)
        try:
            with open("testing_dropbox.tmp", 'rb') as f:
                dbx.files_upload(bytes(f.read()), '/testing_dropbox.tmp')
                self.assertTrue(True)
        except dropbox.exceptions.AuthError as err:
            print("**AuthError: ", err)
            self.assertFalse(True)
        except requests.exceptions.ConnectionError as er:
            print("**Connection: ", er)
            self.assertFalse(True)

    def test_file_download(self):
        """
        Case: to download the file from dropbox. Testing to download the same
        file that has been created in the above test.
        """

        app_token = sync_music.get_config()
        dbx = dropbox.Dropbox(app_token)
        try:
            dbx.files_download_to_file(
                'testing_dropbox.tmp', '/testing_dropbox.tmp'
            )
            if os.path.isfile('testing_dropbox.tmp'):
                self.assertTrue(True)
            else:
                self.assertTrue(False)
        except dropbox.exceptions.AuthError as err:
            print("**AuthError: ", err)
            self.assertFalse(True)
        except requests.exceptions.ConnectionError as er:
            print("**Connection: ", er)
            self.assertFalse(True)

    def test_trashing_files(self):
        """
        This test case deletes files that were created in above cases.
        """

        app_token = sync_music.get_config()
        dbx = dropbox.Dropbox(app_token)
        try:
            os.remove('testing_dropbox.tmp')
            dbx.files_delete('/testing_dropbox.tmp')
        except requests.exceptions.ConnectionError as err:
            print("**Connection: ", err)
            self.assertFalse(True)
        except AttributeError:
            print("File not found")


if __name__ == '__main__':
    unittest.main()
