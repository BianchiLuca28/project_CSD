import csv
import glob
import os
import pandas as pd

column_names = ['Material', 'Speed', 'Diameter']

def extract_info_from_folder_name(folder_name):
    parts = folder_name.split('_')
    material = parts[2] if len(parts) > 2 else None
    diameter = parts[3] if len(parts) > 3 else None
    speed = int(parts[4].replace("VEL", "")) if len(parts) > 4 else None
    return material, speed, diameter

def add_columns_to_csv(csv_file, values):
    # Read the existing CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Add new columns to the header
    header = rows[0]
    for column_name in column_names:
        header.append(column_name)

    # Add corresponding values to each row
    for row in rows[1:]:
        for value in values:
            row.append(value)

    # Write the modified content back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def cycle_folders(current_folder):
    all_items = os.listdir(current_folder)
    # Filter out only folders (directories)
    folders = [item for item in all_items if os.path.isdir(os.path.join(current_folder, item))]
    # Print the list of folders
    for folder in folders:
        folder_path = os.path.join(current_folder, folder)
        folder_data = extract_info_from_folder_name(folder)

        # Use glob to get a list of CSV files in the current folder
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        for csv_file in csv_files:
            add_columns_to_csv(csv_file, folder_data)

if __name__ == '__main__':
    current_folder = os.path.dirname(os.path.abspath(__file__))
    cycle_folders(current_folder)
