import streamlit as st
import pandas as pd
import os
import re
from PIL import Image

def load_patient_database():
    try:
        df = pd.read_csv("../patient_database.csv")
        return df
    except FileNotFoundError:
        st.error("Patient database file not found.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading database: {str(e)}")
        return pd.DataFrame()


def get_recent_reports(n=5):
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        return []

    reports = [f for f in os.listdir(reports_dir) if f.endswith('.docx')]
    reports.sort(key=lambda x: os.path.getmtime(os.path.join(reports_dir, x)), reverse=True)
    return reports[:n]


def extract_days(hospitalization_time):
    match = re.search(r'(\d+)', hospitalization_time)
    return int(match.group(1)) if match else 0


def calculate_stats(df):
    stats = {
        "Número total de registros": len(df),
        "Tiempo promedio de hospitalización (días)": "N/A",
        "Pacientes actualmente hospitalizados": "N/A",
        "Diagnósticos más comunes": "N/A"
    }

    if not df.empty:
        if 'Días de hospitalización' in df.columns:
            # Extract the number of days from the string
            df['Hospitalization Days'] = df['Días de hospitalización'].apply(extract_days)

            # Calculate average hospitalization time
            avg_time = df['Hospitalization Days'].mean()
            stats["Tiempo promedio de hospitalización (días)"] = f"{avg_time:.1f}"

            # Count of currently hospitalized patients (assuming they're hospitalized if days > 0)
            current_patients = (df['Hospitalization Days'] > 0).sum()
            stats["Pacientes actualmente hospitalizados"] = current_patients

        # Most common diagnoses
        if 'Diagnostico' in df.columns:
            top_diagnoses = df['Diagnostico'].value_counts().head(3)
            stats["Diagnósticos más comunes"] = ", ".join(f"{diag} ({count})" for diag, count in top_diagnoses.items())

    return stats


def main():
    st.set_page_config(page_title="Sistema electrónico Neurocirugía Curicó", layout="wide")
    header_image_path = "header.jpg"  # Adjust this path if needed
    if os.path.exists(header_image_path):
        # Open the image
        header_image = Image.open(header_image_path)

        # Get the original dimensions
        # Display the resized color image
        st.image(header_image, use_column_width=True)
    else:
        st.error(f"Header image not found: {header_image_path}")

    st.title("Sistema electrónico Neurocirugía Curicó")

    # Load patient database
    df = load_patient_database()

    # Calculate and display statistics
    stats = calculate_stats(df)
    st.subheader("Estadísticas de la base de datos")
    for metric, value in stats.items():
        st.metric(label=metric, value=value)

    # Recent reports
    st.subheader("Informes recientes")
    recent_reports = get_recent_reports()
    if recent_reports:
        for report in recent_reports:
            st.write(f"- {report}")
    else:
        st.write("No se encontraron informes recientes.")

    st.markdown("""
            <style>
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #f0f2f6;
                color: #31333F;
                text-align: center;
                padding: 10px 0;
                font-size: 14px;
                border-top: 1px solid #d1d1d1;
            }
            </style>
            <div class="footer">
                <p><strong>AVISO DE CONFIDENCIALIDAD:</strong> La información contenida en este sistema es confidencial y está protegida por ley. El acceso no autorizado está prohibido.</p>
                <p>© 2024 Neurocorp Spa. Todos los derechos reservados.</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()