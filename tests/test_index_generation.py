#!/usr/bin/env python3
import project
import unittest
import sync_music
import os

class TestIndexGeneration(unittest.TestCase):

    """
    Following test cases run when user invoke "sync-music <directory>", To test
    if the application is giving correct messages for different cases.
    """


    __user_home=os.path.expanduser('~')

    def test_dir_found(self):
        """
        Case: When user gives perfect directory.
        """

        # "tmpfiles" directory is created with setup.sh. So, passing it as a
        # valid directory for this test case.
        self.assertTrue(
            sync_music.gen_index((self.__user_home+'/.sync-music/tmpfiles/',))
        )


    def test_dir_not_exist(self):
        """
        Case: When any of the given directory doesn't exist.
        """

        self.assertFalse(
            sync_music.gen_index((self.__user_home+"/non_existing_dir1",))
        )


    def test_dir_not_found(self):
        """
        Case: When user gives combination of "../" and "dir".
        e.i:  $ sync_music ../../dir and this app fails to find the directory.
        """

        self.assertFalse(sync_music.gen_index(('../../',)))

if __name__ == '__main__':
    unittest.main()
