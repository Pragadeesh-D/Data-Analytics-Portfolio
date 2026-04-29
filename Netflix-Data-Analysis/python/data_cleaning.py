import pandas as pd
import os

def clean_data():
    # Define file paths
    input_file = '../dataset/raw/netflix_titles.csv'
    output_file = '../dataset/processed/netflix_cleaned.csv'
    
    print("Starting data cleaning process...")
    
    # Load dataset
    try:
        df = pd.read_csv(input_file)
        print(f"Successfully loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    except FileNotFoundError:
        print(f"Error: Could not find the file {input_file}")
        return

    # Check initial missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # Fill missing values
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Not Available')
    df['country'] = df['country'].fillna('Unknown')
    
    # Optional: Fill other categorical columns just in case, or drop rows if needed. 
    # For now, we follow exact instructions. 
    # Let's also handle potential missing dates or ratings nicely:
    if 'date_added' in df.columns:
        df['date_added'] = df['date_added'].fillna('January 1, 2000') # Placeholder before conversion
    if 'rating' in df.columns:
        df['rating'] = df['rating'].fillna('Unknown')
        
    # Convert date_added to datetime
    if 'date_added' in df.columns:
        # Some dates might have leading/trailing spaces
        df['date_added'] = df['date_added'].str.strip()
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Strip whitespace from string columns
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # Standardize column names (lowercase + underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Check final missing values
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())
    
    # Save cleaned dataset
    df.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to {output_file}. Final shape: {df.shape[0]} rows, {df.shape[1]} columns.")

if __name__ == "__main__":
    # Change working directory to script location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    clean_data()
