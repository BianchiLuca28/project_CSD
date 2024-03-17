import csv
import glob
import os
import sys

import pandas as pd

label_mapping = {
    "Acquisition_Number": "Acquisition_Number",
    "Acquisition_Name": "Acquisition_Name",
    "Date": "Date",
    "Task_MS": "Task_MS",
    "Task MS": "Task_MS",
    "Diametro": "Diameter",
    "Id": "Id",
    "N°Fili": "N_Wires",
    "Pezzi_fare": "Pieces_To_Make",
    "Pezzi_fatti": "Pieces_Made",
    "Cnt_Call_Start_1": "Cnt_Call_Start_1",
    "Time_Worked_1": "Time_Worked_1",
    "Cnt_Error_1": "Cnt_Error_1",
    "Average_Current_1": "Average_Current_1",
    "Average_Velocity_1": "Average_Velocity_1",
    "Average_Temperature_1": "Average_Temperature_1",
    "Total_Rev_1": "Total_Rev_1",
    "Cnt_Call_Start_2": "Cnt_Call_Start_2",
    "Time_Worked_2": "Time_Worked_2",
    "Cnt_Error_2": "Cnt_Error_2",
    "Average_Current_2": "Average_Current_2",
    "Average_Velocity_2": "Average_Velocity_2",
    "Average_Temperature_2": "Average_Temperature_2",
    "Total_Rev_2": "Total_Rev_2",
    "Sviluppo pezzo": "Development_Piece",
    "Velocita asse": "Axis_Speed"
}

unique_id = 1

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def extract_metadata_from_csv(csv_file):
    # Function to extract metadata from each CSV file
    metadata = {}
    with open(csv_file, 'r', encoding='latin-1') as file:
        # Read the CSV until the # symbol
        for line in file:
            if line.strip() == "#":
                break
            key, value = line.strip().split(';', 1)
            metadata[key] = value
    return metadata

def delete_data_up_to_hashtag(input_csv):
    # Create a temporary file to write the modified content
    temp_file_path = input_csv + '.temp'

    with open(temp_file_path, 'w', newline='', encoding='latin-1') as temp_file:
        # Open the original CSV file and skip lines until the #
        with open(input_csv, 'r', newline='', encoding='latin-1') as original_file:
            for line in original_file:
                if line.strip() == "#":
                    break

            # Write the remaining lines to the temporary file
            temp_file.writelines(original_file)

    # Replace the original CSV file with the modified temp file
    os.remove(input_csv)
    os.rename(temp_file_path, input_csv)

def add_acquisition_n_column(csv_file):
    global unique_id
    # Create a temporary file to write the modified content
    temp_file_path = csv_file + '.temp'

    with open(temp_file_path, 'w', newline='', encoding='latin-1') as temp_file:
        # Write the header with Acquisition_Number added
        header = "Acquisition_Number," + open(csv_file, 'r', encoding='latin-1').readline()
        temp_file.write(header)

        # Open the original CSV file and add Acquisition_Number to every entry
        with open(csv_file, 'r', newline='', encoding='latin-1') as original_file:
            reader = csv.reader(original_file, delimiter='\t')
            next(reader)  # Skip the header

            for row in reader:
                # Add Acquisition_Number to the beginning of each row
                row = [str(unique_id)] + row
                temp_file.write('\t'.join(row) + '\n')

    # Replace the original CSV file with the modified temp file
    os.remove(csv_file)
    os.rename(temp_file_path, csv_file)
    unique_id += 1

def remove_header_and_add_number(csv_file):
    delete_data_up_to_hashtag(csv_file)
    add_acquisition_n_column(csv_file)

def populate_anagrafica(csv_file, output_csv, folder_name):
    global unique_id
    # Function to populate the anagrafica.csv file with metadata from each CSV file
    metadata = extract_metadata_from_csv(csv_file)
    # Add Acquisition_Number and Acquisition_Name to metadata
    metadata['Acquisition_Number'] = unique_id
    metadata['Acquisition_Name'] = folder_name

    # Map the labels based on label_mapping
    standardized_metadata = {label_mapping[key]: metadata[key] for key in metadata if key in label_mapping}
    print(standardized_metadata)

    original_order = list(label_mapping.values())
    unique_order = remove_duplicates(original_order)

    # Append the standardized metadata to the anagrafica.csv file
    with open(output_csv, 'a', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=unique_order)
        csv_writer.writerow(standardized_metadata)

    # # Check if this is the first entry and print unique_id
    # if unique_id == 1:
    #     print(f"Unique ID after the first entry: {unique_id}")
    #     # Stop the program
    #     sys.exit()

def normalize_dataset_and_anagrafica(current_folder, output_csv):
    all_items = os.listdir(current_folder)
    # Filter out only folders (directories)
    folders = [item for item in all_items if os.path.isdir(item)]
    # Print the list of folders
    for folder in folders:
        folder_path = os.path.join(current_folder, folder)

        # Use glob to get a list of CSV files in the current folder
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        for csv_file in csv_files:
            print(f"Processing {csv_file}")
            populate_anagrafica(csv_file, output_csv, folder)
            remove_header_and_add_number(csv_file)


if __name__ == "__main__":
    csv_file_path = "anagrafica.csv"
    current_folder = os.path.dirname(os.path.abspath(__file__))
    print(current_folder)
    anagrafica_path = os.path.join(current_folder, csv_file_path)
    normalize_dataset_and_anagrafica(current_folder, anagrafica_path)
