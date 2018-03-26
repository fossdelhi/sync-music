# sync-music
[![Build Status](https://travis-ci.org/fossdelhi/sync-music.svg?branch=syncing)](https://travis-ci.org/fossdelhi/sync-music)

A project, to ease backup, add metadata, and sync your music using cloud storage. :)

This app is build up with Python [3.5, 3.6] and Shell [Bash: 4.3] Script.
Sync-music creates a backup of your music files (.mp3) on dropbox and you get rid of logging into dropbox account to download your music files. In case you loose your hard-disk or change your laptop, using this app, you may get your songs back to your new device.

### Before Installing
As this app uses dropbox as the host to upload your songs. You need to sign up on dropbox. And generate your tokens from [dropbox developers console](https://www.dropbox.com/developers/apps).

### Installing
```
$ cd ~/ && clone https://github.com/fossdelhi/sync-music/
$ cd sync-music
$ pip install -r requirements.txt
$ bash setup.sh
```

Generate your tokens from dropbox developers console and configure with this command:
```
$ sync-music --config dropbox.key "API_token"
```

Now sync-music is ready to sync your favorite songs.

### Working
To sync your songs from a directory say "~/Mymusic" just give a command.
```
$ sync-music ~/Mymusic
```
Or sync multiple directories with.
```
$ sync-music ~/complete/path/to/dir ~/other_dir
```
#### CAUTION
Make sure the name of directories you give either starts with a dot "." or with home directory symbol "~"(recommended).

### Regular refresh
Refreshing sync-music makes sure that you don't miss your newly added songs to sync with dropbox. Also, if you accidently deleted any of your mp3 file, then refreshing will prompt you to bring them back if you want.

**This option is currently not applicable.**
```
$ sync-music --refresh
```

### Testing
This app supports unit testing with ```Unittest```.
**Before running tests make sure, that you have installed ```requirements```, ```unittest``` through ```pip``` and executed ```setup.sh``` successfully.**

There are following 3 aspacts for which you may run test cases:
(run these tests from application directory)

1. To test songs Index generation ```$ python3 ./tests/test_index_generation.py```
2. To test reading/writing configurations ```$ python3 ./tests/test_config.py```
3. To test dropbox api call ```$ python3 ./dropbox_api.py```

### Important files
Following files are created when you run ```setup.sh```. Their importance and usage is as follows:

1. index.tmp: this file holds the paths of all mp3 files that are found in those directories that you pass as arguments e.i ```$ sync-music ~/dir1 ~/dir2```
2. Index: this file stored the paths of all mp3 files that are uploaded on dropbox.
3. added.tmp: this file holds the paths of all those mp3 files that are newly found in the directories that you pass as arguments. It doesn't include songs of ```Index``` only contains newly added songs.
4. keys.json: this file stored your dropbox API token.

The code of this app is available with [MIT LICENSE](https://github.com/fossdelhi/sync-music/blob/syncing/LICENSE).
Suggestions for Improvement and Pull requests are appreciated.
