import pandas as pd

# Read the text file with proper encoding and handle it as a single column of drug names
df = pd.read_csv('archive4/medicines.csv')
print(f"Original medicines.csv shape: {df.shape}")
df = df.drop_duplicates()
print(f"After removing duplicates: {df.shape}")

df2 = pd.read_csv('archive (2)/medicine_dataset.csv')
print(f"Original medicine_dataset.csv shape: {df2.shape}")
print(df2.columns.tolist())
# Keep only the Name column from df2
df2 = df2[['Name']]
print(f"Keeping only the Name column from df2")

print(df2.shape)
# unique_medicines = df2['Name'].unique()
# print(f"Unique medicines in df2: {unique_medicines.shape}")
df2 = df2.drop_duplicates()
print(f"After removing duplicates: {df2.shape}")

df3 = pd.read_csv('archive (3)/Medicine_Details.csv')
print(f"Original Medicine_Details.csv shape: {df3.shape}")
# Keep only the Medicine Name column from df3
df3 = df3[['Medicine Name']]
print(f"Keeping only the Medicine Name column from df3")
df3 = df3.drop_duplicates()
print(f"After removing duplicates: {df3.shape}")

# Check column names to understand the data structure
print("\nColumns in medicines.csv:")
print(df.columns.tolist())

print("\nColumns in medicine_dataset.csv (after filtering):")
print(df2.columns.tolist())

print("\nColumns in Medicine_Details.csv (after filtering):")
print(df3.columns.tolist())

# First, let's standardize column names to avoid case sensitivity issues
df.columns = [col.lower() for col in df.columns]
df2.columns = [col.lower() for col in df2.columns]
df3.columns = [col.lower() for col in df3.columns]

# Reset indices for proper concatenation
df = df.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
df3 = df3.reset_index(drop=True)

# Here we'll use pandas concat to combine all datasets
# Rename all columns to a standardized name for consistency
df.columns = ['medicine_name']
df2.columns = ['medicine_name']
df3.columns = ['medicine_name']
df.shape
df2.shape
df3.shape
# Now concat the dataframes
combined_df = pd.concat([df, df2, df3], ignore_index=True, sort=False)

# Remove any potential duplicates after concatenation
combined_df = combined_df.drop_duplicates()
print(f"\nFinal combined dataset shape: {combined_df.shape}")

# Save the combined dataset to a new CSV file
combined_df.to_csv('Medicine_Database.csv', index=False)
print("Combined dataset saved as Medicine_Database.csv")
