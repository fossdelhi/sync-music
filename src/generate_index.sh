#!/bin/bash

# This script generates following files
#   1. index.tmp: consists of paths of mp3 files found in the given directories.
#   2. added.tmp: consists of newly found songs in the given directories.
#
# arg $0: This script file
# arg $1-$9: Directories to search for mp3 files.
#
# exit 1: If given directory is not a valid directory.
# exit 2: If given directory is valid but couldn't found by the application.
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

# Generating empty index.tmp
: > "$HOME"/.sync-music/tmpfiles/index.tmp


# Updating "index.tmp" having paths of all the mp3 files in given directories.
for i in "$@"
do
    if echo "$i" | grep "^./" >> /dev/null
    then
        # making relative path from current working directory.
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
# This function generates following file:
#   1. "added.tmp": if new songs are found in the given directory.
#
# arg $1: Index
# arg $2: index.tmp
#
# exit 0: Success, if index.tmp is found and added.tmp is not empty.
# exit 3: Success, if added.tmp is empty that means Index is already updated
#         with no pending songs to upload.

# Compares Index with index.tmp and generates file having songs that are newly
# added in the directory.
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
}


generate_updates "$HOME"/.sync-music/tmpfiles/Index "$HOME"/.sync-music/tmpfiles/index.tmp
exit "$?"
