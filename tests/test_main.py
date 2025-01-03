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
        ]
        for filename in expected_files:
            with self.subTest(filename=filename):
                file_path = os.path.join('images', filename)
                self.assertTrue(os.path.exists(file_path), f"Graph file {filename} not found.")

if __name__ == '__main__':
    unittest.main()
