import setPaths
import unittest
import attachmeta


class testAttachmetaMethods(unittest.TestCase):
    def test_splitByFirstOccurence(self):
        string = "First half - Last Half"
        self.assertEqual(
            attachmeta.splitByFirstOccurence(string, '-'),
            ["First half", "Last Half"]
        )
        string = "First half - Second Half - Last Half"
        self.assertEqual(
            attachmeta.splitByFirstOccurence(string, '-'),
            ["First half", "Second Half - Last Half"]
        )

    def test_getSongName(self):
        self.assertEqual(
            attachmeta.getSongName('Source Code ft. Developers'),
            'Source Code'
        )

    def test_getArtists(self):
        self.assertEqual(
            attachmeta.getArtists('artist1 & artist2'),
            ['artist1', 'artist2']
        )
        self.assertEqual(
            attachmeta.getArtists(
                'artist1 & artist2 ft. artist3',
                featuring=1
            ),
            ['artist1', 'artist2', 'artist3']
        )
        self.assertIsNone(
            attachmeta.getArtists('artist1 & artist2', featuring=1)
        )

    def test_getData(self):
        self.assertEqual(
            attachmeta.getData('see you again', ['wiz khalifa'])["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )
        self.assertIsNone(
            attachmeta.getData('some random song', ['artist1', 'artist2'])
        )

    def test_stripNumbersAtBeginning(self):
        self.assertEqual(
            attachmeta.stripNumbersAtBeginning('12. song name'), 'song name'
        )

    def test_getTheSong(self):
        data = attachmeta.getTheSong('see you again ft. Charlie Puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('see you again - charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('charlie puth - see you again')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('001. see you again ft. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('001) see you again ft. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('001 see you again ft. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('see you again feat. charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('see you again by charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )

        data = attachmeta.getTheSong('see you again featuring charlie puth')
        self.assertEqual(
            data["Track Name"],
            'See You Again (feat. Charlie Puth)'
        )


if __name__ == "__main__":
    unittest.main()
