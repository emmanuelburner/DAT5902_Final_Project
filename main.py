import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Change base pandas settings to view all rows and cols when using .head()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the csv 
df = pd.read_csv(r'data/LeagueofLegends.zip')
print(df.head(1)) # Check the dataframe is correct
