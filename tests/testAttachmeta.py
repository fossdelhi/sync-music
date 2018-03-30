import unittest
from src import attachmeta


class testAttachmetaMethods(unittest.TestCase):
    def test_split_by_first_occurence(self):
        string = "First half - Last Half"
        self.assertEqual(
            attachmeta.split_by_first_occurence(string, '-'),
            ["First half", "Last Half"]
        )
        string = "First half - Second Half - Last Half"
        self.assertEqual(
            attachmeta.split_by_first_occurence(string, '-'),
            ["First half", "Second Half - Last Half"]
        )

    def test_get_song_name(self):
        self.assertEqual(
            attachmeta.get_song_name('Source Code ft. Developers'),
            'Source Code'
        )

    def test_get_artists(self):
        self.assertEqual(
            attachmeta.get_artists('artist1 & artist2'),
            ['artist1', 'artist2']
        )
        self.assertEqual(
            attachmeta.get_artists(
                'artist1 & artist2 ft. artist3',
                featuring=1
            ),
            ['artist1', 'artist2', 'artist3']
        )
        self.assertIsNone(
            attachmeta.get_artists('artist1 & artist2', featuring=1)
        )

    def test_get_data(self):
        self.assertEqual(
            attachmeta.get_data('see you again', ['wiz khalifa'])["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )
        self.assertIsNone(
            attachmeta.get_data('some random song', ['artist1', 'artist2'])
        )

    def test_strip_numbers_at_beginning(self):
        self.assertEqual(
            attachmeta.strip_numbers_at_beginning('12. song name'), 'song name'
        )

    def test_get_the_song(self):
        data = attachmeta.get_the_song('see you again ft. Charlie Puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('see you again - charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('charlie puth - see you again')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('001. see you again ft. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('001) see you again ft. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('001 see you again ft. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('see you again feat. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('see you again by charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.get_the_song('see you again featuring charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )


if __name__ == "__main__":
    unittest.main()
