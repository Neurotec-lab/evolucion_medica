import streamlit as st
from docx import Document
from docx.shared import Inches, Cm, Pt
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from datetime import datetime
import re

def create_word_document(data):
    doc = Document()
    section = doc.sections[0]
    section.page_height = Inches(11)  # Letter height
    section.page_width = Inches(8.5)  # Letter width
    section.left_margin = section.right_margin = section.top_margin = section.bottom_margin = Inches(0.5)
    section.orientation = WD_ORIENT.PORTRAIT

    # Set default paragraph format
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)  # Smaller font size
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    style.paragraph_format.space_after = Pt(0)  # Remove space after paragraphs

    # Add title
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    title = doc.add_heading(f"Evolución médica neurocirugía", level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.style.font.size = Pt(14)  # Larger font for title
    subtitle = doc.add_paragraph(f"{data['Nombre']} , {data['Fecha']}, {current_time}")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.style.font.size = Pt(12)  # Slightly larger font for subtitle

    # Define sections and their corresponding fields
    sections = {
        "Información del Paciente": ["Nombre", "Rut", "Edad", "Sexo", "Domicilio", "Fecha", "Fecha de ingreso", "Días de hospitalización"],
        "Antecedentes médicos": ["Alergias", "Tabaquismo", "Medicamentos", "Antiagregantes plaquetarios", "Anticoagulantes", "Antecedentes mórbidos"],
        "Evolución clínica": ["Peso", "Presión arterial", "Saturación O2", "Anamnesis", "Examen físico", "Escala de Glasgow"],
        "Tratamiento": ["Plan", "Reposo", "Tromboprofilaxis farmacológica", "Régimen nutricional", "Equipo multidisciplinario"],
        "Indicaciones enfermería": ["Retiro sonda foley", "Retiro de CVC", "Curación por enfermería", "Instalación sonda nasogástrica", "Oxigenoterapia", "Exámenes de laboratorio"],
        "Firma médico": ["Firma médico"]
    }

    # Add sections to the document
    for section_title, fields in sections.items():
        doc.add_heading(section_title, level=2).style.font.size = Pt(10)
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        table.autofit = False
        table.allow_autofit = False

        for field in fields:
            if field in data:
                row_cells = table.add_row().cells
                row_cells[0].text = field
                row_cells[1].text = str(data[field])

                # Limit text length for each cell
                for cell in row_cells:
                    if len(cell.text) > 50:  # Adjust this value as needed
                        cell.text = cell.text[:47] + "..."

        # Set column widths

      #  for cell in table.columns[0].cells:
       #     cell.width = Inches(2)
       # for cell in table.columns[1].cells:
        #    cell.width = Inches(5.5)

        # Apply smaller font size to table contents
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.style.font.size = Pt(8)

    # Create a filename-safe version of the patient's name
    safe_name = re.sub(r'[^\w\-_\. ]', '_', data['Nombre'])
    safe_name = safe_name.replace(' ', '_')

    filename = f"{safe_name}_{datetime.now().strftime('%d%m%Y_%H%M')}.docx"
    doc.save(filename)
    return filename

def main():
    st.title("Evolución médica neurocirugía")
    date = st.date_input("Fecha")  # Existing date input

    # Patient Information section
    st.subheader("Información del Paciente")
    col1, col2 = st.columns(2)  # Divide into two columns
    with col1:
        name = st.text_input("Nombre")
        rut = st.text_input("Rut")
        admission_date = st.date_input("Fecha de admisión")  # New admission date input
    with col2:
        age = st.number_input("Edad", min_value=0, max_value=120)
        gender = st.selectbox("Sexo", ["Male", "Female"])
        domicilio = st.selectbox("Domicilio",
                                 ["Curicó", "Molina", "Sagrada Familia", 'Romeral', 'Hualañe', 'Licantén', 'Rauco',
                                  'Teno', 'Vichuquén', 'Otro'])

    # Medical Details section
    st.subheader("Antecedentes médicos")
    col1, col2 = st.columns(2)
    with col1:
        alergias = st.text_input("Alergias")
        tabaquismo = st.selectbox("Tabaquismo", ["No", "Si"])
        fármacos = st.text_input("Medicamentos")
        aspirina = st.selectbox("Antiagregantes plaquetarios", ["No", "Si"])
        taco = st.selectbox("Anticoagulantes", ["No", "Si"])

    with col2:
        st.write("Antecedentes mórbidos")
        morbidos_options = ["Diabetes Mellitus NIR", "Diabetes Mellitus IR", "HTA", "Hipotiroidismo",
                            "Enfermedad renal crónica", "EPOC", "Asma Bronquial", "Daño hepático crónico",
                            "Cardiopatía Coronaria", "Insuficiencia cardíaca", "Arritmia"]
        morbidos_selections = {}
        for option in morbidos_options:
            morbidos_selections[option] = st.checkbox(option)

    st.subheader("Evolución clínica")
    col1, col2, col3 = st.columns(3)
    with col1:
        peso = st.number_input("Peso (kg)", min_value=0.0)
    with col2:
        blood_pressure = st.text_input("Presión arterial (sistólica/diastólica)")
    with col3:
        sat02 = st.text_input("Saturación O2")
    medical_history = st.text_area("Anamnesis")
    examen_fisico = st.text_area("Exámen físico")
    st.write("Escala de Glasgow")
    col1, col2, col3 = st.columns(3)
    with col1:
        ocular_options = ["O1", "O2", "O3", "O4"]
        ocular_selections = {}
        for option in ocular_options:
            ocular_selections[option] = st.checkbox(option)
    with col2:
        verbal_options = ["V1", "V2", "V3", "V4", "V5"]
        verbal_selections = {}
        for option in verbal_options:
            verbal_selections[option] = st.checkbox(option)
    with col3:
        motor_options = ["M1", "M2", "M3", 'M4', 'M5', "M6"]
        motor_selections = {}
        for option in motor_options:
            motor_selections[option] = st.checkbox(option)

    # Additional Details section
    st.subheader("Tratamiento")
    plan = st.text_area("Plan")
    col1, col2, col3 = st.columns(3)
    with col1:
        reposo = st.selectbox("Reposo",
                              ["Absoluto cero grados", 'Absoluto cabecera en 30 grados', 'Absoluto semisentado',
                               "Levantar asisitdo", "Relativo"])
        trombo = st.selectbox("Tromboprofilaxis farmacológica", ["No", "Si"])
    with col2:
        # Régimen section (nested within col2)
        st.write("Régimen nutricional")
        regimen_options = ["Cero", "Hídrico", "Blando", "Liviano", "Común", "Hiposódico", "Diabético", "Enteral"]
        regimen_selections = {}
        for option in regimen_options:
            regimen_selections[option] = st.checkbox(option)
    with col3:
        st.write("Equipo multidisciplinario")
        equipo_options = ["Kinesioterapia motora ", "Kinesioterapia respiratoria", "Fonoaudiología",
                          "Terapia Ocupacional", "Fisiatría"]
        equipo_selections = {}
        for option in equipo_options:
            equipo_selections[option] = st.checkbox(option)

    st.subheader("Indicaciones enfermería")
    col1, col2, col3 = st.columns(3)
    with col1:
        foley = st.selectbox("Retiro sonda foley", ['No', "Si"])
        cvc = st.selectbox("Retiro de CVC", ["No", "Si"])
    with col2:
        # Régimen section (nested within col2)
        curacion = st.selectbox("Curación por enfermería", ["No", "Si"])
        SNG = st.selectbox("Instalación sonda nasogástrica", ["No", "Si"])
    with col3:
        oxigeno = st.selectbox("Oxigenoterpia", ["No", "Bigotera", 'Mascarilla'])
        examenes = st.selectbox("Exámenes de laboratorio",
                                ["No", "Urgencia (orden amarilla)", 'Laboratorio (orden blanca)'])

    st.subheader("Firma médico")
    firma = st.selectbox("Neurocirujano",
                         ["Dr. Nicolás González Romo", "Dr. Patricio Giménez Hermosilla", "Dr.José Villamediana"])

    if st.button("Guardar"):
        # Process selections
        selected_regimens = [option for option, selected in regimen_selections.items() if selected]
        regimen_str = ", ".join(selected_regimens) if selected_regimens else "None selected"
        selected_equipo = [option for option, selected in equipo_selections.items() if selected]
        equipo_str = ", ".join(selected_equipo) if selected_equipo else "None selected"
        selected_morbidos = [option for option, selected in morbidos_selections.items() if selected]
        morbidos_str = ", ".join(selected_morbidos) if selected_morbidos else "None selected"

        # Process Glasgow scale
        ocular_score = next((key for key, value in ocular_selections.items() if value), "N/A")
        verbal_score = next((key for key, value in verbal_selections.items() if value), "N/A")
        motor_score = next((key for key, value in motor_selections.items() if value), "N/A")
        glasgow_score = f"Ocular: {ocular_score}, Verbal: {verbal_score}, Motor: {motor_score}"

        # Calculate hospitalization time
        hospitalization_time = (date - admission_date).days

        data = {
            "Nombre": name,
            "Rut": rut,
            "Edad": age,
            "Sexo": gender,
            "Domicilio": domicilio,
            "Fecha": date.strftime("%d-%m-%Y"),
            "Fecha de ingreso": admission_date.strftime("%d-%m-%Y"),
            "Días de hospitalización": f"{hospitalization_time} días",
            "Alergias": alergias,
            "Tabaquismo": tabaquismo,
            "Medicamentos": fármacos,
            "Antiagregantes plaquetarios": aspirina,
            "Anticoagulantes": taco,
            "Antecedentes mórbidos": morbidos_str,
            "Peso": f"{peso} kg",
            "Presión arterial": blood_pressure,
            "Saturación O2": sat02,
            "Anamnesis": medical_history,
            "Examen físico": examen_fisico,
            "Escala de Glasgow": glasgow_score,
            "Plan": plan,
            "Reposo": reposo,
            "Tromboprofilaxis farmacológica": trombo,
            "Régimen nutricional": regimen_str,
            "Equipo multidisciplinario": equipo_str,
            "Retiro sonda foley": foley,
            "Retiro de CVC": cvc,
            "Curación por enfermería": curacion,
            "Instalación sonda nasogástrica": SNG,
            "Oxigenoterapia": oxigeno,
            "Exámenes de laboratorio": examenes,
            "Firma médico": firma
        }

        filename = create_word_document(data)
        st.success(f"Archivo guardado: {filename}")
        st.download_button(
            label="Descargar documento Word",
            data=open(filename, "rb"),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


if __name__ == "__main__":
    main()