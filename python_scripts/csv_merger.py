import glob
import os
import pandas as pd

def delete_board4(csv_file):
    # Read the CSV into a DataFrame with the correct delimiter
    df = pd.read_csv(csv_file, delimiter=';')

    # Identify columns that start with "Board4"
    cols_to_drop = [col for col in df.columns if col.startswith("Unnamed")]
    print(cols_to_drop)

    # Drop the identified columns
    df = df.drop(columns=cols_to_drop)

    # Write the modified DataFrame back to the CSV file
    df.to_csv(csv_file, index=False, sep=';')

def merge_csvs(folder_path, output_path):
    # Check if folder name starts with 'NO' or 'RUOTA'
    if not folder_path.startswith('NO') and not folder_path.startswith('RUOTA'):
        return  # Skip checking this folder

    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Check if there are files to merge
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return

    # Read each CSV file into a DataFrame and concatenate them
    dfs = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    merged_df = pd.concat(dfs, ignore_index=True)

    # Write the merged DataFrame to a new CSV file
    output_csv_path = os.path.join(output_path, f"{os.path.basename(folder_path)}_merged.csv")
    merged_df.to_csv(output_csv_path, index=False)

def merge_two_categories(folder_path, output_path):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Check if there are files to merge
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return

    # Separate files based on category (NO or RUOTA)
    no_category_files = [file for file in csv_files if file.startswith("NO")]
    ruota_category_files = [file for file in csv_files if file.startswith("RUOTA")]

    # Merge and write DataFrames for each category
    if no_category_files:
        no_category_df = pd.concat((pd.read_csv(os.path.join(folder_path, file)) for file in no_category_files), ignore_index=True)
        no_category_df.to_csv(os.path.join(output_path, "NO_merged.csv"), index=False)
    print("Finished")
    if ruota_category_files:
        ruota_category_df = pd.concat((pd.read_csv(os.path.join(folder_path, file)) for file in ruota_category_files), ignore_index=True)
        ruota_category_df.to_csv(os.path.join(output_path, "RUOTA_merged.csv"), index=False)
    print("finished again")

def folder_csv_merger(current_folder):
    # Filter out only folders (directories)
    folders = [item for item in os.listdir(current_folder) if os.path.isdir(os.path.join(current_folder, item))]

    # Create the "mergedCsvs" folder if it doesn't exist
    output_folder = os.path.join(current_folder, "mergedCsvs")
    os.makedirs(output_folder, exist_ok=True)

    final_folder = os.path.join(current_folder, "finalCsvs")
    os.makedirs(final_folder, exist_ok=True)
    # for folder in folders:
    #     merge_csvs(folder, output_folder)

        # folder_path = os.path.join(current_folder, folder)
        #
        # # Use glob to get a list of CSV files in the current folder
        # csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        # for csv_file in csv_files:
        #     delete_board4(csv_file)


    merge_two_categories(output_folder, final_folder)



if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    folder_csv_merger(current_folder)