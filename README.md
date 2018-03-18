# sync-music
A project, to ease backup, add metadata, and sync your music using cloud storage. :)

This app is build up with Python [3.5, 3.6] and Shell [Bash: 4.3] Script.
Sync-music creates a backup of your music files (.mp3) on dropbox. And in case you loose your hard-disk or change your laptop, using this app, you may get your songs back to your new device.

## FOLLOWING STEPS AREN'T APPLICABLE. CURRENTLY THE PROJECT IS UNDER DEVELOPMENT.

### Before Installing
As we have used dropbox as the medium to upload music. You need to sign up on dropbox. And generate your tokens.

### Installing
#### On Ubuntu
$ cd ~/ && clone https://github.com/fossdelhi/sync-music/ && cd sync-music
$ sudo updatedb
$ sudo pip install -r requirements.txt

Generate your tokens from dropbox and spotify developers console and configure with these commands:
$ sync-music --config dropbox.key ""
$ sync-music --config dropbox.seckey ""
$ sync-music --config spotify.key ""
$ sync-music --config spotify.seckey ""

Now sync-music is ready to sync your favorite songs.

### Working
To sync your songs from a directory say "~/Mymusic" just give a command.
$ sync-music -d ~/Mymusic
or to sync multiple directories
$ sync-music -d ./any_dir -d ./other_dir

### CAUTION
DO NOT USE "../../dirA/../" or any complex "../" "./" combinations. MAKE SURE YOUR DIRECTORY NAME EITHER STARTS WITH "./" or "~/".

### Regular refresh
Refreshing sync-music makes sure that you don't miss your newly added songs to sync with dropbox. Also, if you accidently deleted any of your mp3 file, then refreshing will prompt you to bring them back if you want.

$ sync-music --refresh

The code of this app is available with MIT LICENSE.
Suggestions for Improvement and Pull requests are appreciated.
