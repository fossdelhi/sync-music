#!/bin/bash

cd ~

echo -e "\nCreating directory structure..."
mkdir -p ~/.sync-music/tmpfiles/
mkdir -p ~/.sync-music/scripts/
mkdir -p ~/.sync-music/config/

echo -e "\nMaking data files..."
touch ~/.sync-music/tmpfiles/index.tmp
touch ~/.sync-music/tmpfiles/Index
touch ~/.sync-music/tmpfiles/added.tmp
touch ~/.sync-music/tmpfiles/deleted.tmp
touch ~/.sync-music/config/keys.json

echo -e "\nGiving executable permissions..."
chmod +x ~/sync-music/src/generate_index.sh
chmod +x ~/sync-music/src/sync_music.py

echo -e "\nCreating required symlinks..."
ln ~/sync-music/src/generate_index.sh ~/.sync-music/scripts/generate_index.sh
ln ~/sync-music/src/sync_music.py /usr/bin/sync-music
