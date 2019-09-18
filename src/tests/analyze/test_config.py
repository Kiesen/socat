import unittest
from analyze import config


class TestStreamConfigImport(unittest.TestCase):

    def test_import_config(self):
        self.assertEqual(config.KMEANS_CONF, config.KMEANS_CONF)
        self.assertEqual(config.PLOT_CONF, config.PLOT_CONF)
        self.assertEqual(config.LDA_CONF, config.LDA_CONF)
        self.assertEqual(config.TF_CONF, config.TF_CONF)


if __name__ == "__main__":
    unittest.main()
