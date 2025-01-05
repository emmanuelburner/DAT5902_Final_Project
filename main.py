# Import libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define colours for graphs
RED_COLOR = '#FF2400'
BLUE_COLOR = '#0072B2'

# Ensure directory for saving images exists
os.makedirs('images', exist_ok=True)

# Read the csv to a dataframe
df = pd.read_csv('data/LeagueofLegends.csv')

# Obtain the values for game lengths from the dataframe and sort them
gameLength = df['gamelength']
x = np.sort(gameLength)
y = np.arange(1, len(x) + 1) / len(x)

# Subplot 1:
fig, ax = plt.subplots(1, 2, figsize=(10, 10))

# Fig 1: Boxplot of game lengths
ax[0].boxplot(gameLength)
ax[0].set_title('Boxplot of Game Length')
ax[0].set_ylabel('Game Length (minutes)')

# Fig 2: ECDF of game lengths
ax[1].plot(x, y, marker='.', linestyle='none')
ax[1].set_title('Empirical CDF of Game Length')
ax[1].set_xlabel('Game Length (minutes)')
ax[1].set_ylabel('ECDF')
ax[1].axhline(0.25, color=RED_COLOR, linestyle='--', label='25th Percentile')
ax[1].axhline(0.50, color='green', linestyle='--', label='50th Percentile')
ax[1].axhline(0.75, color='orange', linestyle='--', label='75th Percentile')
ax[1].legend()

# Save subplot
plt.tight_layout()
fig.savefig('images/game_length_distribution.png')
plt.close(fig)

# Group data by region and calculate the wins for each side
region_wins = df.groupby('League', observed=False).agg(
    red_wins=('rResult', 'sum'),
    blue_wins=('bResult', 'sum')
).reset_index()

# Extract region names, red/blue wins, and calculate absolute win difference
regions = region_wins['League']
red_wins = region_wins['red_wins']
blue_wins = region_wins['blue_wins']
win_difference_abs = (red_wins - blue_wins).abs()
colors = ['blue' if diff < 0 else 'red' for diff in (red_wins - blue_wins)]

# Subplot 2:
fig, ax = plt.subplots(1, 3, figsize=(15, 15))

# Fig 1: Blue side wins per region
ax[0].bar(regions, blue_wins, color=BLUE_COLOR)
ax[0].set_title("Blue Side Wins")
ax[0].set_xlabel("Region")
ax[0].set_ylabel("Wins")
ax[0].tick_params(axis='x', rotation=90)

# Fig 2: Red side wins per region
ax[1].bar(regions, red_wins, color=RED_COLOR)
ax[1].set_title("Red Side Wins")
ax[1].set_xlabel("Region")
ax[1].set_ylabel("Wins")
ax[1].tick_params(axis='x', rotation=90)

# Fig 3: Absolute difference in wins between sides per region
ax[2].bar(regions, win_difference_abs, color=colors, alpha=0.7)
ax[2].set_title('Difference in Wins (Absolute)')
ax[2].set_xlabel('Region')
ax[2].set_ylabel('Difference in Wins')
ax[2].tick_params(axis='x', rotation=45)

# Save subplot
plt.tight_layout()
fig.savefig('images/win_comparison.png')
plt.close(fig)

# Group data by game length and calculate red/blue wins
game_length_wins = df.groupby('gamelength').agg(
    red_wins=('rResult', 'sum'),
    blue_wins=('bResult', 'sum')
).reset_index()

# Subplot 3:
fig, ax = plt.subplots(figsize=(10, 6))

# Fig 1: "Population pyramid" style graph to show red wins vs blue wins by game length
ax.barh(game_length_wins['gamelength'], -game_length_wins['red_wins'], color=RED_COLOR, label='Red Side Wins')
ax.barh(game_length_wins['gamelength'], game_length_wins['blue_wins'], color=BLUE_COLOR, label='Blue Side Wins')
ax.set_xlabel('Wins')
ax.set_ylabel('Game Length (minutes)')
ax.set_title('Red vs Blue Wins by Game Length')
ax.legend()

# Save subplot
plt.tight_layout()
fig.savefig('images/red_vs_blue_by_length.png')
plt.close(fig)

# Extract gold difference data from the 'golddiff' column
df['golddiff'] = df['golddiff'].apply(lambda x: eval(x)[-1] if isinstance(eval(x), list) else np.nan)

