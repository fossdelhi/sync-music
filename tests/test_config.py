#!/usr/bin/env python3
import project
import unittest
import sync_music
import os

class TestConfigFile(unittest.TestCase):

    """
    Following test cases run to test those functions which read and write data
    to config files like keys.json.
    """


    def test_create_config_file(self):
        """
        Creates a demo config file for this test series.
        """

        try:
            with open('config_test.json', 'w'):
                pass
            self.assertTrue(True)
        except AttributeError:
            self.assertTrue(False)


    def test_invalid_field(self):
        """
        Case: when user give invalid field to configure.
        """

        self.assertFalse(
            sync_music.update_config(
                ('invalid_field', 'valid_value'), 'config_test.json'
            )
        )


    def test_file_not_found(self):
        """
        Case1: when config file keys.json not found by update_config().
        Case2: when config file keys.json not found by get_config().
        """

        self.assertFalse(
            sync_music.update_config(
                ('dropbox.key', 'valid_value'), './invalid_dir')
        )

        self.assertFalse(sync_music.get_config('./invalid_dir'))


    def test_file_found_empty(self):
        """
        Case: when config file is found with empty values.
        """

        # Creating file with empty values.
        sync_music.update_config(
            ('dropbox.key', ''), 'config_test.json'
        )

        self.assertFalse(sync_music.get_config('config_test.json'))


    def test_file_found(self):
        """
        Case: when config file successfully found.
        """

        self.assertTrue(
            sync_music.update_config(
                ('dropbox.key', 'valid_value'), 'config_test.json'
            )
        )

        # getting configuration that are just added in above assert statement.
        self.assertEqual(
            sync_music.get_config('config_test.json'), 'valid_value'
        )


    def test_remove_file(self):
        """
        This function removes the file created in this test.
        """

        try:
            os.remove('config_test.json')
            self.assertTrue(True)
        except AttributeError:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
