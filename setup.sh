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
touch "$PWD"/.env


echo -e "\nGiving executable permissions..."
chmod +x ./src/generate_temp_files.sh
chmod +x ./sync_music.py


echo -e "\nCreating required symlinks..."
if [ ! -f ~/.sync-music/scripts/generate_temp_files.sh ]; then
    ln "$PWD"/src/generate_temp_files.sh ~/.sync-music/scripts/generate_temp_files.sh
fi

if [ ! -f ~/.sync-music/config/.env ]; then
    ln "$PWD"/.env ~/.sync-music/config/.env
fi

if [ ! -d ~/bin/ ]; then
    mkdir ~/bin/
fi

if [ ! -L ~/bin/sync-music ]; then
    ln -s "$PWD"/sync_music.py ~/bin/sync-music
fi
