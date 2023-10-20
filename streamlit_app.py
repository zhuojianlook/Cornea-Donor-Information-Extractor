import streamlit as st
from extraction_code_manual import extract_layout_updated, final_refined_extract_values_from_regions, refined_extract_tissue_id, bounding_boxes_6436
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
            
            # Display extracted layout data for troubleshooting
            st.subheader(f"Extracted Layout Data for {uploaded_file.name}")
            st.write(pd.DataFrame(layout_data).head(10))  # Displaying first 10 rows for brevity
            
            st.subheader("Using Bounding Boxes:")
            st.write(bounding_boxes_6436)
            
            extracted_values = final_refined_extract_values_from_regions(layout_data, bounding_boxes_6436)
            extracted_values["Tissue ID"] = refined_extract_tissue_id(layout_data, bounding_boxes_6436["Tissue ID"])
            extracted_data_list.append(extracted_values)

        extracted_df = pd.DataFrame(extracted_data_list)
        st.subheader("Final Extracted Data")
        st.write(extracted_df)

        # Provide option to download the extracted data as Excel
        towrite = io.BytesIO()
        extracted_df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)
        st.download_button("Download Extracted Data", towrite, "extracted_data.xlsx")

streamlit_app()
