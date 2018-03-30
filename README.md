# sync-music 
A project, to ease backup, add metadata, and sync your music using cloud storage. :)

## Installing 
To install, do:
```
pip install pipenv 
pipenv install . 
``` 

## Usage 
Type : 
`python3 src/attachmeta.py` 
This requires an `index` file to contain address of songs, to whom metadata is to be added 
The path should be an absolute path. 
In case the song name couldn't be deduced from the filename, and error will be displayed. 

## Testing 
To test, simply do: 
`python3 -m unittest discover tests` 
