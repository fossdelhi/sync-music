import findmeta
import eyed3
import requests


def splitByFirstOccurence(string, character):
    if character not in string:
        return [string]
    first_half = string[:string.find(character)]
    first_half = first_half.strip()
    last_half = string[string.find(character) + len(character):]
    if '(' in last_half:
        # part after the brackets is mostly not required for song name
        last_half = last_half[:last_half.find('(')]
    elif '[' in last_half:
        last_half = last_half[:last_half.find('[')]
    last_half = last_half.strip()
    return [first_half, last_half]


def getSongName(string):
    feat_words = ['ft.', 'feat.', 'by', 'featuring']
    for feat in feat_words:
        if string.find(feat) != -1:
            string = string[:string.find(feat)].strip()
    return string


def getArtists(string, featuring=0):
    """
        featuring argument is supplied seperately when we want to explicitly
        test it's presence else the artist list is returned again and get's
        appended repeatedly. Even in song name if we want to test featuring
        artists name, the song name would be returned if no featuring artist
        is found.
    """
    artists = []
    if string.find('&') != -1:
        artists = splitByFirstOccurence(string, '&')
        # Returns single element list, if character not in string
    found = 0
    feat_words = ['ft.', 'feat.', 'by', 'featuring']
    for feat in feat_words:
        if string.find(feat) != -1:
            artists.append(string[string.find(feat) + len(feat):].strip())
            found = 1
    for i in range(len(artists)):
        for feat in feat_words:
            if artists[i].find(feat) != -1:
                artists[i] = artists[i][:artists[i].find(feat)].strip()
    if featuring == 1 and found == 0:
        return None
    if artists == []:
        return [string]
    return artists


def getData(song, artists):
    tracks = findmeta.getTracks(song)
    found = 0
    track_generator = (track for track in tracks if found != 1)
    # using generators just to accomodate found and for together
    song_data = None
    for track in track_generator:
        if artists:
            for artist in artists:
                if artist.lower() in track['Artist(s)'].lower() and found != 1:
                    song_data = track
                    found = 1
                    break
        elif song.lower() == getSongName(track['Track Name']).lower():
            song_data = track
            found = 1

    return song_data


def stripNumbersAtBeginning(string):
    """
    Stripping numbers in the beginning that might have been added to
    serialize the collection.
    """
    temporary_index = 0
    for character in string:
        if not character.isdigit():
            break               # Now it points to the last non digit character
        temporary_index += 1
    if character in ['.', ')']:
        temporary_index += 1   # Before incrementing it points to . or )
    string = string[temporary_index:]
    return string.strip()


def getTheSong(artist_and_song):
    """
    Check for song names with the spotify database
    if no match is found with artist and names combinations
    return none
    """
    artist_and_song = splitByFirstOccurence(artist_and_song, ' - ')
    song = getSongName(artist_and_song[-1])
    artists = getArtists(artist_and_song[0])
    if getArtists(artist_and_song[-1], featuring=1):
        # Only checks if any featuring artist is provided
        artists.extend(getArtists(artist_and_song[-1], featuring=1))
    song_data = getData(song, artists)
    if song_data is None:
        # Strip numbers that might appear before artists name in
        # beginning of filename
        artists[0] = stripNumbersAtBeginning(artists[0])
        song_data = getData(song, artists)

    if song_data is None:
        song = getSongName(artist_and_song[0])
        artists = getArtists(artist_and_song[-1])
        if getArtists(artist_and_song[0], featuring=1):
            artists.extend(getArtists(artist_and_song[0], featuring=1))
        song_data = getData(song, artists)

    if song_data is None:  # For song names like "12. See you again.mp3"
        song = stripNumbersAtBeginning(song)
        song_data = getData(song, artists)

    if song_data is None:  # Find for exact name match if other things fail
        song_data = getData(song, None)
        if song_data is None:
            song_data = getData(getSongName(artist_and_song[-1]), None)

    if song_data is None:
        print("Can't find data for song: {}".format(song))

    return song_data


def setData(SONG_NAME_FILE="index", DEBUG=0):
    songPaths = []
    with open(SONG_NAME_FILE, 'r') as musicFile:
        for line in musicFile:
            songPaths.append(line.strip())

    song_files = [x.split('/')[-1] for x in songPaths]
    song_files = [x.strip('.mp3') for x in song_files]

    for i in range(len(song_files)):
        artist_and_song = song_files[i]
        song_data = getTheSong(artist_and_song)
        if song_data is None:
            continue
        song_data = findmeta.getTrackInfo(song_data["Track ID"])

        if DEBUG != 1:
            audio_file = eyed3.load(songPaths[i])
            if audio_file:
                try:
                    audio_file.tag.artist = song_data["Artist(s)"]
                except AttributeError:
                    # To add id3 tags if they aren't present
                    audio_file.initTag()
                    audio_file.tag.artist = song_data["Artist(s)"]
                audio_file.tag.album = song_data["Album Name"]
                audio_file.tag.album_artist = song_data["Album Artist(s)"]
                audio_file.tag.title = song_data["Name Of Song"]
                audio_file.tag.track_num = song_data["Track Number"]
                if song_data["Image Link"]:
                    req = requests.get(song_data["Image Link"])
                    audio_file.tag.images.set(3, req.content, 'jpg')
                    # 0 For other Image, 1 for Icon, 2 for Other Icon, 3 for
                    # front conver, 4 for Back cover
                if song_data["Icon Link"]:
                    req = requests.get(song_data["Icon Link"])
                    audio_file.tag.images.set(1, req.content, 'jpg')
                audio_file.tag.save()

                print('Saved details for : {}'.format(
                    song_data['Name Of Song']
                ))
            else:
                print("{}\n Couldn't be found".format(song_files[i]))
        else:
            print('Details of song found are: ')
            findmeta.printDictionary(song_data)


if __name__ == "__main__":
    setData()
