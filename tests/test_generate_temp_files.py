#!/usr/bin/env python3
import unittest
import os
import sync_music


class TestGenerateTempFiles(unittest.TestCase):

    """
    Following test run to check multiple cases of user inputs, while
    giving directories as arguments to this app for syncing songs.

    Temporary files are generated if either the directory or new songs
    are found.
    """

    def test_directory_found(self):
        self.assertTrue(sync_music.find_new_songs((os.getcwd(),)) in
                        (True, 3, ))

    def test_directory_not_exist(self):
        self.assertEqual(
            sync_music.find_new_songs(("./non_existing_directory",)), 1
        )

    def test_directory_not_found(self):
        self.assertEqual(sync_music.find_new_songs(('../../',)), 2)

    def test_directory_not_given(self):
        self.assertFalse(sync_music.find_new_songs(('',)))


if __name__ == '__main__':
    unittest.main()
