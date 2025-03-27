import pandas as pd
import re

# Read the Excel file
df = pd.read_excel('golfn_clubs_updated.xlsx')

# Function to extract year from URL
def extract_year(url):
    if pd.isna(url):
        return None
    
    # Skip external URLs (not from usga.org)
    if 'usga.org' not in str(url):
        return None
        
    # Look for all patterns:
    # 1. R2018-0706.jpg format
    # 2. 20220430.jpg format
    # 3. R2009-0460a.jpg format (with letter suffix)
    # 4. 2003417.jpg format (just numbers)
    # Using case-insensitive flag (?i) to match .jpg, .JPG, etc.
    match = re.search(r'(?:R(\d{4})-\d+[a-zA-Z]?\.(?:jpg|JPG)|(\d{4})\d{4}\.(?:jpg|JPG)|(\d{4})\d+\.(?:jpg|JPG))', str(url), re.IGNORECASE)
    if match:
        # Return the first non-None group (any of the formats)
        return int(next(g for g in match.groups() if g is not None))
    return None

# Create new column with extracted years
df['club_year'] = df['club_image'].apply(extract_year)

# Save the updated DataFrame back to Excel
df.to_excel('golfn_clubs_updated.xlsx', index=False)

print("Successfully added club_year column to the Excel file!") 