#!/usr/bin/env python3
from authorize import spotify


def getTracks(search_string=None):
    """
    Get mulitple maching tracks along with their details,
    details like artist, album, and so on.

    :param search_string: Name of track to be searched
    :returns: A list of dictionary of track details.
              The list is sorted by decreasing popularity of tracks found.

    """
    if search_string is None:
        print('Please use a search string with getTracks function')
        exit(0)
    item_type = "tracks"
    info_dict = spotify.search(q=search_string, limit=10, type='track')
    items = info_dict[item_type]["items"]
    tracks = []
    for i in range(len(items)):
        album_name = items[i]["album"]["name"]
        album_type = items[i]["album"]["album_type"]
        artists_names = ', '.join([
            items[i]["artists"][index]["name"]
            for index in range(len(items[i]["artists"]))
        ])
        track_name = items[i]["name"]
        track_id = items[i]["id"]
        track_popularity = items[i]["popularity"]
        tracks.append({"Album Name": album_name,
                       "Album Type": album_type,
                       "Artist(s)": artists_names,
                       "Track Name": track_name,
                       "Popularity": track_popularity,
                       "Track ID": track_id
                       })
    tracks.sort(key=lambda d: d['Popularity'], reverse=True)
    return tracks


def getCategories():
    """
    Spotify has categories, under this, it contains different playlists.
    This function returns available categories.
    like pop, Top Lists, Rock Cavier etc.
    :returns: A list of dictionary
    """
    item_type = "categories"
    info_dict = spotify.categories()
    items = info_dict[item_type]["items"]
    categories = []
    for i in range(len(items)):
        category_name = items[i]["name"]
        category_id = items[i]["id"]
        categories.append({"Category Name": category_name,
                           "Category ID": category_id
                           })
    return categories


def getPlaylists(search_string=None):
    """
    This function will be used to get playlists of a specified category

    :param search_string: Category name whose playlists are required
    """
    item_type = 'playlists'
    info_dict = spotify.category_playlists(search_string)
    items = info_dict[item_type]["items"]
    playlists = []
    for i in range(len(items)):
        playlist_name = items[i]["name"]
        owner_name = items[i]["owner"]["display_name"]
        total_tracks = items[i]["tracks"]["total"]
        playlist_id = items[i]["id"]
        owner_id = items[i]["owner"]["id"]
        playlists.append({"Playlist Name": playlist_name,
                          "Owner Name": owner_name,
                          "No. of tracks": total_tracks,
                          "Playlist ID": playlist_id,
                          "Owner ID": owner_id
                          })
    return playlists


def getPlaylistTracks(user, playlist_id, limit=100):
    """
    Get all the tracks under a playlist

    :param user: The user or owner of the playlist
    :param playlist_id: A unique alphanumeric sequence for a playlist
    :param limit: Limit the number of tracks being fetched at once.

    :returns: A list of dictionary containing track details.
    """
    info_dict = spotify.user_playlist_tracks(user, playlist_id, limit=limit)
    items = info_dict["items"]
    tracks = []
    for i in range(len(items)):
        album_name = items[i]["track"]["album"]["name"]
        album_type = items[i]["track"]["album"]["album_type"]
        artists_names = ', '.join([
            items[i]["track"]["artists"][index]["name"]
            for index in range(len(items[i]["track"]["artists"]))
        ])
        track_name = items[i]["track"]["name"]
        popularity = items[i]["track"]["popularity"]
        track_id = items[i]["track"]["id"]
        tracks.append({"Album Name": album_name,
                       "Album Type": album_type,
                       "Artist(s)": artists_names,
                       "Track Name": track_name,
                       "Popularity": popularity,
                       "Track ID": track_id
                       })
    tracks.sort(key=lambda d: d['Popularity'], reverse=True)
    return tracks


