# %%
import pandas as pd
import numpy as np
import os 
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# Define file path
file_path = r"" #INPUT FULL PATH OF THE DATA SOURCE HERE

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load the first sheet of the Excel file
df = pd.read_excel(file_path, sheet_name=0)

# Ensure column names match expected format
df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces

# Rename the elevation and group columns for consistency
df.rename(columns={'ele': 'Elevation', 'ROUND': 'Group'}, inplace=True)

# Convert max elevation to integer for binning
max_elevation = int(df['Elevation'].max())

# Define elevation bins with 100m intervals
bins = list(range(0, max_elevation + 100, 100))
labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins)-1)]

# Categorize elevation into 100m bins
df['Elevation_Range'] = pd.cut(df['Elevation'], bins=bins, labels=labels, right=False)

# Create a pivot table to count occurrences
pivot_table = df.pivot_table(index='Elevation_Range', columns='Group', aggfunc='size', fill_value=0)

# Convert pivot table into a long format for visualization
plot_data = pivot_table.reset_index().melt(id_vars='Elevation_Range', var_name='Group', value_name='Count')

# Create a Seaborn barplot
plt.figure(figsize=(12, 6))
sns.barplot(data=plot_data, x='Elevation_Range', y='Count', hue='Group')
plt.xticks(rotation=90)
plt.xlabel("Elevation Range (m)")
plt.ylabel("Count of Entries")
plt.title("Elevation Distribution Across Groups")
plt.legend(title="Group")
plt.tight_layout()
plt.show()

# Print the pivot table
print(pivot_table)
