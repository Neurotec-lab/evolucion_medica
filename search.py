import streamlit as st
import pandas as pd
import csv
from io import StringIO
import base64


# Function to load the patient database
def load_patient_database(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y', errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading patient database: {str(e)}")
        return pd.DataFrame()


# Function to search for patient records
def search_patient_records(df, rut):
    return df[df['Rut'] == rut].sort_values('Fecha', ascending=False)


# Function to create a downloadable link for CSV data
def get_csv_download_link(df, filename="patient_data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href


# Main Streamlit app
def main():
    st.title("Patient Data Search and Download")

    # Load the patient database
    db_file = "patient_database.csv"  # Update this with your actual database file path
    df = load_patient_database(db_file)

    if df.empty:
        st.warning("No patient data available.")
        return

    # Input for RUT
    rut = st.text_input("Enter patient RUT:")

    if rut:
        # Search for patient records
        patient_records = search_patient_records(df, rut)

        if patient_records.empty:
            st.warning("No records found for this RUT.")
        else:
            st.success(f"Found {len(patient_records)} records for RUT: {rut}")

            # Display available dates
            st.subheader("Available Dates:")
            dates = patient_records['Fecha'].dt.strftime('%d-%m-%Y').tolist()
            for date in dates:
                st.write(date)

            # Date range selection
            st.subheader("Select Date Range for Download:")
            start_date = st.date_input("Start Date", min(patient_records['Fecha']).date())
            end_date = st.date_input("End Date", max(patient_records['Fecha']).date())

            # Filter records based on date range
            filtered_records = patient_records[
                (patient_records['Fecha'].dt.date >= start_date) &
                (patient_records['Fecha'].dt.date <= end_date)
                ]

            if not filtered_records.empty:
                st.write(f"Records found in selected date range: {len(filtered_records)}")

                # Create download link
                st.markdown(get_csv_download_link(filtered_records), unsafe_allow_html=True)
            else:
                st.warning("No records found in the selected date range.")


if __name__ == "__main__":
    main()