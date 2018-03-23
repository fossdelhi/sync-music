#!/usr/bin/env python3
import project
import unittest
import sync_music
import os


class TestIndexGeneration(unittest.TestCase):

    """
    Following test run to test multiple cases of user input, while giving
    directories as arguments to this app for syncing.

    An index of songs is generated if user gives valid directories.
    """


    __user_home=os.path.expanduser('~')

    def test_dir_found(self):
        """
        Case: When user gives a valid directory.
        """

        self.assertTrue(
            sync_music.gen_index((os.getcwd(),))
        )


    def test_dir_not_exist(self):
        """
        Case: When any of the given directories doesn't exist.
        """

        self.assertFalse(
            sync_music.gen_index((os.getcwd(),"./non_existing_dir1",))
        )


    def test_dir_not_found(self):
        """
        Case: When user gives relative path to directories, and this app fails
        to find them.
        """

        self.assertFalse(sync_music.gen_index(('../../',)))


    def test_dir_not_given(self):
        """
        Case: When user doesn't give any directory.
        """

        self.assertFalse(sync_music.gen_index(('',)))


if __name__ == '__main__':
    unittest.main()
