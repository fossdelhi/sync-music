import eyed3
import requests
import findmeta


# To avoid the lame tag CRC check warning
eyed3.log.setLevel("ERROR")
def split_by_first_occurence(string, character):
    """
    Split a function by first occurence of a character or a substring,
    and then strip the results.
    Like most song names can have artists name seperated with an '&'
    'Artist1 & Artist2' For this string, and character = '&',the
    function would return ['Artist1', 'Artist2']. This function
     also strips bracket content, to provide better search results.

    :param string: String in which to search
    :param character: character or substring which is to be searched

    :returns: A list of 2 strings, stripped of spaces at the beginning and end
    """
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


def get_song_name(string):
    """
    Get song name from a string. If a string contains feat. words,
    that list featuring artists. Then the function returns the part before it.
    Else whole string is returned.

    :param string: String from which song name is to be found

    :returns: Possible song name from the string
    """
    feat_words = ['ft.', 'feat.', 'by', 'featuring']
    for feat in feat_words:
        if string.find(feat) != -1:
            string = string[:string.find(feat)].strip()
    return string


def get_artists(string, featuring=0):
    """
    Featuring argument is supplied seperately when we want to explicitly
    test its presence else the artist list is returned again and gets
    appended repeatedly. Even in song name if we want to test featuring
    artists name, the song name would be returned if no featuring artist
    is found.

    :param string: String from which artists name can be found
    :param featuring: Flag for checking featuring artists

    :returns: List of possible artists from the string
    """
    artists = []
    if string.find('&') != -1:
        artists = split_by_first_occurence(string, '&')
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


def get_data(song, artists):
    """
    Get the data of a song from song name.
    This uses song and artist name to narrow down to a single song.

    :param song: Song name to be searched
    :param artists: List of artists to be verified against song

    :returns: Dictionary containing song data.
    """
    tracks = findmeta.get_tracks(song)
    found = 0
    track_generator = (track for track in tracks if found != 1)
    # using generators just to accomodate found condition and tracks together
    # in the loop condition.
    song_data = None
    for track in track_generator:
        if artists:
            for artist in artists:
                if artist.lower() in track['Artist(s)'].lower() and found != 1:
                    song_data = track
                    found = 1
                    break
        elif song.lower() == get_song_name(track['Track Name']).lower():
            song_data = track
            found = 1

    return song_data


def strip_numbers_at_beginning(string):
    """
    Stripping numbers and dot in the beginning that might have been added to
    serialize the collection.

    :param string: String from which numbers are to be stripped.

    :returns: String stripped with numbers or numbers and dot.
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


def get_the_song(artist_and_song):
    """
    Check for song names with the spotify database

    :returns: Dictionary containing song data, if the song could be
              found on spotify database

              None if no match is found with artist and names combinations
    """
    artist_and_song = split_by_first_occurence(artist_and_song, ' - ')
    song = get_song_name(artist_and_song[-1])
    artists = get_artists(artist_and_song[0])
    if get_artists(artist_and_song[-1], featuring=1):
        # Only checks if any featuring artist is provided
        artists.extend(get_artists(artist_and_song[-1], featuring=1))
    song_data = get_data(song, artists)
    if song_data is None:
        # Strip numbers that might appear before artists name in
        # beginning of filename
        artists[0] = strip_numbers_at_beginning(artists[0])
        song_data = get_data(song, artists)

    if song_data is None:
        song = get_song_name(artist_and_song[0])
        artists = get_artists(artist_and_song[-1])
        if get_artists(artist_and_song[0], featuring=1):
            artists.extend(get_artists(artist_and_song[0], featuring=1))
        song_data = get_data(song, artists)

    if song_data is None:  # For song names like "12. See you again.mp3"
        song = strip_numbers_at_beginning(song)
        song_data = get_data(song, artists)

    if song_data is None:  # Find for exact name match if other things fail
        song_data = get_data(song, None)
        if song_data is None:
            song_data = get_data(get_song_name(artist_and_song[-1]), None)

    if song_data is None:
        print("Can't find data for song: {}".format(song))

    return song_data


def set_data(song_name_file='index', DEBUG=False):
    """
    Sets the metadata to the song files, using eyed3 module
    If this function is called using main, then it searches for a file
    named index for addresses of the songs.

    :param song_name_file: File from which song path are to be fetched
    :param DEBUG: Set this to 1 to print results to screen, rather than adding
                  to the songs repeatedly
    """
    song_paths = []
    with open(song_name_file, 'r') as music_file:
        for line in music_file:
            song_paths.append(line.strip())

    song_files = [x.split('/')[-1] for x in song_paths]
    song_files = [x.strip('.mp3') for x in song_files]

    for i in range(len(song_files)):
        artist_and_song = song_files[i]
        song_data = get_the_song(artist_and_song)
        if song_data is None:
            continue
        song_data = findmeta.get_track_info(song_data["Track ID"])

        if DEBUG != 1:
            audio_file = eyed3.load(song_paths[i])
            if audio_file:
                try:
                    audio_file.tag.artist = song_data["Artist(s)"]
                except AttributeError:
                    # To add id3 tags if they aren't present
                    audio_file.init_tag()
                    audio_file.tag.artist = song_data["Artist(s)"]
                audio_file.tag.album = song_data["Album Name"]
                audio_file.tag.album_artist = song_data["Album Artist(s)"]
                audio_file.tag.title = song_data["name"]
                audio_file.tag.track_num = song_data["Track Number"]
                if song_data["Image Link"]:
                    req = requests.get(song_data["Image Link"])
                    audio_file.tag.images.set(
                        3, req.content, 'jpg', song_data["Album Name"]
                    )
                    # 0 For other Image, 1 for Icon, 2 for Other Icon, 3 for
                    # front cover, 4 for Back cover
                if song_data["Icon Link"]:
                    req = requests.get(song_data["Icon Link"])
                    audio_file.tag.images.set(
                        1, req.content, 'jpg', song_data["name"]
                    )
                if "lyrics" in song_data.keys():
                    audio_file.tag.lyrics.set(
                        song_data["lyrics"], song_data["name"]
                    )

                audio_file.tag.save()

                print('Saved details for : {}'.format(
                    song_data['name']
                ))
            else:
                print("{}\n Couldn't be found".format(song_files[i]))
        else:
            print('Details of song found are: ')
            findmeta.print_dictionary(song_data)


if __name__ == "__main__":
    set_data()
