import pandas as pd
import os

def clean_data():
    # Define file paths
    input_path = '../dataset/raw/UK_Accident.csv'
    output_path = '../dataset/processed/accident_cleaned.csv'
    
    print("Starting data cleaning process...")
    
    # Load dataset
    try:
        # The file seems to have an unnamed index column as the first column
        df = pd.read_csv(input_path, index_col=0)
        print(f"Dataset loaded successfully with {df.shape[0]} rows.")
    except FileNotFoundError:
        print(f"Error: {input_path} not found.")
        return

    # Standardize column names IMMEDIATELY (lowercase + underscore)
    df.columns = [col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]
    
    # Map key columns if they have different names in the UK dataset
    # Local_Authority_(District) -> region/city
    if 'local_authority_district' in df.columns:
        df = df.rename(columns={'local_authority_district': 'region'})
    
    # Weather_Conditions -> weather_condition
    if 'weather_conditions' in df.columns:
        df = df.rename(columns={'weather_conditions': 'weather_condition'})

    # Check missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # Fill missing values
    fill_values = {
        'region': 'Unknown',
        'weather_condition': 'Unknown',
        'road_type': 'Unknown'
    }
    for col, val in fill_values.items():
        if col in df.columns:
            df[col] = df[col].fillna(val)

    # Convert date to datetime
    if 'date' in df.columns:
        # UK dates are often DD/MM/YYYY
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['date'])

    # Extract month, year, day_of_week
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['day_of_week_extracted'] = df['date'].dt.day_name() # Use extracted to be sure

    # Remove duplicates
    df = df.drop_duplicates()

    # Check missing values after cleaning
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved to {output_path}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    clean_data()
