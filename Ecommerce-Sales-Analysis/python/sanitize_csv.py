import pandas as pd
import numpy as np

print('Sanitizing CSV for MySQL Workbench Wizard...')
df = pd.read_csv('superstore_orders_cleaned.csv')

# Get text columns
text_cols = df.select_dtypes(include=['object']).columns

# Remove ALL characters that confuse the wizard:
# Single quotes, Double quotes, Commas, Newlines, Backslashes
for col in text_cols:
    df[col] = df[col].astype(str)
    # Removing completely
    df[col] = df[col].str.replace('"', '', regex=False)
    df[col] = df[col].str.replace("'", "", regex=False)
    # Replacing with space
    df[col] = df[col].str.replace(',', ' ', regex=False)
    df[col] = df[col].str.replace('\\', ' ', regex=False)
    df[col] = df[col].str.replace('\n', ' ', regex=False)
    df[col] = df[col].str.replace('\r', '', regex=False)
    # Clean up double spaces that might have formed
    df[col] = df[col].str.replace('  ', ' ', regex=False)

df.to_csv('superstore_orders_cleaned.csv', index=False)
print('CSV heavily sanitized and saved.')
