import pandas as pd
import numpy as np

# 1. SETUP
# Updated to look for your new file
input_filename = 'media_diet_diff26.csv'

try:
    df = pd.read_csv(input_filename)
    print(f"Loaded {input_filename}. Columns found: {list(df.columns)}")
except FileNotFoundError:
    print(f"ERROR: Could not find '{input_filename}'")
    exit()

# 2. RENAME COLUMNS
# Left side = Likely CSV Headers | Right side = Code Keys
rename_map = {
    'source': 'source',
    'all': 'overall',
    'dem': 'dem',
    'rep': 'rep',
    'age18': 'age18',
    'age30': 'age30', 
    'age50': 'age50',
    'age65': 'age65',
}

# 3. NORMALIZE HEADERS
# This loop looks for matches regardless of capitalization or extra spaces
actual_rename = {}
for col in df.columns:
    col_lower = col.lower().strip() 
    for key, val in rename_map.items():
        # Check if the CSV header contains the key string (e.g. "age 30" inside "Age 30-49")
        if key in col_lower:
            actual_rename[col] = val

df = df.rename(columns=actual_rename)

# 4. CLEAN DATA
# Ensure columns are numbers. We expect positive/negative values.
numeric_cols = ['overall', 'dem', 'rep', 'age18', 'age30', 'age50', 'age65']

for col in numeric_cols:
    if col in df.columns:
        # If text, remove % and convert
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace('%', '').astype(float)
        
        # Fill NaNs with 0
        df[col] = df[col].fillna(0)
    else:
        print(f"WARNING: Column '{col}' not found in CSV. Chart buttons for this group won't work.")

# 5. EXPORT
df.to_json('data2.json', orient='records', indent=2) 
print("Success! Created 'data2.json' (Chart 2) from 'media_diet_diff.csv'.")
