
pip install pipenv
pipenv install .

echo -e "\nCreating directory structure..."
mkdir -p ~/.sync-music/tmpfiles/
mkdir -p ~/.sync-music/scripts/
mkdir -p ~/.sync-music/config/

echo -e "\nMaking data files..."
touch ~/.sync-music/tmpfiles/index.tmp
touch ~/.sync-music/tmpfiles/Index
touch ~/.sync-music/tmpfiles/added.tmp
touch ~/.sync-music/config/keys.json

echo -e "\nGiving executable permissions..."
chmod +x ./src/generate_temp_files.sh
chmod +x ./src/sync_music.py

echo -e "\nCreating required symlinks..."
ln -s ./src/generate_temp_files.sh ~/.sync-music/scripts/generate_temp_files.sh 
sudo ln ./src/sync_music.py /usr/bin/sync-music
