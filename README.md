# League of Legends Data Analysis

This project analyzes match statistics from League of Legends to explore the relationship between game length, gold difference, and win rates for both the red and blue teams. The analysis includes the generation of various graphs and charts to visualize trends and results.

## Project Structure

- `config.yml`: CircleCI configuration file for automating the setup, testing, and execution of the Python script.
- `data/`: Folder containing the dataset (CSV file) with match statistics.
- `images/`: Folder where the generated images (graphs and charts) will be saved.
- `main.py`: Python script to read the dataset, process the data, and generate graphs.
- `test_main.py`: Unit tests to ensure data integrity, graph generation, and correct functionality of the code.

## Dependencies

The project requires the following Python packages:

- `numpy`
- `pandas`
- `matplotlib`

These packages are installed during the CircleCI setup step using a virtual environment.

## Setup and Testing with CircleCI

### Configuration

The project is configured to run automatically using CircleCI. The `.circleci/config.yml` file defines a job to:

1. Set up a Python virtual environment.
2. Install dependencies.
3. Run the `main.py` script to generate graphs.
4. Ensure that the `images/` folder contains the generated graphs.
5. Run unit tests to check the integrity of the dataset and correctness of the script.

### CircleCI Workflow

The CircleCI configuration file specifies the `setup_and_test` job to execute in the workflow, which includes the following steps:
1. Checkout the project files.
2. Install Python dependencies (`numpy`, `pandas`, `matplotlib`).
3. Run the main script (`main.py`) to generate graphs.
4. Verify that the images are generated successfully.
5. Run unit tests from `test_main.py`.

## Dataset

The dataset (`data/LeagueofLegends.csv`) includes match statistics with columns such as:
- `gamelength`: Length of the game in minutes.
- `golddiff`: Gold difference between the two teams.
- `bResult`: Result of the blue team (1 = win, 0 = loss).
- `rResult`: Result of the red team (1 = win, 0 = loss).
- `League`: The region/league the match took place in.

## Generated Graphs

The script generates the following graphs:

1. **Game Length Distribution**:
   - Boxplot and Empirical CDF (ECDF) of game lengths.
   
2. **Win Comparison by Region**:
   - Bar charts comparing the number of wins for blue and red teams across regions, with an additional chart showing the absolute difference in wins.

3. **Red vs Blue by Game Length**:
   - A horizontal bar chart showing the number of red and blue wins grouped by game length.

4. **Win Rate vs Gold Difference**:
   - A line plot comparing the win rates for blue and red teams across different gold difference bins.

5. **Gold Difference Histogram for Wins**:
   - A histogram showing the distribution of gold difference for games won by blue and red teams.

6. **Gold Difference vs Game Length (Scatter Plot)**:
   - Scatter plots showing the relationship between gold difference and game length, categorized by win type (unexpected and expected results).

## Unit Tests

The project includes unit tests in `test_main.py` to verify the following:

- Dataset loads correctly and is not empty.
- The `images/` folder exists and contains the expected graph files.
- Gold difference processing is correct and free of missing values.
- The dataset contains all required columns and has no duplicate entries.

### Running Tests Locally

To run the tests locally, you can set up the environment and run the tests as follows:

1. Install dependencies:

   ```bash
   python -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt
