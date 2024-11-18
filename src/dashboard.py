import streamlit as st
import pandas as pd
import sys
import os
from api.google_sheets import connect_to_google_sheets, update_google_sheets
from utils.file_handler import load_csv
from api.search_api import search_query
from api.llm_parser import parse_results_with_llm
from utils.rate_limiter import rate_limiter

sys.path.append('..')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def run_dashboard():
    st.set_page_config(page_title="AI Data Extraction Dashboard", layout="wide", initial_sidebar_state="expanded")
    
    st.markdown("""
    <style>
        body {
            background-color: #D4E6F1;  
            font-family: 'Roboto', sans-serif;
            color: #34495E;
        }
        .stApp {
            background-color: #D4E6F1;  
        }
        
        .file-uploader {
            background-color: #F8D7DA;  
            border: 2px dashed #E57373;  
            border-radius: 10px;
            padding: 20px;
            color: #B71C1C;
            font-weight: bold;
            text-align: center;
        }
        .stButton>button {
            background-color: #6C63FF;
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease, transform 0.3s ease;
            border: none;
        }
        .stButton>button:hover {
            background-color: #5a52e5;
            transform: scale(1.05);
        }
        .stButton>button:active {
            transform: scale(0.98);
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border: 2px solid #6C63FF;
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
            width: 100%;
            background-color: #f0f0f0;
        }
        .stTextArea>div>div>textarea {
            background-color: #f7f7f7;
        }
        .stDataFrame {
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .stProgress>div>div>div>div {
            background-color: #6C63FF;
        }
        h1, h2, h3 {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        }
        .stMarkdown {
            color: #34495E;
            font-size: 16px;
        }
        .stSidebar {
            background-color: #2C3E50;
        }
        .stSidebar .sidebar-content {
            color: white;
        }
        .stDownloadButton>button {
            background-color: #FF9800;
            color: white;
            border-radius: 12px;
            padding: 12px;
            width: 100%;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .stDownloadButton>button:hover {
            background-color: #FF5722;
            transform: scale(1.05);
        }
        .stDownloadButton>button:active {
            transform: scale(0.98);
        }
        .section-title {
            background-color: #2C3E50;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            color: white;
            font-size: 22px;
        }
        .container {
            padding: 25px;
            background: #D4E6F1;  
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }
        .tab {
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

    st.title("🚀 **AI Data Extraction Agent**")
    st.markdown("### Automate your data extraction and analysis effortlessly! 📊")
    
    st.markdown("""<div class="section-title">Step-by-Step Guide for Data Processing</div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📁 Upload Data", "🔗 Google Sheets", "🔍 Data Extraction"])

    with tab1:
        st.subheader("1. Upload a CSV File")
        csv_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")
        csv_data = None
        columns = None

        if csv_file:
            csv_data = load_csv(csv_file)
            if csv_data is not None:
                st.write("### Data Preview")
                st.dataframe(csv_data.head(), use_container_width=True)
                columns = list(csv_data.columns)
                st.write("### Available Columns")
                st.write(columns)

    with tab2:
        st.subheader("2. Connect to Google Sheets")
        st.markdown("**Note:** Ensure you have a valid credentials JSON file for Google Sheets API access.")

        google_credentials_path = st.text_input("Enter the path to your Google Sheets credentials JSON file", "")
        sheet_name = st.text_input("Enter the name of your Google Sheet", "")

        sheet_data = None
        if google_credentials_path and sheet_name:
            sheet_data = connect_to_google_sheets(google_credentials_path, sheet_name)
            if sheet_data is not None:
                st.write("### Google Sheets Data Preview")
                st.dataframe(sheet_data.head())
                columns = list(sheet_data.columns)
                st.write("### Available Columns")
                st.write(columns)

    with tab3:
        if columns:
            st.subheader("3. Select the Main Column")
            main_column = st.selectbox("Choose the main column (e.g., company names)", columns, key="main_column")

        st.subheader("4. Define Your Advanced Query Template")
        query_template = st.text_area(
            "Enter your query template (e.g., 'Get the email and address for {company}')",
            height=150
        )
        st.write("**Tip**: Use `{column_name}` as a placeholder in your query for better results.")

        if csv_data is not None and main_column:
            st.markdown("### 📊 Run Web Search and Extract Information")
            if st.button("Run Extraction", key="run_extraction"):
                st.info("The extraction process may take some time depending on the data size. Please wait...")

                progress = st.progress(0)
                extracted_results = []

                @rate_limiter(interval=1.5)
                def perform_search_and_extract(entity):
                    query = query_template.replace(f"{{{main_column}}}", str(entity))
                    
                    search_results = search_query(query)
                    
                    if search_results:
                        extracted_info = parse_results_with_llm(entity, search_results, query_template)
                        return {"entity": entity, "extracted_info": extracted_info}
                    else:
                        return {"entity": entity, "extracted_info": "No results found."}

                # Iterate over each entity and call the function with only one argument
                for index, entity in enumerate(csv_data[main_column]):
                    result = perform_search_and_extract(entity)  # Corrected function call
                    extracted_results.append(result)
                    st.write(f"**Extracted information for {entity}:** {result['extracted_info']}")

                results_df = pd.DataFrame(extracted_results)
                st.write("### All Extracted Information")
                st.dataframe(results_df, use_container_width=True)

                st.download_button(
                    "💾 Download Extracted Information as CSV",
                    results_df.to_csv(index=False),
                    "extracted_information.csv",
                    "text/csv",
                    use_container_width=True
                )

                if google_credentials_path and sheet_name:
                    if st.button("📤 Update Google Sheet with Extracted Information", key="update_sheet"):
                        success = update_google_sheets(google_credentials_path, sheet_name, results_df)
                        if success:
                            st.success("Google Sheet updated successfully! 🎉", icon="✅")
                        else:
                            st.error("Failed to update Google Sheet. Please check your credentials and try again.", icon="❌")

if __name__ == "__main__":
    run_dashboard()
