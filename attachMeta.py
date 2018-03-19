import findmeta
import eyed3

DEBUG=0
def splitByFirstOccurence(string, character):
    if character not in string:
        return [string]
    first_half = string[:string.find(character)]
    first_half = first_half.strip()
    last_half = string[string.find(character)+len(character):]
    if '(' in last_half: # Since the part after the brackets is mostly not required for song name
        last_half = last_half[ :last_half.find('(') ]
    elif '[' in last_half:
        last_half = last_half[:last_half.find('[')]
    last_half = last_half.strip()
    return [first_half, last_half]

songPaths = []
with open('index', 'r') as musicFile:
    for line in musicFile:
        songPaths.append(line.strip())
    
song_files = [x.split('/')[-1] for x in songPaths]
song_files = [x.strip('.mp3') for x in song_files]
artist_and_songs = [splitByFirstOccurence(x, ' - ') for x in song_files]

#for i in range(len(artist_and_songs)):
#    for j in range(len(artist_and_songs[i])):
#        artist_and_songs[i][j] = artist_and_songs[i][j].strip()

for i in range(len(artist_and_songs)):
    song = artist_and_songs[i][-1]
    artists = artist_and_songs[i][0]
    artists = splitByFirstOccurence(artists, '&') #Even if the character is not in string, a single element list would be returned
    tracks = findmeta.getTracks(song)
    found = 0
    track_generator = (track for track in tracks if found!=1) # using generators just to accomodate found and for together
    #import pdb; pdb.set_trace() ##########
    for track in track_generator:
        for artist in artists:
            if artist.lower() in track['Artist(s)'].lower() and found != 1:
                song_data = track
                found = 1
                break
    if found == 0:
        print('Details for song {} could not be found, '
            'skipping for now.'
            .format(song))
        continue
    song_data = findmeta.getTrackInfo(song_data["Track ID"])
    
    if DEBUG != 1:
        audio_file = eyed3.load(songPaths[i])
        audio_file.tag.artist = song_data["Artist(s)"]
        audio_file.tag.album = song_data["Album Name"]
        audio_file.tag.album_artist = song_data["Album Artist(s)"]
        audio_file.tag.title = song_data["Track Name"]
        audio_file.tag.track_num = song_data["Track Number"]
        audio_file.save()
    else:
        print('Details of song found are: ')
        findmeta.printDictionary(song_data)
