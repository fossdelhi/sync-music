pip install -U pipenv 
pipenv install .

echo -e "\nCreating directory structure..."
if [ ! -d ~/.sync-music/tmpfiles ]; then
    mkdir -p ~/.sync-music/tmpfiles/
fi
if [ ! -d ~/.sync-music/scripts ]; then
    mkdir -p ~/.sync-music/scripts/
fi
if [ ! -d ~/.sync-music/config ]; then
    mkdir -p ~/.sync-music/config/
fi

echo -e "\nMaking data files..."
touch ~/.sync-music/tmpfiles/index.tmp
touch ~/.sync-music/tmpfiles/Index
touch ~/.sync-music/tmpfiles/added.tmp
touch ~/.sync-music/config/keys.json

echo -e "\nGiving executable permissions..."
chmod +x ./src/generate_temp_files.sh
chmod +x ./sync_music.py

echo -e "\nCreating required symlinks..."
if [ ! -L ~/.sync-music/scripts/generate_temp_files.sh ]; then
    ln -s ./src/generate_temp_files.sh ~/.sync-music/scripts/generate_temp_files.sh 
fi
if [ ! -f $HOME/bin/sync-music ]; then 
    ln -s ./src/sync_music.py $HOME/bin/sync-music
fi
