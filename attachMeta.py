import findmeta
import eyed3

songPaths = []
with open('index', 'r') as musicFile:
    for line in musicFile:
        songPaths.append(line.strip())
    
song_files = [x.split('/')[-1] for x in songPaths]
song_files = [x.strip('.mp3') for x in song_files]
artist_and_song = [x.split('-') for x in song_files]

for i in range(len(artist_and_song)):
    for j in range(len(artist_and_song[i])):
        artist_and_song[i][j] = artist_and_song[i][j].strip()

for i in range(len(artist_and_song)):
    for song in artist_and_song[i][-1]:
        tracks = findmeta.getTracks(song)
        found = 0
        track_generator = (track for track in tracks if found!=1) # using generators just to accomodate found and for together
        for track in track_generator:
            artist_generator = (artist for artist in track['Artist(s)'] if found != 1) 
            for artist in artist_generator:
                if artist_and_song[i][0].lower() in artist.lower():
                    song_data = track
                    found = 1
                    break
        if found == 0:
            print('Details for song {} couldn not be found'
                'Skipping for now'
                .format(song))
            break
        song_data = findmeta.getTrackInfo(song_data["Track ID"])
        #
        #audio_file = eyed3.load(songPaths[i])
        #audio_file.tag.artist = song_data["Artist(s)"]
        #audio_file.tag.album = song_data["Album Name"]
        #audio_file.tag.album_artist = song_data["Album Artist(s)"]
        #audio_file.tag.title = song_data["Track Name"]
        #audio_file.tag.track_num = song_data["Track Number"]

        #audio_file.save()
        print('Details of song found are: ')
        findmeta.printDictionary(song_data)
