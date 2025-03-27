import pandas as pd
import re

# Read the Excel file
df = pd.read_excel('golfn_clubs_updated.xlsx')

# Store original club names to check what changed
original_names = df['clubname'].copy()

# Remove parentheses and their contents
df['clubname'] = df['clubname'].str.replace(r'\s*\([^)]*\)', '', regex=True)

# Mark rows as updated where the club name changed
df.loc[df['clubname'] != original_names, 'Updated'] = True

# Remove duplicates based on clubname, keeping the first occurrence
df = df.drop_duplicates(subset=['clubname'], keep='first')

# Save the updated dataframe back to Excel
df.to_excel('golfn_clubs_updated.xlsx', index=False)