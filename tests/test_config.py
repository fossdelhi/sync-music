#!/usr/bin/env python3
import unittest
import os
import sync_music


class TestConfigFile(unittest.TestCase):

    """
    Following test cases run to test those functions which read and
    write data to and from configuration file "keys.json".
    """

    def setUp(self):
        try:
            with open('for_config_test.json', 'w'):
                pass
        except AttributeError as err:
            print("**Attribute Error: ", err)

    def test_given_invalid_field(self):
        self.assertFalse(
            sync_music.update_user_config_in_file(
                ('invalid_field', 'valid_value'), 'for_config_test.json'
            )
        )

    def test_file_not_found(self):
        self.assertFalse(
            sync_music.update_user_config_in_file(
                ('dropbox.key', 'valid_value'), './invalid_dir')
        )

        self.assertFalse(sync_music.get_user_config_from_file('./invalid_dir'))

    def test_file_found_empty(self):
        # Updating file with empty value.
        sync_music.update_user_config_in_file(
            ('dropbox.key', ''), 'for_config_test.json'
        )

        self.assertFalse(
            sync_music.get_user_config_from_file('for_config_test.json')
        )

    def test_file_found(self):
        self.assertTrue(
            sync_music.update_user_config_in_file(
                ('dropbox.key', 'valid_value'), 'for_config_test.json'
            )
        )

        # getting configuration that are just added in above assert
        # statement.
        self.assertEqual(
            sync_music.get_user_config_from_file('for_config_test.json'),
            'valid_value'
        )

    def tearDown(self):
        try:
            os.remove('for_config_test.json')
        except AttributeError as err:
            print("**Attribute Error: ", err)


if __name__ == '__main__':
    unittest.main()
