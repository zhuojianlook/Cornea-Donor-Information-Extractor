import streamlit as st
import pandas as pd
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LAParams

def extract_layout_updated(pdf_path):
    layout_data = []
    for page_layout in extract_pages(pdf_path, laparams=LAParams(line_margin=0.1)):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                st.write(f"Extracted Text: {text}")  # Add this line to print the text to Streamlit
                for char in element:
                    if isinstance(char, LTChar):
                        layout_data.append({
                            "text": text,
                            "x0": char.bbox[0],
                            "y0": char.bbox[1],
                            "x1": char.bbox[2],
                            "y1": char.bbox[3]
                        })
                        break
    return layout_data


def hybrid_extract_values(layout_data, extracted_text):
    extracted_values = {}
    for field, bbox in bounding_boxes_6436.items():
        potential_values = []
        distance_constraint = 80 if field in ["Epithelium", "Stroma", "Descemet's", "Endothelium"] else 150
        for entry in layout_data:
            if (entry["x0"] > bbox["x1"] and entry["x0"] - bbox["x1"] < distance_constraint and 
                (entry["y0"] <= bbox["y1"] and entry["y1"] >= bbox["y0"]) and 
                entry["x0"] > bbox["x1"]):
                potential_values.append(entry["text"])
        if potential_values:
            combined_value = " ".join(potential_values)
            extracted_values[field] = None if combined_value in ["N/A", "NA", "None"] else combined_value
        else:
            extracted_values[field] = None
            st.warning(f"Couldn't find value for field: {field}")
    return extracted_values


def refined_extract_tissue_id(layout_data, bbox):
    potential_values = []
    for entry in layout_data:
        if (entry["x0"] > bbox["x1"] and entry["x0"] - bbox["x1"] < 150 and 
            (entry["y0"] <= bbox["y1"] and entry["y1"] >= bbox["y0"]) and 
            entry["x0"] > bbox["x1"]):
            potential_values.append(entry["text"])
    return potential_values[0] if potential_values else None

bounding_boxes_6436 = {}
bounding_boxes_6436["Tissue ID"] = {'x0': 210.0, 'y0': 756.27256965, 'x1': 250.083, 'y1': 766.454698545}
bounding_boxes_6436["Tissue Type"] = {'x0': 298.5, 'y0': 679.2158203125, 'x1': 360.444, 'y1': 691.09497069}
bounding_boxes_6436["Donor Age"] = {'x0': 32.25, 'y0': 603.720703125, 'x1': 79.089, 'y1': 613.749023424}
bounding_boxes_6436["Donor Gender"] = {'x0': 32.25, 'y0': 591.720703125, 'x1': 93.339, 'y1': 601.749023424}
bounding_boxes_6436["Donor Race"] = {'x0': 32.25, 'y0': 579.720703125, 'x1': 83.589, 'y1': 589.749023424}
bounding_boxes_6436["Primary COD"] = {'x0': 297.75, 'y0': 603.720703125, 'x1': 354.339, 'y1': 613.749023424}
bounding_boxes_6436["Date-Time of Death"] = {'x0': 32.25, 'y0': 567.720703125, 'x1': 118.839, 'y1': 577.749023424}
bounding_boxes_6436["Date-Time of In Situ"] = {'x0': 32.25, 'y0': 555.720703125, 'x1': 121.839, 'y1': 565.749023424}
bounding_boxes_6436["Ocular Cooling"] = {'x0': 297.75, 'y0': 591.720703125, 'x1': 361.839, 'y1': 601.749023424}
bounding_boxes_6436["Total"] = {'x0': 297.75, 'y0': 579.720703125, 'x1': 322.089, 'y1': 589.749023424}
bounding_boxes_6436["Storage Media"] = {'x0': 297.75, 'y0': 543.720703125, 'x1': 361.089, 'y1': 553.749023424}
bounding_boxes_6436["Media Lot#"] = {'x0': 297.75, 'y0': 531.720703125, 'x1': 347.589, 'y1': 541.749023424}
bounding_boxes_6436["Approved Usages"] = {'x0': 32.25, 'y0': 414.720703125, 'x1': 108.339, 'y1': 424.749023424}
bounding_boxes_6436["Lens Type"] = {'x0': 348.75, 'y0': 380.220703125, 'x1': 397.839, 'y1': 390.249023424}
bounding_boxes_6436["Epithelium"] = {'x0': 32.25, 'y0': 350.220703125, 'x1': 79.089, 'y1': 360.249023424}
bounding_boxes_6436["Stroma"] = {'x0': 32.25, 'y0': 338.220703125, 'x1': 65.589, 'y1': 348.249023424}
bounding_boxes_6436["Descemet's"] = {'x0': 32.25, 'y0': 326.220703125, 'x1': 83.589, 'y1': 336.249023424}
bounding_boxes_6436["Endothelium"] = {'x0': 32.25, 'y0': 314.220703125, 'x1': 87.339, 'y1': 324.249023424}
bounding_boxes_6436["Testing Facility"] = {'x0': 32.25, 'y0': 56.220703125, 'x1': 100.083, 'y1': 66.249023424}
