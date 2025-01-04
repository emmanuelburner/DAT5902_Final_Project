import os
import unittest
import pandas as pd

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

if __name__ == '__main__':
    unittest.main()
