import streamlit as st
from extraction_code_manual import extract_layout_updated, heuristic_extract_values_from_text, refined_extract_tissue_id, bounding_boxes_6436
import pandas as pd
import io

def streamlit_app():
    st.title("PDF Data Extractor")

    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        extracted_data_list = []

        for uploaded_file in uploaded_files:
            # Read the uploaded file's content into a BytesIO stream
            file_content = io.BytesIO(uploaded_file.read())
            
            layout_data = extract_layout_updated(file_content)
            extracted_text = [entry["text"] for entry in layout_data]
            
            extracted_values = heuristic_extract_values_from_text(extracted_text)
            extracted_data_list.append(extracted_values)

        extracted_df = pd.DataFrame(extracted_data_list)
        st.write(extracted_df)

        
streamlit_app()
