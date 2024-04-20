from PIL import Image
import streamlit as st
import streamlit_nested_layout
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
from projeto_ciclo1.database.database import *
import math
import io

def run(img_file):
    initial_rect = {
        "meta": {
            "version": "v0.1",
            "split": "train",
            "image_id": 1,
            "image_size": {
                "width": 1280,
                "height": 900
            }
        },
        "words": []
    }
    
    ui_width = st_js.st_javascript("window.innerWidth")

    docImg = Image.open(img_file)
    height = initial_rect['meta']['image_size']['width']
    width = initial_rect['meta']['image_size']['height']
    with_org, height_org = docImg.size
    
    proportion = map_proportion(with_org, height_org, width, height)
    
    assign_labels = st.checkbox("Adicionar Campos", True)
    mode = "transform" if not assign_labels else "rect"

    data_processor = DataProcessor()

    col1, col2 = st.columns([1, 1])

    with col1:
    
        canvas_width = ui_width/2
        
        result_rects = st_sparrow_labeling(
            fill_color="rgba(0, 151, 255, 0.3)",
            stroke_width=1,
            stroke_color="rgba(0, 50, 255, 0.7)",
            background_image=docImg,
            initial_rects=initial_rect,
            height=height,
            width=width,
            drawing_mode=mode,
            display_toolbar=False,
            update_streamlit=True,
            canvas_width=canvas_width,
            doc_height=height,
            doc_width=width,
            image_rescale=True,
            key="doc_annotation"
        )
        
        # st.caption("Check 'Assign Labels' to enable editing of labels and values, move and resize the boxes to "
        #            "annotate the document.")
       

    with col2:
        if result_rects is not None:
            with st.form(key="fields_form_scan"):

                for i, rect in enumerate(result_rects.rects_data['words']):
                    
                    label = st.text_input("Rótulo", key=f"label_{i}", disabled=False if i == result_rects.current_rect_index else True)
                    
                    st.markdown("---")
                    data_processor.update_rect_data(result_rects.rects_data, i, [], label)

                btn = st.form_submit_button("Scan", type="secondary")
                if btn:
                    try:
                        rois = []
                        for i, rect in enumerate(result_rects.rects_data['words']):
                            p1 = (int(rect['rect']['x1'] * proportion[0]),int(rect['rect']['y1'] * proportion[1]))
                            p2 = (int(rect['rect']['x2'] * proportion[0]),int(rect['rect']['y2'] * proportion[1]))
                            roi = [p1, p2]
                            roi.append(rect['label'])
                            rois.append(roi)
                        
                        st.session_state.rois = rois
                    except Exception as e:
                        print(e)
    
    

def canvas_available_width(ui_width):
    # Get ~40% of the available width, if the UI is wider than 500px
    if ui_width > 500:
        return math.floor(38 * ui_width / 100)
    else:
        return ui_width

def map_proportion(width_org, height_org, width_new, heigt_new):
    proportion_w = width_org / width_new
    proportion_h = height_org / heigt_new
    
    return [proportion_w, proportion_h]

