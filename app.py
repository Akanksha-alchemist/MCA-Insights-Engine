
import streamlit as st
import pandas as pd
import os
import numpy as np
import warnings


warnings.filterwarnings('ignore', category=UserWarning, module='pandas')


DATA_PATH = os.path.join(os.path.dirname(__file__), 'DATA')

ENRICHED_PATH = os.path.join(DATA_PATH, 'enriched_master_dataset.csv')
CHANGELOG_PATH = os.path.join(DATA_PATH, 'changelog_day1_day2.csv')
DAY3_MASTER_PATH = os.path.join(DATA_PATH, 'Day3_masterdf.csv')


def ai_summary(df_log):

    total = len(df_log)
    new_incorp = df_log[df_log['Change_Type'].str.contains('New Incorporation', na=False)].shape[0]
    field_updates = total - new_incorp

    st.markdown("### 🤖 AI Summary")
    st.info(f""" 
       Event Detected: **{total}**
       * New Incorporations: **{new_incorp}**
       * Field Update: **{field_updates}**
    """)


def run_app():
    st.set_page_config(layout="wide")
    st.title("MAC Insights Dashboard")

    df_display = pd.DataFrame()
    df_log = pd.DataFrame()

    try:
        df_audit_log = pd.read_csv(ENRICHED_PATH)
        df_log = pd.read_csv(CHANGELOG_PATH)
        df_base = pd.read_csv(DAY3_MASTER_PATH)




        df_audit_log['CIN'] = df_audit_log['CIN'].astype(str).str.strip()
        df_base['CIN'] = df_base['CIN'].astype(str).str.strip()


        if 'NEW_VALUE_FIELD' in df_audit_log.columns:
            df_audit_log = df_audit_log.rename(columns={'NEW_VALUE_FIELD': 'NEW_VALUE'})


        if 'NEW_VALUE' not in df_audit_log.columns:
            raise KeyError("NEW_VALUE")


        df_master = df_audit_log.pivot_table(
            index=['CIN', 'COMPANY_NAME', 'STATE', 'STATUS'],
            columns='FIELD',
            values='NEW_VALUE',
            aggfunc='first'
        ).reset_index()


        base_fields = ['CIN', 'Authorized_Capital', 'Paidup_Capital', 'Date_of_Incorporation']

        df_display = pd.merge(df_master, df_base[base_fields], on='CIN', how='left')


        df_display['Year'] = pd.to_datetime(df_display['Date_of_Incorporation'], errors='coerce').dt.year.astype(str)


        df_display['STATE'] = df_display['STATE'].astype(str).str.strip()
        df_display['STATUS'] = df_display['STATUS'].astype(str).str.strip()

        df_display = df_display.fillna('N/A')

    except Exception as e:
        st.error(f"FATAL ERROR loading data. Ensure all CSVs are ready. Error: {e}")
        return

    ai_summary(df_log)

    st.sidebar.header("FILTER & SEARCH")


    selected_state = st.sidebar.multiselect("State", options=df_display['STATE'].unique(),
                                            default=df_display['STATE'].unique())
    selected_status = st.sidebar.multiselect("Status", options=df_display['STATUS'].unique(), default=['Active'])


    years = sorted(df_display['Year'].unique().tolist())
    selected_years = st.sidebar.multiselect("Incorporation Year", options=years, default=years)

    df_filtered = df_display[df_display['STATE'].isin(selected_state)].copy()
    df_filtered = df_filtered[df_filtered['STATUS'].isin(selected_status)].copy()
    df_filtered = df_filtered[df_filtered['Year'].isin(selected_years)].copy()

    search_query = st.text_input("Search (CIN or Company Name)", "")

    if search_query:

        search_query = search_query.strip()
        df_filtered = df_filtered[
            df_filtered['CIN'].astype(str).str.strip().str.contains(search_query, case=False, na=False) |
            df_filtered['COMPANY_NAME'].astype(str).str.strip().str.contains(search_query, case=False, na=False)
            ].copy()

    st.subheader(f"Enriched Company Records ({len(df_filtered)} records)")

    display_cols = [
        'CIN', 'COMPANY_NAME', 'STATUS', 'STATE', 'Sector', 'Director_Name',
        'Authorized_Capital', 'Paidup_Capital', 'Year'
    ]

    st.dataframe(df_filtered[display_cols], use_container_width=True)

    st.markdown("---")
    st.markdown("### 💬 Chatbot Query")

    chat_query = st.text_input("Ask a question (e.g., 'new incorporations in Maharashtra')", key="chat_input")

    df_result = df_log.copy()

    if chat_query:
        if df_log.empty:
            st.write("No changes found in the audit log.")

        if "new incorporations" in chat_query.lower():
            df_result = df_result[df_result['Change_Type'].str.contains('New Incorporation', na=False)]

        if "maharashtra" in chat_query.lower():
            df_result = df_result[df_result['CIN'].astype(str).str.contains('MH', na=False)]

        if not df_result.empty:
            st.write("Query Acknowledged. Results from Change Log:")
            st.dataframe(df_result[['CIN', 'Change_Type', 'Field_Changed', 'New_Value']].head(5))
        else:
            st.write("No matching changes found in the audit log for that query.")


if __name__ == "__main__":
    run_app()


