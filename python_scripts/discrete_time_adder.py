import glob
import os
import pandas as pd


def add_discrete_time_column(df):
    # Create a new column "Discrete_Time" starting from 1, considering the group of identical "Time" values
    df['Discrete_Time'] = df.groupby('Time').ngroup() + 1

    # Reorder the columns to have "Discrete_Time" as the second column
    column_order = ['Discrete_Time', 'Time'] + [col for col in df.columns if col not in ['Time', 'Discrete_Time']]
    df = df[column_order]

    return df


def process_csv(csv_file):
    print(f"Processing {csv_file}")
    df = pd.read_csv(csv_file, delimiter=';')
    df = add_discrete_time_column(df)
    # Save the sorted DataFrame back to the same CSV file, overwriting the existing file
    df.to_csv(csv_file, index=False, sep=';')
    print("finished one")

def iterate_csvs(dest_folder):
    csv_files = glob.glob(os.path.join(dest_folder, "*.csv"))
    for csv_file in csv_files:
        process_csv(csv_file)


if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    final_folder = os.path.join(current_folder, "finalCsvs")
    iterate_csvs(final_folder)