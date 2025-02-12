import pandas as pd
import json

# Read the Excel file
df = pd.read_excel('github/static-website/data.xlsx', header=None)

# Convert the DataFrame to a list of lists
data = df.values.tolist()

# Extract headers and rows
headers = data[0]
rows = data[1:]

# Create a dictionary to hold the data
data_dict = {
    "headers": headers,
    "rows": rows
}

# Write the data to a JSON file
with open('github/static-website/data.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=2)

print('Data has been written to data.json')
