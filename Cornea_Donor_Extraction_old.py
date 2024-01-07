import streamlit as st
import pandas as pd
import pdf2image
import pytesseract
import re
import os
from io import BytesIO
from PIL import Image
from tempfile import NamedTemporaryFile

# Function to extract data from PDF
def extract_data_from_pdf(pdf_path):
    # Convert PDF to images
    images = pdf2image.convert_from_path(pdf_path)
    # Extract text from the images using OCR
    ocr_texts = [pytesseract.image_to_string(img) for img in images]

    # Regular expression patterns for extracting values
    patterns = {
        "Tissue ID": r"Tissue\s?ID[:#]?\s?(?P<value>[\d-]+[\s\w]+)",
        "DIN": r"DIN:\s?(?P<value>W\d{4}\s\d{2}\s\d{6})",
        "Product Code": r"Product Code:\s?(?P<value>V\d{7})",
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
        "Media Lot#": r"Media Lot#[:\s]?\s?(?P<value>[\d\w-]+)",
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
    }

    # Extract values using the patterns
    extracted_values = {}
    for field, pattern in patterns.items():
        for text in ocr_texts:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                extracted_values[field] = match.group("value").strip()
                break

    return extracted_values

# Streamlit interface
st.title("Donor Cornea PDF Data Extractor")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        # Create a temporary file to save the uploaded PDF
        with st.spinner(f"Processing {uploaded_file.name}..."):
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
            data = extract_data_from_pdf(temp_file.name)
            all_data.append(data)

    if st.button("Generate Excel"):
        df = pd.DataFrame(all_data)

        # Save the DataFrame to an in-memory Excel file
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")
        excel_buffer.seek(0)

        # Offer the Excel file for download
        st.write("### Download Excel File")
        st.download_button("Click to Download", excel_buffer, key="download_excel", file_name="data.xlsx")
