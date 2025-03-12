import pandas as pd
import re

def extract_medicines(md_file):
    """Reads an MD file and extracts only medicine names."""
    with open(md_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract medicine names (skip headers, numbers, and punctuation)
    medicines = [re.sub(r"^\d+\.\s*", "", line).strip() for line in lines if re.match(r"^\d+\.", line)]
    
    return medicines

# Load transformed CSV
df_csv = pd.read_csv("english_medicines.csv")

df2 = pd.read_csv("medicines_transformed.csv")
# Concatenate both DataFrames
df_combined = pd.concat([df_csv, df2], ignore_index=True)

# Remove duplicates
df_combined = df_combined.drop_duplicates()

# Save back to CSV
df_combined.to_csv("medicines.csv", index=False)

# Print output
print(df_combined)
