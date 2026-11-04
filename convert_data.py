import pandas as pd
import json

print("--- STARTING CONVERSION ---")

# 1. Load Data
try:
    df = pd.read_csv('media_diet_data26.csv')
    print(f"Loaded CSV. Found {len(df)} rows.")
    print(f"Raw Headers: {list(df.columns)}")
except Exception as e:
    print(f"ERROR: {e}")
    exit()

# 2. RENAME (The Critical Step)
# We map YOUR headers (left) to the WEBSITE keys (right)
# If your header is "all", we must rename it to "overall" because chart.js looks for d.overall
rename_map = {
    'all': 'overall',       
    'men': 'male',          
    'women': 'female',      
    'democrat': 'dem',      
    'republican': 'rep',    
    'age18': 'age18',
    'age30': 'age30',
    'age50': 'age50',
    'age65': 'age65',
    'source': 'source'
}

# Check if keys exist before renaming to avoid silent failures
for csv_key, js_key in rename_map.items():
    if csv_key not in df.columns:
        print(f"WARNING: Could not find column '{csv_key}' in CSV. The website might break for '{js_key}'.")

df = df.rename(columns=rename_map)

# 3. FORCE NUMBERS (Integer Fix)
# We ensure the columns are numbers, not text
data_cols = ['overall', 'male', 'female', 'dem', 'rep', 'age18', 'age30', 'age50', 'age65']

for col in data_cols:
    if col in df.columns:
        # Remove any non-numeric junk
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 4. EXPORT
df.to_json('data.json', orient='records', indent=2)
print("--- SUCCESS! Data exported to data.json ---")
