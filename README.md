# sync-music
[![Build Status](https://travis-ci.org/fossdelhi/sync-music.svg?branch=syncing)](https://travis-ci.org/fossdelhi/sync-music)

A project, to ease backup, add metadata, and sync your music using cloud storage. :)

This app is build up with Python [3.5, 3.6] and Shell [Bash: 4.3] Script.
Sync-music creates a backup of your music files (.mp3) on dropbox. And in case you loose your hard-disk or change your laptop, using this app, you may get your songs back to your new device without manually downloading them from dropbox.

### Before Installing
As this app uses dropbox as the medium to upload music. You need to sign up on dropbox. And generate your tokens from [dropbox developers console](https://www.dropbox.com/developers/apps).

### Installing
#### On Ubuntu
```
$ cd ~/ && clone https://github.com/fossdelhi/sync-music/
$ cd sync-music
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
The code of this app is available with [MIT LICENSE](https://github.com/fossdelhi/sync-music/blob/syncing/LICENSE).
Suggestions for Improvement and Pull requests are appreciated.
