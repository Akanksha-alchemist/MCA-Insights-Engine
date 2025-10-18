
import pandas as pd
import os

all_df = []  # list for storing all the dfs;

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'DATA')


# ------

def standardize_columns(df, index):
    # 1. Cleaning columns
    df.columns = (
        df.columns.str.strip()
        .str.replace(' ', '_')
        .str.replace('(', '')
        .str.replace(')', '')
    )

    COLUMNS_TO_RENAME = {}

    # renaming
    for col in df.columns:
        if 'Date' in col or 'date' in col:
            COLUMNS_TO_RENAME[col] = 'Date_of_Incorporation'
            break

    # Applied
    df.rename(columns=COLUMNS_TO_RENAME, inplace=True)

    # 3. Column adding
    state_names = ['Delhi', 'Gujarat', 'Karnataka', 'Maharashtra', 'TamilNadu']
    state_name = state_names[index]
    df['STATE'] = state_name

    return df


def convert_datetime(df):

    df['Date_of_Incorporation'] = pd.to_datetime(df['Date_of_Incorporation'], errors='coerce')
    return df


def cleaning_Data(df):
    for c in ['Authorized_Capital', 'Paidup_Capital']:
        df[c] = df[c].fillna(0)
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    if 'Company_Status' in df.columns:
        df['Company_Status'] = df['Company_Status'].fillna('UNKNOWN')
    df.drop_duplicates(subset=['CIN'], keep='first', inplace=True)

    return df


# --- working here ---

if __name__ == "__main__":
    print("---starting---")

    files = ["Day3_Delhi.csv",
             "Day3_Gujarat.csv",
             "Day3_Karnataka.csv",
             "Day3_Maharashtra.csv",
             "Day3_Tamil_Nadu.csv"]

    # Brick 1: Loading
    for file in files:
        file_path = os.path.join(DATA_PATH, file)

        try:
            df = pd.read_csv(file_path)
            all_df.append(df)
            print(f"Loaded {file} successfully.")

        except FileNotFoundError:
            print(f"ERROR: File not found at: {file_path}. Please check file name and path.")
        except Exception as e:
            print(f"An error occurred while reading {file}: {e}")


    for i, df in enumerate(all_df):
        all_df[i] = standardize_columns(df, i)
        all_df[i] = convert_datetime(all_df[i])
        print(f"DF {i + 1}: Columns standardized and State added.")


    for i, df in enumerate(all_df):
        all_df[i] = cleaning_Data(all_df[i])
        print(f"DF {i + 1}: Data cleaned.")

    print("-------creating canonical master df------")

    #  Merging and Saving
    if all_df:
        Day3_masterdf = pd.concat(all_df, ignore_index=True)

        print("\nrecords per state")
        print(Day3_masterdf['STATE'].value_counts())

        print("checking sample of the data")
        # CRITICAL: Corrected typo in 'Company_Name'
        print(Day3_masterdf[['CIN', 'Company_Name', 'Authorized_Capital', 'STATE']].head())

        master_outputpath = os.path.join(DATA_PATH, 'Day3_masterdf.csv')
        Day3_masterdf.to_csv(master_outputpath, index=False)
        print("done successfully")

    else:
        print("df list is empty")


