import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define red and blue colors
RED_COLOR = '#FF2400'
BLUE_COLOR = '#0072B2'
# Load the dataset
df = pd.read_csv(r'data/LeagueofLegends.zip')


""" 
Plot 2 graphs to show the distribution of game lengths:
    - Boxplot: Displays the spread and outliers of game lengths.
    - Empirical CDF (ECDF): Shows the cumulative distribution of game lengths.
"""

gameLength = df['gamelength']

# Compute ECDF values
x = np.sort(gameLength)
y = np.arange(1, len(x) + 1) / len(x)

fig, ax = plt.subplots(1, 2, figsize=(10, 10))

# Boxplot of game lengths
ax[0].boxplot(gameLength)
ax[0].set_title('Boxplot of Game Length')
ax[0].set_ylabel('Game Length (minutes)')

# ECDF plot with percentile lines
ax[1].plot(x, y, marker='.', linestyle='none')
ax[1].set_title('Empirical CDF of Game Length')
ax[1].set_xlabel('Game Length (minutes)')
ax[1].set_ylabel('ECDF')
ax[1].axhline(0.25, color=RED_COLOR, linestyle='--', label='25th Percentile')
ax[1].axhline(0.50, color='green', linestyle='--', label='50th Percentile')
ax[1].axhline(0.75, color='orange', linestyle='--', label='75th Percentile')
ax[1].legend()


""" 
Plot 3 graphs to compare red side vs blue side wins per region:
    - Bar Graph 1: Blue side wins per region.
    - Bar Graph 2: Red side wins per region.
    - Bar Graph 3: Absolute difference in wins between red and blue side.
"""

# Compute wins per side per region
region_wins = (
    df.groupby('League')
    .agg(
        red_wins=('rResult', 'sum'),
        blue_wins=('bResult', 'sum')
    )
    .reset_index()
)
region_wins['win_difference'] = region_wins['red_wins'] - region_wins['blue_wins']

# Extract necessary data for plotting
regions = region_wins['League']
red_wins = region_wins['red_wins']
blue_wins = region_wins['blue_wins']

# Assign colors dynamically based on win difference
colors = ['blue' if diff < 0 else 'red' for diff in region_wins['win_difference']]

# Convert differences to absolute values
win_difference_abs = region_wins['win_difference'].abs()

# Create 3 subplots for the win comparisons
fig, ax = plt.subplots(1, 3, figsize=(15, 15))

# Blue side wins plot
ax[0].bar(regions, blue_wins, color=BLUE_COLOR)
ax[0].set_title("Blue Side Wins")
ax[0].set_xlabel("Region")
ax[0].set_ylabel("Wins")
ax[0].tick_params(axis='x', rotation=90)

# Red side wins plot
ax[1].bar(regions, red_wins, color=RED_COLOR)
ax[1].set_title("Red Side Wins")
ax[1].set_xlabel("Region")
ax[1].set_ylabel("Wins")
ax[1].tick_params(axis='x', rotation=90)

# Difference in wins plot with dynamic coloring
ax[2].bar(regions, win_difference_abs, color=colors, alpha=0.7)
ax[2].set_title('Difference in Wins (Absolute)')
ax[2].set_xlabel('Region')
ax[2].set_ylabel('Difference in Wins')
ax[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()


""" 
Plot a population pyramid-like graph showing red side vs blue side wins by game length.
    - Individual game lengths (minutes) on the x-axis.
    - Red side wins are negative, blue side wins are positive.
"""

# Count red and blue wins for each game length
game_length_wins = (
    df.groupby('gamelength')
    .agg(
        red_wins=('rResult', 'sum'),
        blue_wins=('bResult', 'sum')
    )
    .reset_index()
)

# Plot the population pyramid-like graph
fig, ax = plt.subplots(figsize=(10, 6))

# Plot red side wins as negative values (left side of the pyramid)
ax.barh(game_length_wins['gamelength'], -game_length_wins['red_wins'], color=RED_COLOR, label='Red Side Wins')

# Plot blue side wins as positive values (right side of the pyramid)
ax.barh(game_length_wins['gamelength'], game_length_wins['blue_wins'], color=BLUE_COLOR, label='Blue Side Wins')

# Labels and title
ax.set_xlabel('Wins')
ax.set_ylabel('Game Length (minutes)')
ax.set_title('Red vs Blue Wins by Game Length')

# Display legend
ax.legend()

plt.tight_layout()
plt.show()
