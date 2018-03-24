#!/usr/bin/env python3
import unittest
import dropbox
import project
import sync_music


class TestDropboxAPI(unittest.TestCase):

    """
    This module is used to test dropbox API call, with configurations stored
    in keys.json.
    """

    def test_api_call(self):
        """
        For this test make sure you have configured sync-music with Dropbox API
        Token with command " $ sync-music --config dropbox.key "API_token" "

        Otherwise this test case will fail.
        """

        app_token = sync_music.get_config()
        if not app_token:
            print("API token is not available in keys.json.")
            self.assertTrue(False)
        else:
            dbx = dropbox.Dropbox(app_token)
            try:
                dbx.users_get_current_account()
                self.assertTrue(True)
            except dropbox.exceptions.AuthError as err:
                print("ERROR: Invalid access token."
                      "Please add correct API token.\n", err)
                self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
