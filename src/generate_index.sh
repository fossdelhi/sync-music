#!/bin/bash

# Following script generates index.tmp of recent songs and generates a separate
# file of newly added songs.
#
# arg $0: This script file
# arg $1-$9: Directories for syncing music.
#
# exit 1: If given directory is not a valid directory.
# exit 2: If given directly is valid but couldn't found by the app.
# exit $?: exit status of "generate_updates()" function.

# checks the existance of given directories.
for i in "$@"
do
    if [ ! -d "$i" ]
    then
        echo -e "\033[1;31m\nERROR: $i is not a directory.\n\033[0m"
        unset i
        exit 1
    fi
done

# Truncating index.tmp.
> "$HOME"/.sync-music/tmpfiles/index.tmp

# Updating "index.tmp" having complete path of all the current songs.
for i in "$@"
do
    if echo "$i" | grep "^./" >> /dev/null
    then
        entered_dir="$i"
        entered_dir=${entered_dir:1} # to strip "." from the begining
        target_dir="$(pwd)$entered_dir"
        find "$target_dir" -name '*.mp3' >> "$HOME"/.sync-music/tmpfiles/index.tmp
    elif echo "$i" | grep -e "$HOME" -e '^/' >> /dev/null
    then
        find "$i" -name '*.mp3' >> "$HOME"/.sync-music/tmpfiles/index.tmp
    else
         echo -e "\033[0;36m\nERROR: Couldn't complete syncing! Directory isn't found!\n\033[0m"
         unset i
         exit 2
    fi
done


generate_updates()
{
# This function generates file:
#   1. "added": if new songs are now available in the given directory.
#
# arg $1: Index
# arg $2: index.tmp
#
# exit 0: Success, if index.tmp is found and added.tmp is non empty.
# exit 3: Success, if added.tmp is empty that means Index is already updated
#         with no pending songs to upload.
# exit 4: Failure, if index.tmp not found.

# Create Index if not available
[ -f "$1" ] || touch "$HOME"/.sync-music/tmpfiles/Index

# Compare Index with index.tmp and generate file having songs that are newly
# added in the directory.
if [ -f "$2" ]
then
    sort "$1" -o "$1"
    sort "$2" -o "$2"
    diff -n "$1" "$2" | grep '^/' > "$HOME"/.sync-music/tmpfiles/added.tmp

    if [ -s "$HOME"/.sync-music/tmpfiles/added.tmp ]
    then
        echo -e "\n\033[1;33mFollowing songs are newly found in the directory.:\033[0m\n."
        grep '^/' "$HOME"/.sync-music/tmpfiles/added.tmp
        exit 0
    else
        echo -e "\nIndex already upto date."
        exit 3
    fi

else
    echo -e "\033[1;31mERROR: index.tmp is not available."
    exit 4
fi
}


generate_updates "$HOME"/.sync-music/tmpfiles/Index "$HOME"/.sync-music/tmpfiles/index.tmp
exit "$?"
