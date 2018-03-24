import setPaths
import unittest
import attachmeta

class testAttachmetaMethods(unittest.TestCase):
    def test_splitByFirstOccurence(self):
        string = "First half - Last Half"
        self.assertEqual(attachmeta.splitByFirstOccurence(string, '-'), ["First half", "Last Half"])
        string = "First half - Second Half - Last Half"
        self.assertEqual(attachmeta.splitByFirstOccurence(string, '-'), ["First half", "Second Half - Last Half"])


if __name__ == "__main__":
    unittest.main()