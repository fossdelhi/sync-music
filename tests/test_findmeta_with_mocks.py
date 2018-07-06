from unittest.mock import patch
import unittest
from src import sample_data
from src import findmeta


class testFindmetaMethods(unittest.TestCase):

    @patch('src.findmeta.spotify.search')
    def test_get_tracks(self, mock_search_results):
        mock_search_results.return_value = sample_data.of_get_tracks
        tracks = findmeta.get_tracks(search_string="See You Again")
        for track in tracks:
            if track["Track Name"] == "See You Again (feat. Charlie Puth)":
                self.assertEqual(
                    track["Artist(s)"],
                    "Wiz Khalifa, Charlie Puth"
                )
                break

    @patch('src.findmeta.spotify.categories')
    def test_get_categories(self, mock_category_results):
        mock_category_results.return_value = sample_data.of_get_categories
        categories = findmeta.get_categories()
        for category in categories:
            if category["Category Name"] == "Top Lists":
                assert True
                break

    @patch('src.findmeta.spotify.category_playlists')
    def test_get_playlists(self, mock_playlists):
        mock_playlists.return_value = sample_data.of_get_playlists
        playlists = findmeta.get_playlists(search_string="toplists")
        for playlist in playlists:
            if playlist["Playlist Name"] == "Today's Top Hits":
                assert True
                break

    @patch('src.findmeta.spotify.user_playlist_tracks')
    def test_get_playlist_tracks(self, mock_playlist_tracks):
        mock_playlist_tracks.return_value = sample_data.of_get_playlist_tracks
        tracks = findmeta.get_playlist_tracks(
            user="Spotify",
            playlist_id="37i9dQZF1DXcBWIGoYBM5M"
        )  # Uses Today's Top Hits Playlist
        self.assertGreaterEqual(
            tracks[0]["Popularity"],
            tracks[1]["Popularity"]
        )

    @patch('src.findmeta.spotify.track')
    def test_get_track_info(self, mock_track_metadata):
        mock_track_metadata.return_value = sample_data.of_get_track_info
        track = findmeta.get_track_info("2JzZzZUQj3Qff7wapcbKjc")
        self.assertEqual(
            track["name"],
            "See You Again (feat. Charlie Puth)"
        )


if __name__ == "__main__":
    unittest.main()
