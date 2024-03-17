import os
import pandas as pd
import glob

current_folder = os.path.dirname(os.path.abspath(__file__))
final_folder = os.path.join(current_folder, "finalCsvs")
csv_files = glob.glob(os.path.join(final_folder, "*.csv"))

for csv_file in csv_files:
    df = pd.read_csv(csv_file, delimiter=";")

    # # Apply the operation to 'Board3Acc3Z' column
    # df['Board3Acc3Z'] = df['Board3Acc3Z'].apply(lambda x: float(x[0:len(x) - 1]))

    column_values = df['Board3Acc3Z'].head(5).tolist()
    print(column_values)

    # # Save the changes back to the file
    # df.to_csv(csv_file, index=False, sep=";")
