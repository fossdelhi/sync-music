import unittest
from src import findmeta


class testFindmetaMethods(unittest.TestCase):

    def test_get_tracks(self):
        tracks = findmeta.get_tracks(search_string="See You Again")
        for track in tracks:
            if track["Track Name"] == "See You Again (feat. Charlie Puth)":
                self.assertEqual(
                    track["Artist(s)"],
                    "Wiz Khalifa, Charlie Puth"
                )
                break

    def test_get_categories(self):
        categories = findmeta.get_categories()
        for category in categories:
            if category["Category Name"] == "Top Lists":
                assert True
                break

    def test_get_playlists(self):
        playlists = findmeta.get_playlists(search_string="toplists")
        for playlist in playlists:
            if playlist["Playlist Name"] == "Today's Top Hits":
                assert True
                break

    def test_get_playlist_tracks(self):
        tracks = findmeta.get_playlist_tracks(
            user="Spotify",
            playlist_id="37i9dQZF1DXcBWIGoYBM5M"
        )  # Uses Today's Top Hits Playlist
        self.assertGreaterEqual(
            tracks[0]["Popularity"],
            tracks[1]["Popularity"]
        )

    def test_get_track_info(self):
        track = findmeta.get_track_info("2JzZzZUQj3Qff7wapcbKjc")
        self.assertEqual(
            track["name"],
            "See You Again (feat. Charlie Puth)"
        )


if __name__ == "__main__":
    unittest.main()
