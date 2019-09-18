import io
import os
import unittest
from unittest.mock import patch, mock_open
from stream import utils


class TestStreamUtils(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_initial_info(self, mock_stdout):
        cwd = os.getcwd()
        utils.print_initial_info(cwd)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "Start streaming social media entries\n" +
            "----------------------------------------------------\n" +
            "\nRecived entries getting written to: %s"
            % cwd
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_summary(self, mock_stdout):
        utils.print_summary("0:00:00", 1337)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "Total runtime: %s\nTotal amount of entries: %d"
            % ("0:00:00", 1337)
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_info(self, mock_stdout):
        utils.print_info(1337)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            "Entries recieved: %d"
            % 1337
        )

    @patch('stream.utils.os.path.exists')
    def test_set_output_path_with_existing_path(self, mock_exists):
        cwd = os.getcwd()
        rel_dir_path = '/mock_dir'
        utils.set_output_path(cwd, rel_dir_path)
        mock_exists.assert_called_with(cwd + rel_dir_path)

    @patch('stream.utils.os.makedirs')
    def test_set_output_path_with_no_path(self, mock_makedir):
        rel_dir_path = '/mock_dir'
        utils.set_output_path(None, rel_dir_path)
        mock_makedir.assert_called_with('.' + rel_dir_path)

    @patch("json.dumps")
    @patch("builtins.open", new_callable=mock_open)
    def test_data_to_json(self, mock_file, json_dumps_mock):
        cwd = os.getcwd()
        utils.data_to_json(
            path=cwd,
            json_data="{ \"x\": \"1:33:27\", \"y\": {\"z\": \"1337\"}}"
        )
        mock_file.assert_called_with(cwd, 'w')
        json_dumps_mock.assert_called_once_with(
            '{ "x": "1:33:27", "y": {"z": "1337"}}'
        )

    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_data_from_json(self, mock_file, json_load_mock):
        cwd = os.getcwd()
        utils.data_from_json(cwd)
        mock_file.assert_called_with(cwd)
        self.assertTrue(json_load_mock.called)

if __name__ == "__main__":
    unittest.main()