def getTrackInfo(track_id):
    """
    Get information about a specific track.

    :param track_id: A unique alphanumeric sequence for a spotify track.

    :returns: A dictionary containing track details
    """
    items = spotify.track(track_id)
    name = items["name"]
    artists_names = ", ".join([
        items["artists"][x]["name"]
        for x in range(len(items["artists"]))
    ])
    album_artists = ", ".join([
        items["album"]["artists"][x]["name"]
        for x in range(len(items["album"]["artists"]))
    ])
    album_type = items["album"]["album_type"]
    album_name = items["album"]["name"]
    album_release = items["album"]["release_date"]
    album_track_number = items["track_number"]
    track_duration = items["duration_ms"]
    images_link = items["album"]["images"]
    max_image_res = 0
    max_icon_size = 0
    image_link = ""
    icon_link = ""
    for image in images_link:
        if image["height"] * image["width"] > max_image_res:
            image_link = image["url"]
            max_image_res = image["height"] * image["width"]
        if image["height"] < 400:
            if image["height"] > max_icon_size:
                max_icon_size = image["height"]
                icon_link = image["url"]
    track = {"Name Of Song": name,
             "Artist(s)": artists_names,
             "Album Artist(s)": album_artists,
             "Album Type": album_type,
             "Album Name": album_name,
             "Album Release": album_release,
             "Track Number": album_track_number,
             "Track Duration (ms)": track_duration,
             "Image Link": image_link,
             "Icon Link": icon_link
             }
    return track


def printDictionary(d, start_pos=0, end_pos=2):
    """
    Prints dictionaries in list and seperate dictionaries too
    Since displaying all the contents at once might look cumbersome on the
    screen, hence at a time only 4-5 tracks are displayed.

    :param d: dictionary or the list of dictionaries to be printed
    Parameters for list of dictionaries
    :param start_pos: Position from which to start printing dictionary values
    :param end_pos: Position upto which the dictionary is to be displayed

    :returns: 1 for succesfull end of part of dictionaries being displayed
    """
    if type(d) is list:  # end_pos will also act as limit for no. of results
        print("\n" + "_" * 37 + "BEGIN" + "_" * 37 + "\n")
        for i in range(start_pos, end_pos + 1):
            if i == len(d):
                break
            if len(d) != 1:  # Skip item number for single track dictionary
                print("Item no.: {}".format(i + 1))
            for key, value in d[i].items():
                print("{0}: {1}".format(key, value))
            print()

        if i == len(d):
            print("_" * 38 + "END" + "_" * 38 + "\n")
            return 1
        inner_choice = input("Want more results? (y/n): ")
        if inner_choice.lower() in ['y', 'yes']:
            printDictionary(d, start_pos=end_pos + 1, end_pos=end_pos + 5)

    elif type(d) is dict:
        print()
        for key, value in d.items():
            print("{0}: {1}".format(key, value))
        print()


if __name__ == "__main__":

    while True:
        choice = int(input("Menu:\n"
                           "1) Search for a track\n"
                           "2) See available music categories\n"
                           "3) See available playlists in a category\n"
                           "4) Get playlist tracks\n"
                           "5) Get Track Info\n"
                           "6) Exit\n"
                           ))
        print()
        if choice == 1:
            search_string = input('Enter the name of the track to search: ')
            tracks = getTracks(search_string=search_string)
            printDictionary(tracks)  # List top 3 songs that matched
            inner_choice = input("Do you want details on a track? (y/n) ")
            if inner_choice.lower() in ['y', 'yes']:
                item_no = int(
                    input("Enter Item no. of the track you want details: ")
                )
                printDictionary(getTrackInfo(tracks[item_no - 1]["Track ID"]))

        elif choice == 2:
            categories = getCategories()
            printDictionary(categories, end_pos=5)  # Lists 5 categories

        elif choice == 3:
            playlists = getPlaylists(
                search_string=input("Enter the category id: ")
            )
            printDictionary(playlists, end_pos=5)

        elif choice == 4:
            owner = input("Enter the playlist owner: ")
            playlist_id = input("Enter the playlist id: ")
            tracks = getPlaylistTracks(owner, playlist_id, limit=25)
            printDictionary(tracks, end_pos=5)

        elif choice == 5:
            track_id = input("Enter the Track ID: ")
            track = getTrackInfo(track_id)
            printDictionary(track)

        else:
            exit(0)
