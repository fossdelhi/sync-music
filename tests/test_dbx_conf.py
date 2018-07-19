import unittest
import os
from src import manage_dbx_conf


class TestDbxEnvVar(unittest.TestCase):

    dbx_token = ''

    @classmethod
    def setUpClass(cls):
        # storing the current value of 'dropbox.key' environment variable.
        if manage_dbx_conf.check_dbx_env_var():
            cls.dbx_token = manage_dbx_conf.get_dbx_oauth2_token()
        # giving an arbitrary value to 'dropbox.key' environment variable for
        # following tests.
        os.environ['dropbox.key'] = 'invalid key'

    def test_dotenv_file_found(self):
        dotenv_symlink = os.path.expanduser('~/.sync-music/config/.env')
        if os.path.isfile(dotenv_symlink) and os.path.isfile('.env'):
            self.assertTrue(True)
        else:
            print("\033[1;32mPlease make sure you are running this test"
                  "from project root directory.")
            self.assertTrue(False)

    def test_dbx_env_var_given_invalid_field(self):
        self.assertFalse(manage_dbx_conf.update_dbx_oauth2_token((
            'invalid_field', os.environ['dropbox.key']))
        )

    def test_dbx_env_var_given_valid_field(self):
        self.assertTrue(manage_dbx_conf.update_dbx_oauth2_token((
            'dropbox.key', os.environ['dropbox.key']))
        )

    def test_dbx_env_var_found_empty(self):
        os.environ['dropbox.key'] = ''
        self.assertFalse(manage_dbx_conf.check_dbx_env_var())

    def test_dbx_env_var_found_non_empty(self):
        os.environ['dropbox.key'] = 'invalid key'
        self.assertTrue(manage_dbx_conf.check_dbx_env_var())

    def test_get_dbx_token_successfully(self):
        os.environ['dropbox.key'] = 'a key'
        self.assertEqual(manage_dbx_conf.get_dbx_oauth2_token(), 'a key')

    def test_not_get_dbx_token_successfully(self):
        os.environ['dropbox.key'] = ''
        self.assertFalse(manage_dbx_conf.get_dbx_oauth2_token())

    def test_dbx_env_var_get_update_successfully(self):
        manage_dbx_conf.update_dbx_oauth2_token(('dropbox.key', 'a key'))
        found = False
        try:
            with open('.env', 'r') as f:
                for line in f.readlines():
                    if 'dropbox.key=a key' == line:
                        found = True
            self.assertTrue(found)
        except AttributeError:
            self.assertTrue(False)

    @classmethod
    def tearDownClass(cls):
        os.environ['dropbox.key'] = cls.dbx_token
        manage_dbx_conf.update_dbx_oauth2_token(
            ('dropbox.key', cls.dbx_token)
        )


if __name__ == '__main__':
    unittest.main()
