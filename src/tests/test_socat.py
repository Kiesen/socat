import unittest
import socat


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = socat.create_parser()

    def test_stream(self):
        parsed_all = self.parser.parse_args([
            'stream',
            'tweets',
            '-m',
            '100',
            '-l',
            '-p',
            '/mocked/path',
            '-v'
        ])
        self.assertEqual(parsed_all.log, True)
        self.assertEqual(parsed_all.maximum, 100)
        self.assertEqual(parsed_all.verbose, True)
        self.assertEqual(parsed_all.mode, 'stream')
        self.assertEqual(parsed_all.tweets, 'tweets')
        self.assertEqual(parsed_all.path, '/mocked/path')

        parsed_required = self.parser.parse_args([
            'stream',
            'tweets',
        ])
        self.assertEqual(parsed_required.log, False)
        self.assertEqual(parsed_required.path, None)
        self.assertEqual(parsed_required.maximum, 100)
        self.assertEqual(parsed_required.verbose, False)
        self.assertEqual(parsed_required.mode, 'stream')
        self.assertEqual(parsed_required.tweets, 'tweets')

    def test_analyze(self):
        parsed_text = self.parser.parse_args([
            'analyze',
            '-p',
            '/mocked/path',
            'text',
            '-lang',
            'de',
            '-m'
            'KM',

        ])
        self.assertEqual(parsed_text.source, 'text')
        self.assertEqual(parsed_text.mode, 'analyze')
        self.assertEqual(parsed_text.path, '/mocked/path')
        self.assertEqual(parsed_text.methode, 'KM')
        self.assertEqual(parsed_text.language, 'de')

        parsed_required = self.parser.parse_args([
            'analyze',
            '-p',
            '/mocked/path',
            'logs',
        ])
        self.assertEqual(parsed_required.source, 'logs')
        self.assertEqual(parsed_required.mode, 'analyze')
        self.assertEqual(parsed_required.path, '/mocked/path')


if __name__ == "__main__":
    unittest.main()
