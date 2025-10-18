# import pandas as pd
# import os
# import numpy as np
# import random
#
# #paths
#
# DATA_PATH = os.path.join(os.path.dirname(__file__),'..','DATA')
#
# Master_file = os.path.join(DATA_PATH,'Day3_masterdf.csv')
#
# Enriched_path = os.path.join(DATA_PATH,'enriched_dataset.csv')
#
# def data_enriching(basedf):
#     sector = ['IT Services', 'Manufacturing', 'Finance', 'Real Estate', 'Retail', 'Logistics']
#     Director = ['Ravi Sharma', 'Priya Kapoor', 'Amit Singh', 'Anjali Desai']
#
#     data_size = len(basedf)
#
#     basedf['sector'] = np.random.choice(sector,size= data_size)
#     basedf['Director_name'] = np.random.choice(Director,size=data_size)
#
#     basedf['SOURCE'] = 'ZaubaCorp_Sim'
#     basedf = basedf.rename(columns={'Company_Status': 'STATUS', 'Company_Name': 'COMPANY_NAME'})
#
#
#     new_col= ['CIN', 'COMPANY_NAME', 'STATE', 'STATUS', 'SOURCE']
#
#     value_cols = ['Sector', 'Director_Name']
#
#     df_log = basedf.melt(
#         id_vars=new_col,
#         value_vars=value_cols,
#         var_name='FIELD',
#         value_name='NEW_VALUE'
#     )
#     df_log['SOURCE_URL'] = 'https://www.zaubacorp.com/cin/' + df_log['CIN'].astype(str)
#
#     final = ['CIN', 'COMPANY_NAME', 'STATE', 'STATUS', 'SOURCE', 'FIELD', 'SOURCE_URL']
#
#     return df_log[final]
#
#
# if __name__ == "__main__":
#     try:
#
#         basedf = pd.read_csv(Master_file)
#
#         df_log = data_enriching(basedf)
#
#
#         df_log.to_csv(Enriched_path, index=False)
#
#         print("\nEnrichment  Log ")
#         print(f"Total Log Entries: {len(df_log)}")
#
#     except FileNotFoundError:
#         print(f"ERROR: Master file not found.")
#     except Exception as e:
#         print(f"An error occurred during execution: {e}")

import pandas as pd
import os
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'DATA')

MASTER_FILE = os.path.join(DATA_PATH, 'Day3_masterdf.csv')
ENRICHED_PATH = os.path.join(DATA_PATH, 'enriched_master_dataset.csv')


def create_enriched_audit_log(df_base):
    df = df_base.copy()
    data_size = len(df)

    sectors_list = ['IT Services', 'Manufacturing', 'Finance', 'Real Estate', 'Retail', 'Logistics']
    directors_list = ['Ravi Sharma', 'Priya Kapoor', 'Amit Singh', 'Anjali Desai']

    df['Sector'] = np.random.choice(sectors_list, size=data_size)
    df['Director_Name'] = np.random.choice(directors_list, size=data_size)

    df['SOURCE'] = 'ZaubaCorp_Sim'

    df = df.rename(columns={'Company_Status': 'STATUS', 'Company_Name': 'COMPANY_NAME'})

    id_cols = ['CIN', 'COMPANY_NAME', 'STATE', 'STATUS', 'SOURCE']
    value_cols = ['Sector', 'Director_Name']

    df_audit_log = df.melt(
        id_vars=id_cols,
        value_vars=value_cols,
        var_name='FIELD',
        value_name='NEW_VALUE'
    )

    df_audit_log['SOURCE_URL'] = 'https://www.zaubacorp.com/cin/' + df_audit_log['CIN'].astype(str)

    final_cols = ['CIN', 'COMPANY_NAME', 'STATE', 'STATUS', 'SOURCE', 'FIELD', 'SOURCE_URL','NEW_VALUE']

    return df_audit_log[final_cols]


if __name__ == "__main__":
    try:
        df_base = pd.read_csv(MASTER_FILE)

        df_audit_log = create_enriched_audit_log(df_base)

        df_audit_log.to_csv(ENRICHED_PATH, index=False)

    except FileNotFoundError:
        pass
    except Exception as e:
        pass