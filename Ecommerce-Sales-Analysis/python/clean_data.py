import pandas as pd
import numpy as np
import shutil
import os

print("Starting Phase 2 & 3: Excel Data Cleaning and CSV Preparation...")

dataset_path = "global_superstore_2016.xlsx"
working_copy = "superstore_working.xlsx"
csv_output = "superstore_orders_cleaned.csv"

# Step 3 — Create Working Copy
print("Creating working copy...")
if not os.path.exists(dataset_path):
    print(f"Error: {dataset_path} not found. Please download it and place it in the dataset folder.")
    exit(1)
    
shutil.copy(dataset_path, working_copy)

# Step 4-6 — Clean Data, Handle Missing Values & Format
print("Loading Orders sheet from working copy...")
# We only want the Orders sheet
df = pd.read_excel(working_copy, sheet_name='Orders')

print("Handling missing values...")
# Postal Code -> fill with "Unknown"
if 'Postal Code' in df.columns:
    df['Postal Code'] = df['Postal Code'].fillna("Unknown")

# Text columns -> fill "Not Available"
text_cols = df.select_dtypes(include=['object']).columns
df[text_cols] = df[text_cols].fillna("Not Available")

# Numeric columns (Profit/Sales)
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(0) # or handle appropriately

# Convert types if necessary
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'])
if 'Ship Date' in df.columns:
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Step 7 — Create New Columns (Order Year, Order Month)
print("Creating Order Year and Order Month columns...")
if 'Order Date' in df.columns:
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.strftime('%B') # Full month name like 'January'

# Step 8 & 9 — Save Cleaned File and Export to CSV
print("Saving cleaned data back to Excel (superstore_working.xlsx)...")
# Write back to excel (just the Orders sheet for simplicity, or we can use ExcelWriter to keep others, 
# but project instructions only say work on Orders sheet, and save superstore_working.xlsx)
with pd.ExcelWriter(working_copy, engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name='Orders', index=False)

print(f"Exporting to CSV ({csv_output})...")
df.to_csv(csv_output, encoding='utf-8', index=False)

# Step 10 — Verify CSV Rows
print(f"CSV Export successful. Total Rows: {len(df)}")
print("Phase 2 and 3 completed successfully!")
