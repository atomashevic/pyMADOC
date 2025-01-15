import unittest
from unittest.mock import patch
import json
import argparse
from io import StringIO
from contextlib import redirect_stdout
from pymadoc.cli import main
from pymadoc.pymadoc import PLATFORMS, COMMUNITIES

class TestCLI(unittest.TestCase):
    @patch('sys.argv', ['pymadoc', 'list'])
    def test_list_command(self):
        """Test the list command output."""
        output = StringIO()
        with redirect_stdout(output):
            main()
        
        # Parse the JSON output
        data = json.loads(output.getvalue())
        
        # Verify the output structure
        self.assertIn("platforms", data)
        self.assertIn("communities", data)
        self.assertEqual(data["platforms"], PLATFORMS)
        self.assertEqual(data["communities"], COMMUNITIES)
    
    @patch('sys.argv', ['pymadoc', 'download', 'invalid_platform'])
    def test_invalid_platform_cli(self):
        """Test CLI error handling for invalid platform."""
        output = StringIO()
        with redirect_stdout(output):
            main()
        
        self.assertIn("Error: Platform must be one of", output.getvalue())
    
    @patch('sys.argv', ['pymadoc', 'download', 'reddit'])
    def test_missing_community_cli(self):
        """Test CLI error handling for missing community."""
        output = StringIO()
        with redirect_stdout(output):
            main()
        
        self.assertIn("Error: Community must be one of", output.getvalue())
    
    @patch('pymadoc.pymadoc.download_file')
    @patch('sys.argv', ['pymadoc', 'download', 'reddit', '--community', 'funny', '--output-dir', 'test_output'])
    def test_download_command(self, mock_download):
        """Test the download command."""
        mock_download.return_value = "reddit_funny_madoc.parquet"
        
        output = StringIO()
        with redirect_stdout(output):
            main()
        
        mock_download.assert_called_once_with(
            "reddit",
            community="funny",
            output_dir="test_output"
        )
        self.assertIn("Downloaded: reddit_funny_madoc.parquet", output.getvalue())
    
    @patch('pymadoc.pymadoc.download_community_pair')
    @patch('sys.argv', ['pymadoc', 'pair', 'funny', '--output-dir', 'test_output'])
    def test_pair_command(self, mock_pair):
        """Test the pair command."""
        mock_pair.return_value = ("reddit_funny_madoc.parquet", "voat_funny_madoc.parquet")
        
        output = StringIO()
        with redirect_stdout(output):
            main()
        
        mock_pair.assert_called_once_with(
            "funny",
            output_dir="test_output"
        )
        self.assertIn("Downloaded Reddit file:", output.getvalue())
        self.assertIn("Downloaded Voat file:", output.getvalue())
    
    @patch('sys.argv', ['pymadoc'])
    def test_no_command(self):
        """Test CLI behavior when no command is provided."""
        output = StringIO()
        with redirect_stdout(output):
            main()
        
        self.assertIn("usage:", output.getvalue().lower())
        self.assertIn("command to execute", output.getvalue().lower())

if __name__ == '__main__':
    unittest.main() 