import os
import csv

def search_csv_files(folder_path, target_value):
    folders_with_value = {}  # Dictionary to store folders and corresponding CSV files with the value
    total_csv_files = 0  # Variable to store the total number of CSV files
    csv_files_with_value_count = 0  # Variable to store the number of CSV files with the value

    for top_level_folder in os.listdir(folder_path):
        top_level_folder_path = os.path.join(folder_path, top_level_folder)
        if os.path.isdir(top_level_folder_path):
            match_found_in_folder = False  # Flag to track if a match is found in the current folder
            csv_files_with_value = []  # List to store CSV files with the value in the current folder

            for subfolder_name in os.listdir(top_level_folder_path):
                subfolder_path = os.path.join(top_level_folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    for csv_file_name in os.listdir(subfolder_path):
                        if csv_file_name.endswith(".csv"):
                            total_csv_files += 1
                            csv_path = os.path.join(subfolder_path, csv_file_name)
                            with open(csv_path, 'r', encoding='latin-1') as file:
                                csv_reader = csv.reader(file)
                                for row_number, row_values in enumerate(csv_reader, start=1):
                                    if 20 <= row_number <= 25 and target_value in ";".join(row_values):
                                        match_found_in_folder = True
                                        csv_files_with_value.append(csv_file_name)
                                        csv_files_with_value_count += 1

            if match_found_in_folder:
                folders_with_value[top_level_folder] = csv_files_with_value

    # Calculate the percentage
    percentage = (csv_files_with_value_count / total_csv_files) * 100 if total_csv_files > 0 else 0

    # Print the summary
    print("\nSummary:")
    print(f"  - Total CSV files: {total_csv_files}")
    print(f"  - CSV files with value: {csv_files_with_value_count}")
    print(f"  - Percentage of CSV files with value: {percentage:.2f}%")

    # Print top-level folders and corresponding CSV files with the value
    print("\nTop-level folders with CSV files containing the value:")
    for folder, csv_files in folders_with_value.items():
        print(f"  - {folder}: {', '.join(csv_files)}")

if __name__ == "__main__":
    target_value = "Board4Acc1Y"
    current_folder = os.path.dirname(os.path.abspath(__file__))

    search_csv_files(current_folder, target_value)
