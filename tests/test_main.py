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
            "win_rate_vs_gold_difference.png",
            "gold_difference_histogram.png",
            "scatter_gold_difference.png",
        ]
        for filename in expected_files:
            with self.subTest(filename=filename):
                file_path = os.path.join('images', filename)
                self.assertTrue(os.path.exists(file_path), f"Graph file {filename} not found.")

    def test_gold_diff_processing(self):
        """Test if gold difference is processed correctly."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        
        df['golddiff'] = df['golddiff'].apply(lambda x: eval(x)[-1] if isinstance(eval(x), list) else None)
        df.dropna(subset=['golddiff'], inplace=True)
        

        self.assertTrue(df['golddiff'].notna().all(), "'golddiff' contains NaN values after processing.")
        self.assertTrue(df['golddiff'].apply(lambda x: isinstance(x, (int, float))).all(), "'golddiff' contains invalid types.")

    def test_groupby_league(self):
        """Test if data is grouped by 'League' correctly."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        region_wins = df.groupby('League', observed=False).agg(
            red_wins=('rResult', 'sum'),
            blue_wins=('bResult', 'sum')
        ).reset_index()
        
        self.assertFalse(region_wins.empty, "Grouping by 'League' resulted in empty dataframe.")
        self.assertIn('League', region_wins.columns, "'League' column not found after groupby.")
        self.assertIn('red_wins', region_wins.columns, "'red_wins' column not found after aggregation.")
        self.assertIn('blue_wins', region_wins.columns, "'blue_wins' column not found after aggregation.")

    def test_groupby_gamelength(self):
        """Test if data is grouped by 'gamelength' correctly."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        game_length_wins = df.groupby('gamelength').agg(
            red_wins=('rResult', 'sum'),
            blue_wins=('bResult', 'sum')
        ).reset_index()

        self.assertFalse(game_length_wins.empty, "Grouping by 'gamelength' resulted in empty dataframe.")
        self.assertIn('gamelength', game_length_wins.columns, "'gamelength' column not found after groupby.")
        self.assertIn('red_wins', game_length_wins.columns, "'red_wins' column not found after aggregation.")
        self.assertIn('blue_wins', game_length_wins.columns, "'blue_wins' column not found after aggregation.")

    def test_no_missing_values_in_dataframe(self):
        """Test if there are any missing values in the dataframe."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        self.assertFalse(df.isnull().values.any(), "Dataset contains missing values.")

    def test_column_names(self):
        """Test if the dataset has the correct column names."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        expected_columns = ['gamelength', 'bResult', 'rResult', 'League', 'golddiff']
        for column in expected_columns:
            self.assertIn(column, df.columns, f"Column '{column}' not found in dataset.")

    def test_check_data_types(self):
        """Test if the dataset columns have the correct data types."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        self.assertEqual(df['gamelength'].dtype, 'float64', "'gamelength' has incorrect data type.")
        self.assertEqual(df['bResult'].dtype, 'int64', "'bResult' has incorrect data type.")
        self.assertEqual(df['rResult'].dtype, 'int64', "'rResult' has incorrect data type.")
        self.assertEqual(df['League'].dtype, 'object', "'League' has incorrect data type.")
        self.assertEqual(df['golddiff'].dtype, 'float64', "'golddiff' has incorrect data type.")

    def test_correct_gold_difference_bins(self):
        """Test if the gold difference bins are correctly applied."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        golddiff_bins = np.arange(-5000, 5001, 500)
        df['golddiff_bin'] = pd.cut(df['golddiff'], bins=golddiff_bins)
        self.assertTrue(df['golddiff_bin'].notna().all(), "'golddiff_bin' contains NaN values.")
        self.assertTrue(all(df['golddiff_bin'].apply(lambda x: x.left >= -5000 and x.right <= 5000)), 
                        "'golddiff_bin' values are outside the expected range.")

    def test_aggregate_win_rate_by_gold_diff(self):
        """Test if win rate is correctly aggregated by gold difference."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        golddiff_bins = np.arange(-5000, 5001, 500)
        df['golddiff_bin'] = pd.cut(df['golddiff'], bins=golddiff_bins)
        win_rates = df.groupby('golddiff_bin').agg(
            win_rate_blue=('bResult', 'mean'),
            win_rate_red=('rResult', 'mean')
        ).reset_index()

        self.assertFalse(win_rates.empty, "Win rates are empty after aggregation by gold difference.")
        self.assertIn('win_rate_blue', win_rates.columns, "'win_rate_blue' column not found in win rates dataframe.")
        self.assertIn('win_rate_red', win_rates.columns, "'win_rate_red' column not found in win rates dataframe.")

    def test_color_assignment_for_win_difference(self):
        """Test if colors are assigned correctly for the win difference plot."""
        df = pd.read_csv('data/LeagueofLegends.csv')
        region_wins = df.groupby('League', observed=False).agg(
            red_wins=('rResult', 'sum'),
            blue_wins=('bResult', 'sum')
        ).reset_index()
        
        red_wins = region_wins['red_wins']
        blue_wins = region_wins['blue_wins']
        win_difference_abs = (red_wins - blue_wins).abs()
        colors = ['blue' if diff < 0 else 'red' for diff in (red_wins - blue_wins)]
        
        self.assertTrue(all(c in ['blue', 'red'] for c in colors), "Invalid colors assigned in win difference plot.")

if __name__ == '__main__':
    unittest.main()
