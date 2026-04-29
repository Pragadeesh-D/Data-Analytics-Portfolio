import pandas as pd
import numpy as np

print("Loading CSV...")
df = pd.read_csv('superstore_orders_cleaned.csv')

# Replace NaN with None (which translates to NULL in SQL)
df = df.replace({np.nan: None})

# Determine SQL column types based on dataframe dtypes
def get_sql_type(col_name, dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'INT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'DECIMAL(10,2)'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATE'
    else:
        # Determine max length
        max_len = df[col_name].astype(str).str.len().max()
        if max_len < 255:
            return 'VARCHAR(255)'
        else:
            return 'TEXT'

sql_cols = []
for col in df.columns:
    # Safely format column names to be SQL friendly
    safe_col = col.replace(' ', '_').replace('-', '_')
    col_type = get_sql_type(col, df[col].dtype)
    sql_cols.append(f'`{safe_col}` {col_type}')

create_table_stmt = f"""
USE ecommerce_sales;
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    {', '.join(sql_cols)}
);
"""

# Format values for SQL insert
def format_val(val):
    if pd.isna(val) or val is None:
        return 'NULL'
    if isinstance(val, (int, float, np.integer, np.floating)):
        return str(val)
    # Escape quotes
    return "'" + str(val).replace("'", "''") + "'"

out_sql = '../sql/import_data.sql'
print(f"Generating {out_sql} ...")
with open(out_sql, 'w', encoding='utf-8') as f:
    f.write(create_table_stmt)
    f.write('\n')
    
    # Bulk insert
    chunk_size = 1000
    safe_cols = [f'`{c.replace(" ", "_").replace("-", "_")}`' for c in df.columns]
    
    # Pre-calculate string representations for each row to speed up
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        values_list = []
        for _, row in chunk.iterrows():
            formatted_row = [format_val(x) for x in row]
            values_list.append('(' + ', '.join(formatted_row) + ')')
        
        insert_stmt = f"INSERT INTO orders ({', '.join(safe_cols)}) VALUES " + ', '.join(values_list) + ";\n"
        f.write(insert_stmt)

print('SQL Import file generated successfully.')
