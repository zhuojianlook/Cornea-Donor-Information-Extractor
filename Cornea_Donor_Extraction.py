import streamlit as st
import pandas as pd
import pdfplumber
import re
from io import BytesIO

# Function to extract data from PDF using pdfplumber
def extract_data_from_pdf(pdf_file):
    # Initialize a dictionary with default values for all fields
    extracted_values = {
        "Tissue ID": "",
        "DIN": "",
        "Product Code": "",
        "Tissue Type": "",
        "Donor Age": "",
        "Primary COD": "",  # Added "Primary COD" field
        # Add default values for other fields here
    }

    try:
        # Initialize a PDF reader
        pdf = pdfplumber.open(pdf_file)

        for page in pdf.pages:
            # Extract text from the page
            page_text = page.extract_text()

            # Regular expression patterns for other fields (unchanged)
            patterns = {
                "Tissue ID": r"Tissue ID#?:\s?(?P<value>[\d-]+ LC)",
                "Tissue Type": r"Tissue Type:\s?(?P<value>Cornea)",
                "Donor Age": r"Donor Age:\s?(?P<value>\d+)",
                "Epithelium": r"Epithelium:\s?(?P<value>.+?)(?:\n|Descemet's)",
                "Stroma": r"Stroma:\s?(?P<value>.+?)(?:\n|Endothelium)",
                "Descemet's": r"Descemet's:\s?(?P<value>.+?)(?:\n|Endothelium)",
                "Endothelium": r"Endothelium:\s?(?P<value>.+?)(?:\n|Ocular)",
                "Donor Gender": r"Donor Gender:\s?(?P<value>\w+)",
                "Donor Race": r"Donor Race:\s?(?P<value>\w+)",
                "Primary COD": r"Primary COD:\s?(?P<value>CHF)(?![\w\s])",
                "Date-Time of Death": r"Date-Time of Death:\s?(?P<value>[\d-]+\s[\d:]+)",
                "Date-Time of In Situ": r"Date-Time of In Situ:\s?(?P<value>[\d-]+\s[\d:]+)",
                "Ocular Cooling": r"Ocular Cooling:\s?(?P<value>[\d-]+\s[\d:]+)",
                "Total": r"Total:\s?(?P<value>[\d:]+)",
                "Storage Media": r"Storage Media:\s?(?P<value>[\w-]+)",
                "Media Lot#": r"Media Lot#:\s?(?P<value>[\d-]+)",
                "Approved Usages": r"Approved Usages:\s?(?P<value>.+?)(?:\n)",
                "Lens Type": r"Lens Type:\s?(?P<value>[\w\s]+)",
                "Testing Facility": r"Testing Facility:\s?(?P<value>VRL Eurofins)(?![\w\s])",
                "Endothelial Cell Density": r"Endothelial Cell Density:\s?(?P<value>\d+)",
                "HBcAb (Total)": r"HBcAb \(Total\):\s?(?P<value>\w+)",
                "HCV Ab": r"HCV Ab:\s?(?P<value>\w+)",
                "HIV-1/HCV/HBV NAT (Ultrio)": r"HIV-1/HCV/HBV NAT \(Ultrio\):\s?(?P<value>\w+)",
                "HBsAg": r"HBsAg:\s?(?P<value>\w+)",
                "HIV 1&2 Ab": r"HIV 1&2 Ab:\s?(?P<value>\w+)",
                "RPR": r"RPR:\s?(?P<value>\w+)",
                "Recent hx": r"Recent hx:\s?(?P<value>.+?)(?:\n\n|\Z)"
                "Sars-Cov-2": r"Sars-Cov-2:\s?(?P<value>[\w\s]+)",
                "Antibodies to Cytomegalovirus (CMV)": r"Antibodies to Cytomegalovirus \(CMV\):\s?(?P<value>[\w\s]+)",
                "Toxoplasma IgG": r"Toxoplasma IgG:\s?(?P<value>[\w\s]+)",
                "EBV - Epstein-Barr (EB) Virus": r"EBV - Epstein-Barr \(EB\) Virus:\s?(?P<value>[\w\s]+)"
            }
            

            # Iterate through lines on the page
            lines = page_text.split("\n")
            for line in lines:
                for field, pattern in patterns.items():
                    match = re.search(pattern, line, re.DOTALL | re.IGNORECASE)
                    if match:
                        extracted_values[field] = match.group("value").strip()

            # # Special handling for "Tissue ID"
            # if not extracted_values["Tissue ID"]:
            #     if "Tissue ID" in page_text:
            #         index = page_text.index("Tissue ID")
            #         value = page_text[index + len("Tissue ID"):].strip().split("\n")[0]
            #         extracted_values["Tissue ID"] = value

            # Continue to extract other fields here

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    return extracted_values

# Streamlit interface (unchanged)
st.title("PDF Data Extractor")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            data = extract_data_from_pdf(uploaded_file)
            all_data.append(data)

    if st.button("Generate Excel"):
        df = pd.DataFrame(all_data)
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")
        excel_buffer.seek(0)
        st.write("### Download Excel File")
        st.download_button("Click to Download", excel_buffer, key="download_excel", file_name="data.xlsx")
