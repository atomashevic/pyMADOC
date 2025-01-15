import os
import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from pymadoc.pymadoc import list_available_data, download_file, download_community_pair

class TestPyMADOC(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_dir = "test_output"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test directory and its contents
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)
    
    def test_list_available_data(self):
        """Test listing available platforms and communities."""
        data = list_available_data()
        
        self.assertIn("platforms", data)
        self.assertIn("communities", data)
        self.assertIsInstance(data["platforms"], list)
        self.assertIsInstance(data["communities"], list)
        self.assertIn("reddit", data["platforms"])
        self.assertIn("funny", data["communities"])
    
    def test_invalid_platform(self):
        """Test error handling for invalid platform."""
        with self.assertRaises(ValueError):
            download_file("invalid_platform")
    
    def test_invalid_community(self):
        """Test error handling for invalid community."""
        with self.assertRaises(ValueError):
            download_file("reddit", community="invalid_community")
    
    @patch('pymadoc.pymadoc.zenodo_get')
    @patch('pandas.read_parquet')
    @patch('os.remove')
    def test_download_file_as_dataframe(self, mock_remove, mock_read_parquet, mock_zenodo_get):
        """Test downloading file as DataFrame."""
        # Mock the DataFrame that would be returned
        mock_df = pd.DataFrame({'column': [1, 2, 3]})
        mock_read_parquet.return_value = mock_df
        
        # Test downloading Reddit file
        df = download_file("reddit", community="funny", as_dataframe=True)
        self.assertIsInstance(df, pd.DataFrame)
        mock_zenodo_get.assert_called_once()
        mock_remove.assert_called_once_with("reddit_funny_madoc.parquet")
        
        # Reset mocks
        mock_zenodo_get.reset_mock()
        mock_read_parquet.reset_mock()
        mock_remove.reset_mock()
        
        # Test downloading Bluesky file
        df = download_file("bluesky", as_dataframe=True)
        self.assertIsInstance(df, pd.DataFrame)
        mock_zenodo_get.assert_called_once()
        mock_remove.assert_called_once_with("bluesky_madoc.parquet")
    
    @patch('pymadoc.pymadoc.zenodo_get')
    @patch('os.rename')
    def test_download_file_to_disk(self, mock_rename, mock_zenodo_get):
        """Test downloading file to disk."""
        filename = download_file("bluesky", output_dir=self.test_dir)
        self.assertEqual(filename, "bluesky_madoc.parquet")
        mock_zenodo_get.assert_called_once()
        mock_rename.assert_called_once_with(
            "bluesky_madoc.parquet",
            os.path.join(self.test_dir, "bluesky_madoc.parquet")
        )
    
    @patch('pymadoc.pymadoc.download_file')
    def test_download_community_pair(self, mock_download_file):
        """Test downloading community pair."""
        # Mock the DataFrame that would be returned
        mock_reddit_df = pd.DataFrame({'platform': ['reddit'] * 3})
        mock_voat_df = pd.DataFrame({'platform': ['voat'] * 2})
        mock_download_file.side_effect = [mock_reddit_df, mock_voat_df]
        
        # Test downloading as DataFrame
        df = download_community_pair("funny", as_dataframe=True)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)  # Combined length of mock DataFrames

if __name__ == '__main__':
    unittest.main() 