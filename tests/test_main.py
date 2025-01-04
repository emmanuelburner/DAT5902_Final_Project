import os
import unittest
import pandas as pd
import numpy as np  # Import numpy

class TestMain(unittest.TestCase):

    def test_dataset_load(self):
        """Test if the dataset loads correctly."""
        try:
            df = pd.read_csv('data/LeagueofLegends.csv')
            self.assertFalse(df.empty, "Dataset is empty.")
        except Exception as e:
            self.fail(f"Dataset failed to load: {e}")

    def test_images_folder_exists(self):
        """Test if the images folder exists."""
        self.assertTrue(os.path.exists('images'), "Images folder does not exist.")

    def test_graphs_generated(self):
        """Test if graph files are generated."""
        expected_files = [
            "game_length_distribution.png",
            "win_comparison.png",
            "red_vs_blue_by_length.png",
            "win_rate_vs_gold_difference.png",  # New test for this plot
        ]
        for filename in expected_files:
            with self.subTest(filename=filename):
                file_path = os.path.join('images', filename)
                self.assertTrue(os.path.exists(file_path), f"Graph file {filename} not found.")

    def test_gold_diff_processing(self):
        """Test if gold difference is processed correctly."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        
        # Apply the same processing steps as in main.py
        df['golddiff'] = df['golddiff'].apply(lambda x: eval(x)[-1] if isinstance(eval(x), list) else None)
        df.dropna(subset=['golddiff'], inplace=True)
        
        # Check if 'golddiff' has been processed correctly (e.g., no NaN or empty values)
        self.assertTrue(df['golddiff'].notna().all(), "'golddiff' contains NaN values after processing.")
        self.assertTrue(df['golddiff'].apply(lambda x: isinstance(x, (int, float))).all(), "'golddiff' contains invalid types.")
    
    def test_missing_columns(self):
        """Test if the required columns are present in the dataset."""
        required_columns = ['gamelength', 'golddiff', 'bResult', 'rResult', 'League']
        df = pd.read_csv('data/LeagueofLegends.csv')
        for column in required_columns:
            with self.subTest(column=column):
                self.assertIn(column, df.columns, f"Column {column} is missing from the dataset.")

    def test_no_duplicate_entries(self):
        """Test if there are any duplicate entries in the dataset."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        
        # Check for duplicate rows based on key columns
        key_columns = ['gamelength', 'golddiff', 'bResult', 'rResult']
        duplicates = df[df.duplicated(subset=key_columns, keep=False)]
        
        # Assert that there are no duplicates
        self.assertTrue(duplicates.empty, f"Found duplicate entries:\n{duplicates}")

if __name__ == '__main__':
    unittest.main()
