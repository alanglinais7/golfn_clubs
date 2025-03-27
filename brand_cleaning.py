import pandas as pd

# Read the CSV file
df = pd.read_csv('golfn-app-brands.csv')

# List of suffixes to remove
suffixes = [' Ltd.', ' Ltd', ' Co', ' Inc.', ' Inc', ' LLC.', ' LLC']

# Store original names to compare later
original_names = df['Brand Name'].copy()

# Remove suffixes from Brand Name
for suffix in suffixes:
    df['Brand Name'] = df['Brand Name'].str.replace(suffix, '', regex=False)

# Remove commas and periods
df['Brand Name'] = df['Brand Name'].str.replace(',', '', regex=False)
df['Brand Name'] = df['Brand Name'].str.replace('.', '', regex=False)

# Set Updated to TRUE where names changed
df['Updated'] = df['Brand Name'] != original_names

# Save the modified dataframe back to CSV
df.to_csv('golfn-app-brands.csv', index=False)