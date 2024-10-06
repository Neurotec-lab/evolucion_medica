import streamlit as st
import pandas as pd
import os
from datetime import datetime
import re

# Constants
PATIENT_DB_FILE = "patient_database.csv"
REPORTS_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "reports")


def load_patient_database():
    db_path = os.path.join(os.path.dirname(__file__), "..", PATIENT_DB_FILE)
    if not os.path.exists(db_path):
        st.error(f"Patient database file '{db_path}' not found.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(db_path)
        return df
    except Exception as e:
        st.error(f"Error loading patient database: {str(e)}")
        return pd.DataFrame()


def find_patient_reports(patient_name):
    reports = []
    patient_name_underscore = patient_name.replace(" ", "_")

    try:
        if not os.path.exists(REPORTS_DIRECTORY):
            st.error(f"Reports directory does not exist: {REPORTS_DIRECTORY}")
            return []

        pattern = re.compile(rf"{re.escape(patient_name_underscore)}_(\d{{8}}_\d{{4}}).*\.docx", re.IGNORECASE)

        for filename in os.listdir(REPORTS_DIRECTORY):
            match = pattern.match(filename)
            if match:
                date_time_str = match.group(1)
                try:
                    report_datetime = datetime.strptime(date_time_str, '%d%m%Y_%H%M')
                    formatted_date = report_datetime.strftime('%d-%m-%Y')
                    formatted_time = report_datetime.strftime('%H:%M')
                    reports.append((filename, formatted_date, formatted_time))
                except ValueError:
                    pass  # Silently skip files with unparseable dates

        return sorted(reports, key=lambda x: datetime.strptime(f"{x[1]} {x[2]}", '%d-%m-%Y %H:%M'), reverse=True)
    except Exception as e:
        st.error(f"Error accessing reports directory: {str(e)}")
        return []


def main():
    st.title("Patient Report Search")

    patient_df = load_patient_database()

    rut = st.text_input("Enter patient RUT:")

    if st.button("Search"):
        if rut:
            patient = patient_df[patient_df["Rut"] == rut]

            if not patient.empty:
                patient_name = patient['Nombre'].values[0]
                st.success(f"Patient found: {patient_name}")

                reports = find_patient_reports(patient_name)

                if reports:
                    st.subheader("Available Reports")
                    for report, report_date, report_time in reports:
                        report_path = os.path.join(REPORTS_DIRECTORY, report)
                        if os.path.exists(report_path):
                            if st.download_button(
                                    label=f"Download report from {report_date} at {report_time}",
                                    data=open(report_path, "rb"),
                                    file_name=report,
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            ):
                                st.success(f"Report {report} downloaded successfully!")
                else:
                    st.info("No reports found for this patient.")
            else:
                st.warning("Patient not found in the database.")
        else:
            st.warning("Please enter a RUT to search.")


if __name__ == "__main__":
    main()