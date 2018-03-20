#!/bin/bash

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

# Generating a blank ./data/.tmp_index
[ -f "$HOME"/.sync-music/tmpfiles/index.tmp ] && > "$HOME"/.sync-music/tmpfiles/index.tmp

# Updating "index.tmp" having complete path of all the current songs.
for i in "$@"
do
    if echo "$i" | grep "^./" >> /dev/null
    then
        entered_dir="$i"
        entered_dir=${entered_dir:1} # to strip "." from begining
        target_dir="$(pwd)$entered_dir"
        find "$target_dir" -name '*.mp3' >> "$HOME"/.sync-music/tmpfiles/index.tmp
    elif echo "$i" | grep "$HOME" >> /dev/null
    then
        find "$1" -name '*.mp3' >> "$HOME"/.sync-music/tmpfiles/index.tmp
    else
         echo -e "\033[0;36m\nERROR: Couldn't complete syncing! Directory isn't found!\n\033[0m"
         unset i
         exit 2
    fi
done

cat "$HOME"/.sync-music/tmpfiles/index.tmp > "$HOME"/.sync-music/tmpfiles/Index
echo -e "\n\033[1;33mFollowing songs are added in the database:\033[0m\n"
cat "$HOME"/.sync-music/tmpfiles/Index
exit 0
