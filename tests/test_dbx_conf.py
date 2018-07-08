import unittest
import os
from src import manage_dbx_conf

class TestDbxEnvVar(unittest.TestCase):

    dbx_token = ''

    def setUp(self):
        if manage_dbx_conf.get_dbx_oauth2_token() == os.environ['dropbox.key']:
            self.dbx_token = os.environ['dropbox.key']
        else:
            self.dbx_token = manage_dbx_conf.get_dbx_oauth2_token()

    def test_dotenv_file_found(self):
        dotenv_symlink  = os.path.expanduser('~/.sync-music/config/.env')
        if os.path.isfile(dotenv_symlink) and os.path.isfile('.env'):
            self.assertTrue(True)
        else:
            print("\033[1;32mPlease make sure you are running this test"
                  "from project root directory.")
            self.assertTrue(False)

    def test_dbx_env_var_given_invalid_field(self):
        self.assertFalse(manage_dbx_conf.update_dbx_oauth2_token((
            'invalid_field', self.dbx_token,))
        )

    def test_dbx_env_var_given_valid_field(self):
        self.assertTrue(manage_dbx_conf.update_dbx_oauth2_token((
            'dropbox.key', self.dbx_token))
        )

    def test_dbx_env_var_found_empty(self):
        os.environ['dropbox.key'] = ''
        self.assertFalse(manage_dbx_conf.check_dbx_env_var())

    def test_dbx_env_var_found_non_empty(self):
        os.environ['dropbox.key'] = 'any value'
        self.assertTrue(manage_dbx_conf.check_dbx_env_var())

    def test_get_dbx_token_successfully(self):
        os.environ['dropbox.key'] = 'any value'
        self.assertEqual(manage_dbx_conf.get_dbx_oauth2_token(),
            'any value')

    def test_not_get_dbx_token_successfully(self):
        os.environ['dropbox.key'] = ''
        self.assertFalse(manage_dbx_conf.get_dbx_oauth2_token())

    def test_dbx_env_var_get_update_successfully(self):
        self.assertTrue(
            manage_dbx_conf.update_dbx_oauth2_token(('dropbox.key', ''))
        )

    def test_dbx_env_var_not_get_update_successfully(self):
        self.assertFalse(
            manage_dbx_conf.update_dbx_oauth2_token(('invalid_value', ''))
        )

    def tearDown(self):
        os.environ['dropbox.key'] = self.dbx_token
        manage_dbx_conf.update_dbx_oauth2_token(('dropbox.key', self.dbx_token))


if __name__ == '__main__':
    unittest.main()
