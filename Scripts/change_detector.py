import pandas as pd

import os

DATA_PATH = os.path.join(os.path.dirname(__file__),'..','DATA')

Masterfile_Day1= os.path.join(DATA_PATH,'Day2_masterdf.csv')
Masterfile_Day2 = os.path.join(DATA_PATH,'Day3_masterdf.csv')

change_log = os.path.join(DATA_PATH,'changelog_day2_day3.csv')

def master_file_loading():
    try:
        old_df = pd.read_csv(Masterfile_Day1)
        new_df = pd.read_csv(Masterfile_Day2)

        print("successfully done")
        return old_df,new_df

    except FileNotFoundError:
        print("missing file")
        return None,None



def detect_change(old_df , new_df):
    old_df = old_df.set_index('CIN').sort_index()
    new_df = new_df.set_index('CIN').sort_index()

    change_log= []
    change_date = '2025-10-17'

    new_cins = new_df.index.difference(old_df.index)

#new incorporation

    for cin in new_cins:
        change_log.append({
            'CIN' : cin,
            'Change_type' : 'New Incorporation',
            'Field_Changed' : 'N/A',
            'old_value' : 'N/A',
            'New_value' : new_df.loc[cin,'Company_Name'],
            'Date' : change_date

        })

    common_cins = old_df.index.intersection(new_df.index)

    column_comparison = [
            col for col in old_df.columns
            if col  not in ['STATE', 'ROC_Code', 'Date_of_Incorporation']
        ]

    diff = old_df[column_comparison].loc[common_cins].compare(new_df[column_comparison].loc[common_cins], keep_equal = False,keep_shape = False)

    if not diff.empty:

        changed_fields = diff.columns.levels[0]


        for cin, row_data in diff.iterrows():

            for col_name in changed_fields:


                old_val = row_data.get((col_name, 'self'))
                new_val = row_data.get((col_name, 'other'))

                if pd.notna(old_val) or pd.notna(new_val):


                    if col_name == 'Company_Status' and new_val == 'Strike Off':
                        change_type = 'Deregistered/Strike Off'
                    elif col_name in ['Authorized_Capital', 'Paidup_Capital']:
                        change_type = 'Capital Modification'
                    else:
                        change_type = 'Field Update'

                    change_log.append({
                        'CIN': cin,
                        'Change_Type': change_type,
                        'Field_Changed': col_name,
                        'Old_Value': old_val,
                        'New_Value': new_val,
                        'Date': change_date
                    })
        return pd.DataFrame(change_log)



if __name__ == "__main__":


    old_df, new_df = master_file_loading()

    if old_df is not None and new_df is not None:



        old_cols = set(old_df.columns)
        new_cols = set(new_df.columns)


        common_cols = sorted(list(old_cols.intersection(new_cols)))



        old_df = old_df[common_cols]
        new_df = new_df[common_cols]


        print("files loaded successfully")
        print(f"File length: {len(old_df)}")
        print(f"File length: {len(new_df)}")


        df_change_log = detect_change(old_df, new_df)

        if df_change_log.empty:
            print("\nno changes")
        else:
            print(f"\nTotal change {len(df_change_log)}")

            print(df_change_log[['CIN', 'Change_Type', 'Field_Changed', 'New_Value']].head())

            df_change_log.to_csv(change_log, index=False)
            print(f"\nSuccessfully saved {change_log}")