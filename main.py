import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define red and blue colors
RED_COLOR = '#FF2400'
BLUE_COLOR = '#0072B2'

# Ensure images folder exists
os.makedirs('images', exist_ok=True)

# Load the dataset
df = pd.read_csv('data/LeagueofLegends.csv')

# Plot 1: Distribution of Game Lengths (Boxplot and ECDF)
gameLength = df['gamelength']
x = np.sort(gameLength)
y = np.arange(1, len(x) + 1) / len(x)

fig, ax = plt.subplots(1, 2, figsize=(10, 10))
ax[0].boxplot(gameLength)
ax[0].set_title('Boxplot of Game Length')
ax[0].set_ylabel('Game Length (minutes)')

ax[1].plot(x, y, marker='.', linestyle='none')
ax[1].set_title('Empirical CDF of Game Length')
ax[1].set_xlabel('Game Length (minutes)')
ax[1].set_ylabel('ECDF')
ax[1].axhline(0.25, color=RED_COLOR, linestyle='--', label='25th Percentile')
ax[1].axhline(0.50, color='green', linestyle='--', label='50th Percentile')
ax[1].axhline(0.75, color='orange', linestyle='--', label='75th Percentile')
ax[1].legend()
plt.tight_layout()
fig.savefig('images/game_length_distribution.png')
plt.close(fig)

# Plot 2: Red vs Blue Wins Per Region
region_wins = df.groupby('League', observed=False).agg(
    red_wins=('rResult', 'sum'),
    blue_wins=('bResult', 'sum')
).reset_index()

regions = region_wins['League']
red_wins = region_wins['red_wins']
blue_wins = region_wins['blue_wins']
win_difference_abs = (red_wins - blue_wins).abs()
colors = ['blue' if diff < 0 else 'red' for diff in (red_wins - blue_wins)]

fig, ax = plt.subplots(1, 3, figsize=(15, 15))
ax[0].bar(regions, blue_wins, color=BLUE_COLOR)
ax[0].set_title("Blue Side Wins")
ax[0].set_xlabel("Region")
ax[0].set_ylabel("Wins")
ax[0].tick_params(axis='x', rotation=90)

ax[1].bar(regions, red_wins, color=RED_COLOR)
ax[1].set_title("Red Side Wins")
ax[1].set_xlabel("Region")
ax[1].set_ylabel("Wins")
ax[1].tick_params(axis='x', rotation=90)

ax[2].bar(regions, win_difference_abs, color=colors, alpha=0.7)
ax[2].set_title('Difference in Wins (Absolute)')
ax[2].set_xlabel('Region')
ax[2].set_ylabel('Difference in Wins')
ax[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
fig.savefig('images/win_comparison.png')
plt.close(fig)

# Plot 3: Population Pyramid for Red vs Blue Wins by Game Length
game_length_wins = df.groupby('gamelength').agg(
    red_wins=('rResult', 'sum'),
    blue_wins=('bResult', 'sum')
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(game_length_wins['gamelength'], -game_length_wins['red_wins'], color=RED_COLOR, label='Red Side Wins')
ax.barh(game_length_wins['gamelength'], game_length_wins['blue_wins'], color=BLUE_COLOR, label='Blue Side Wins')
ax.set_xlabel('Wins')
ax.set_ylabel('Game Length (minutes)')
ax.set_title('Red vs Blue Wins by Game Length')
ax.legend()
plt.tight_layout()
fig.savefig('images/red_vs_blue_by_length.png')
plt.close(fig)

# Plot 4: Win Rate Based on Gold Difference Thresholds
# Extract the final gold difference (last value in the 'golddiff' list)
df['golddiff'] = df['golddiff'].apply(lambda x: ast.literal_eval(x)[-1] if isinstance(ast.literal_eval(x), list) else np.nan)

# Drop rows with NaN values in 'golddiff' column
df.dropna(subset=['golddiff'], inplace=True)

# Group the data by golddiff ranges and calculate win rates for each range
golddiff_bins = np.arange(-5000, 5001, 500)  # Adjust the range of bins as needed
df['golddiff_bin'] = pd.cut(df['golddiff'], bins=golddiff_bins)

# Calculate win rate for each gold difference range
win_rates = df.groupby('golddiff_bin').agg(
    win_rate_blue=('bResult', 'mean'),  # Blue win rate
    win_rate_red=('rResult', 'mean')    # Red win rate
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

# Plot win rate vs gold difference bin for both blue and red
ax.plot(golddiff_bins[:-1], win_rates['win_rate_blue'], color=BLUE_COLOR, marker='o', label='Blue Win Rate')
ax.plot(golddiff_bins[:-1], win_rates['win_rate_red'], color=RED_COLOR, marker='o', label='Red Win Rate')

ax.set_xlabel('Gold Difference Range')
ax.set_ylabel('Win Rate')
ax.set_title('Win Rate vs Gold Difference')
ax.legend()
plt.tight_layout()
fig.savefig('images/win_rate_vs_gold_difference.png')
plt.close(fig)

# Plot 5: Histogram of Gold Difference for Wins and Losses
# Separate the data for wins and losses
df_blue_wins = df[df['bResult'] == 1]  # Blue wins
df_red_wins = df[df['rResult'] == 1]   # Red wins

# Plotting histogram for gold difference in blue and red wins
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the histogram for blue wins and red wins
ax.hist(df_blue_wins['golddiff'], bins=50, alpha=0.7, label='Blue Wins', color=BLUE_COLOR, edgecolor='black')
ax.hist(df_red_wins['golddiff'], bins=50, alpha=0.7, label='Red Wins', color=RED_COLOR, edgecolor='black')

ax.set_xlabel('Gold Difference')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Gold Difference for Wins')
ax.legend()

plt.tight_layout()
fig.savefig('images/gold_difference_histogram.png')
plt.close(fig)
