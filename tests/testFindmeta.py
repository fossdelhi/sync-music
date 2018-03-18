import unittest
import setPaths
import findmeta

class testFindmetaMethods(unittest.TestCase):

	def test_getTracks(self):
		tracks = findmeta.getTracks(item_type="tracks", search_string="See You Again")
		for track in tracks:
			if track["Track Name"] == "See You Again (feat. Charlie Puth)":
				self.assertEqual(track["Artist(s)"], "Wiz Khalifa, Charlie Puth")
				break

	def test_getTracks_categories(self):
		categories = findmeta.getTracks(item_type='categories')
		for category in categories:
			if category["Category Name"] == "Top Lists":
				assert True
				break


	def test_getTracks_playlists(self):
		playlists = findmeta.getTracks(item_type="playlists", search_string="toplists")
		for playlist in playlists:
			if playlist["Playlist Name"] == "Today's Top Hits":
				assert True
				break

	def test_getPlaylistTracks(self):
		tracks = findmeta.getPlaylistTracks(user="Spotify", playlist_id="37i9dQZF1DXcBWIGoYBM5M")
		self.assertEqual(tracks[0]["Popularity"], 100)

	def test_getTrackInfo(self):
		track = findmeta.getTrackInfo("2JzZzZUQj3Qff7wapcbKjc")
		self.assertEqual(track["Name Of Song"], "See You Again (feat. Charlie Puth)")


if __name__ == "__main__":
	unittest.main()