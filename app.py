import streamlit as st
import pandas as pd
import numpy as np

st.title("Data Cleaning App")

# File Uploading 
uploaded_file = st.file_uploader("Upload your dataset (CSV format only)", type="csv")

if uploaded_file:
    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.write("### Original Dataset")
    st.dataframe(df)

    # Sidebar options
    st.sidebar.header("Cleaning Options")

    # Handle Missing Values
    missing_value_option = st.sidebar.selectbox(
        "Handle Missing Values",
        ("Do Nothing", "Drop Missing Values", "Fill with Mean", "Fill with Median", "Fill with Mode"),
    )

    # Drop Duplicates
    drop_duplicates = st.sidebar.checkbox("Drop Duplicate Rows")

    # Rename Columns
    rename_columns = st.sidebar.text_area(
        "Rename Columns (Enter comma-separated new names, leave blank to skip)",
        placeholder="e.g., Col1, Col2, Col3",
    )

    # Convert Data Types
    convert_types = st.sidebar.text_area(
        "Convert Column Data Types (Enter as 'Column:Type', e.g., Age:int)",
        placeholder="e.g., Age:int, Price:float",
    )

    # Cleaning steps 
    if st.sidebar.button("Apply Cleaning"):
        cleaned_df = df.copy()

        # Handle Missing Values
        if missing_value_option == "Drop Missing Values":
            cleaned_df.dropna(inplace=True)
        elif missing_value_option == "Fill with Mean":
            cleaned_df.fillna(cleaned_df.mean(numeric_only=True), inplace=True)
        elif missing_value_option == "Fill with Median":
            cleaned_df.fillna(cleaned_df.median(numeric_only=True), inplace=True)
        elif missing_value_option == "Fill with Mode":
            cleaned_df.fillna(cleaned_df.mode().iloc[0], inplace=True)

        # Drop Duplicates
        if drop_duplicates:
            cleaned_df.drop_duplicates(inplace=True)

        # Rename Columns
        if rename_columns:
            new_column_names = [name.strip() for name in rename_columns.split(",")]
            if len(new_column_names) == len(cleaned_df.columns):
                cleaned_df.columns = new_column_names
            else:
                st.warning("Number of new column names doesn't match the dataset columns. Skipping rename.")

        # Convert Data Types
        if convert_types:
            for item in convert_types.split(","):
                try:
                    column, dtype = item.split(":")
                    cleaned_df[column.strip()] = cleaned_df[column.strip()].astype(dtype.strip())
                except Exception as e:
                    st.warning(f"Error converting {item}: {e}")

        # Display Cleaned Data
        st.write("### Cleaned Dataset")
        st.dataframe(cleaned_df)

        # Download Cleaned Dataset
        @st.cache_data
        def convert_df_to_csv(dataframe):
            return dataframe.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(cleaned_df)
        st.download_button(
            label="Download Cleaned Data as CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
        )
