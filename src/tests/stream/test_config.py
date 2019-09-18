import unittest
from stream import config


class TestStreamConfigImport(unittest.TestCase):

    def test_import_config(self):
        self.assertEqual(config.TWITTER, config.TWITTER)


if __name__ == "__main__":
    unittest.main()
