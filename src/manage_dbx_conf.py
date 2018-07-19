import os


def check_dbx_env_var():
    """
    This function checks for environment variable 'dropbox.key'.

    returns: True, if env variable 'dropbox.key' is available and is not empty.
    returns: False, if env variable 'dropbox.key' isn't available or is empty.
    """
    dbx = 'dropbox.key'
    if dbx not in os.environ.keys() or os.environ[dbx] == '':
            return False

    return True


def update_dbx_oauth2_token(config):
    """
    This function updates dropbox OAuth 2 token in environment variable
    'dropbox.key' with new provided token.

    param config: is a tuple containing "field" and its "value"
                  e.i:- ('dropbox.key', 'OAuth2_token')

    returns: True, if token updated successfully.
    returns: False, if user input incorrect field.
    returns: False, if .env symlink isn't found
    """
    if config[0] != 'dropbox.key':
        print("\nCouldn't recognize {0} option."
              " See: sync-music --help".format(config[0]))
        return False

    env_file = os.path.expanduser('~/.sync-music/config/.env')
    try:
        with open(env_file, 'w') as f:
            f.write('dropbox.key='+config[1])
        return True
    except AttributeError:
        return False


def get_dbx_oauth2_token():
    """
    Function to return dropbox OAuth2 token, from environment variable
    'dropbox.key'.

    returns: token, if .env var 'dropbox.key' is found to be non-empty.
    returns: False, if .env var 'dropbox.key' is found to be empty.
    """
    if check_dbx_env_var():
        return os.environ['dropbox.key']
    else:
        False