# Drop rows with missing golddiff
df.dropna(subset=['golddiff'], inplace=True)

# Create bins for gold difference and categorize data
golddiff_bins = np.arange(-5000, 5001, 500)
df['golddiff_bin'] = pd.cut(df['golddiff'], bins=golddiff_bins)

# Calculate win rates for each gold difference bin
win_rates = df.groupby('golddiff_bin').agg(
    win_rate_blue=('bResult', 'mean'),
    win_rate_red=('rResult', 'mean')
).reset_index()

# Subplot 4:
fig, ax = plt.subplots(figsize=(10, 6))

# Fig 1: Red win rate and blue win rate vs gold difference
ax.plot(golddiff_bins[:-1], win_rates['win_rate_blue'], color=BLUE_COLOR, marker='o', label='Blue Win Rate')
ax.plot(golddiff_bins[:-1], win_rates['win_rate_red'], color=RED_COLOR, marker='o', label='Red Win Rate')
ax.set_xlabel('Gold Difference Range')
ax.set_ylabel('Win Rate')
ax.set_title('Win Rate vs Gold Difference')
ax.legend()

# Save subplot
plt.tight_layout()
fig.savefig('images/win_rate_vs_gold_difference.png')
plt.close(fig)

# Filter data for games where blue and red teams win
df_blue_wins = df[df['bResult'] == 1]
df_red_wins = df[df['rResult'] == 1]

# Subplot 5:
fig, ax = plt.subplots(figsize=(10, 6))

# Fig 1: Histogram to show gold difference of wins
ax.hist(df_blue_wins['golddiff'], bins=50, alpha=0.7, label='Blue Wins', color=BLUE_COLOR, edgecolor='black')
ax.hist(df_red_wins['golddiff'], bins=50, alpha=0.7, label='Red Wins', color=RED_COLOR, edgecolor='black')
ax.set_xlabel('Gold Difference')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Gold Difference for Wins')
ax.legend()

# Save subplot
plt.tight_layout()
fig.savefig('images/gold_difference_histogram.png')
plt.close(fig)

# Subplot 6:
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Fig 1: Full dataset scatter plot
ax[0].scatter(df['golddiff'], df['gamelength'], 
              c=df['bResult'], cmap='coolwarm', alpha=0.7)
ax[0].set_xlabel('Gold Difference')
ax[0].set_ylabel('Game Length (minutes)')
ax[0].set_title('Gold Difference vs Game Length (Full Dataset)')
cbar = plt.colorbar(ax[0].collections[0], ax=ax[0])
cbar.set_label('Game Result (0=Red Win, 1=Blue Win)')

# Fig 2: Unexpected (Team with less gold wins) scatter plot
filtered_unexpected = df[(df['golddiff'] > 0) & (df['rResult'] == 1)]
filtered_unexpected = pd.concat([filtered_unexpected, df[(df['golddiff'] < 0) & (df['bResult'] == 1)]])
ax[1].scatter(filtered_unexpected['golddiff'], filtered_unexpected['gamelength'], 
              c=filtered_unexpected['bResult'], cmap='coolwarm', alpha=0.7)
ax[1].set_xlabel('Gold Difference')
ax[1].set_ylabel('Game Length (minutes)')
ax[1].set_title('Unexpected (Team with Less Gold Wins)')
cbar = plt.colorbar(ax[1].collections[0], ax=ax[1])
cbar.set_label('Game Result (0=Red Win, 1=Blue Win)')

# Fig 3: Expected (Team with more gold wins) scatter plot
filtered_expected = df[(df['golddiff'] > 0) & (df['bResult'] == 1)]
filtered_expected = pd.concat([filtered_expected, df[(df['golddiff'] < 0) & (df['rResult'] == 1)]])
ax[2].scatter(filtered_expected['golddiff'], filtered_expected['gamelength'], 
              c=filtered_expected['bResult'], cmap='coolwarm', alpha=0.7)
ax[2].set_xlabel('Gold Difference')
ax[2].set_ylabel('Game Length (minutes)')
ax[2].set_title('Expected (Team with More Gold Wins)')
cbar = plt.colorbar(ax[2].collections[0], ax=ax[2])
cbar.set_label('Game Result (0=Red Win, 1=Blue Win)')

# Save subplot
plt.tight_layout()
fig.savefig('images/scatter_gold_difference.png')
plt.close(fig)
