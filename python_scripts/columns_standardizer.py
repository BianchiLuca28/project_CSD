import pandas as pd
import os
import glob

def parse_combined_column(combined_string):
    # Split the combined column into Acquisition_Number and Time using '\t' as the delimiter
    parts = combined_string.split('\t')
    return parts[0], parts[1]

def order_base_time(csv_file):
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file, delimiter=';')

    # Split the combined column into Acquisition_Number and Time
    new_columns = df[df.columns[0]].apply(parse_combined_column).apply(pd.Series)
    new_columns.columns = ['Acquisition_Number', 'Time']

    # Drop the original combined column and insert the new columns at the beginning
    df = pd.concat([new_columns, df.drop(df.columns[0], axis=1)], axis=1)

    # Apply the custom time parsing function to the "Time" column
    df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d-%H:%M:%S.%f')

    # Sort the DataFrame based on the "Time" column
    df = df.sort_values(by='Time')

    print(df.columns)

    # Save the sorted DataFrame back to the same CSV file, overwriting the existing file
    df.to_csv(csv_file, index=False, sep=';')

def csv_iterator(current_folder):
    # Use glob to get a list of CSV files in the current folder
    csv_files = glob.glob(os.path.join(current_folder, "*.csv"))
    for csv_file in csv_files:
        order_base_time(csv_file)

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    final_folder = os.path.join(current_folder, "finalCsvs")

    csv_iterator(final_folder)
