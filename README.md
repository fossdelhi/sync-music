# sync-music
[![Build Status](https://travis-ci.org/fossdelhi/sync-music.svg?branch=master)](https://travis-ci.org/fossdelhi/sync-music)

A project, to ease backup, add metadata, and sync your music using cloud storage. :)

This app is build up with Python [3.5] and Shell [Bash: 4.3] Script.
Sync-music creates a backup of your music files (.mp3) on dropbox and you get rid of logging into dropbox account to download your music files. In case you loose your hard-disk or change your laptop, using this app, you may get your songs back to your new device.

### Before Installing
As this app uses dropbox as the host to upload your songs. You need to sign up on dropbox. And generate your tokens from [dropbox developers console](https://www.dropbox.com/developers/apps).

### Installing
```
$ cd ~
$ git clone https://github.com/fossdelhi/sync-music/
$ cd sync-music
$ . ./setup.sh
```

And to run the app you would need to activate the virtual environment from application directory with the following command:
```
$ pipenv shell
```

Generate your API token from dropbox developers console and configure with this command:
```
$ sync-music --config dropbox.key "API_token"
```
Generate your client_id and client_secret from spotify developer website, and put them in a .env file in this directory. They will be autmatically loaded when the virtual environment in launched.

Now sync-music is ready to sync your favorite songs.

### Working
#### To Upload
To upload your songs from a directory, say "~/Mymusic", just give a command:
```
$ sync-music ~/Mymusic
```
Or sync multiple directories with:
```
$ sync-music ~/complete/path/to/dir ~/other_dir
```

This uploads the songs in the directory to your dropbox, and also attaches metadata to them before uploading.
#### CAUTION
Make sure that the path to directories you give either starts with a dot ```.``` like ```./Mymusic/``` (relative path from current working directory) or with home directory symbol ```~``` like ```~/Mymusic/classic/``` (complete path). Because, current version of the app won't be able to find directories if you would give their path as ```../../dir```.

#### To download
Following command will download all your uploaded songs to ```~/Music/```.

```
$ sync-music --download all
```

#### Regular refresh
Refreshing sync-music makes sure that you don't miss your newly added songs to sync with dropbox. Also, if you accidently deleted any of your mp3 file, then refreshing will prompt you to bring them back if you want.

```
$ sync-music --refresh
```
**Regular refresh and selective downloading are not applicable for the current version.**

### Attaching metadata only

You can attach meta data to songs without uploading them using the `-m` or `--meta` option. You need to specify the path of the file containing absolute path of songs. For example:

```
$ sync-music -m abc
```

This will attach metadata to all the songs whose absolute paths are available in the file named `abc`.

### Testing
This application supports unit testing with ```Unittest```.

**Before running tests make sure, that you have installed ```unittest``` through ```pip```, executed ```setup.sh``` successfully and you are in virtual environment of the application.**

There are following 3 aspects for which you may run test cases:
(run these tests from application directory)

1. To test songs Index generation ```$ python3 -m tests.test_generate_temp_files```
2. To test reading/writing configurations ```$ python3 -m tests.test_config```
3. To test dropbox api call ```$ python3 -m tests.test_dropbox_api```

To run all the tests with single command use:
```$ python3 -m unittest discover tests```


### Important files
Following files are created when you run ```setup.sh```. Their importance and usage is as follows:

1. index.tmp: this file holds the paths of all mp3 files that are found in those directories that you pass as arguments i.e ```$ sync-music ~/dir1 ~/dir2```
2. Index: this file stores the paths of all mp3 files that are uploaded on dropbox.
3. added.tmp: this file holds the paths of all those mp3 files that are newly found in the directories that you pass as arguments. It doesn't include songs of ```Index``` only contains newly added songs.
4. keys.json: this file stores your dropbox API token.

The code of this app is available with [MIT LICENSE](https://github.com/fossdelhi/sync-music/blob/syncing/LICENSE).
Suggestions for Improvement and Pull requests are appreciated.

