from PIL import Image
import streamlit as st
import streamlit_nested_layout
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
from projeto_ciclo1.database.database import *
import math
import io

def run(img_file, model):
    initial_rect = {
        "meta": {
            "version": "v0.1",
            "split": "train",
            "image_id": 1,
            "image_size": {
                "width": 1280,
                "height": 850
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
    
    assign_labels = st.checkbox("Assign Labels", True)
    mode = "transform" if assign_labels else "rect"

    data_processor = DataProcessor()

    col1, col2 = st.columns([4, 6])

    with col1:
        

        canvas_width = canvas_available_width(ui_width)
        
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
        
        st.caption("Check 'Assign Labels' to enable editing of labels and values, move and resize the boxes to "
                   "annotate the document.")
        st.caption(
            "Add annotations by clicking and dragging on the document, when 'Assign Labels' is unchecked.")

    with col2:
        if result_rects is not None:
            with st.form(key="fields_form"):
                if result_rects.current_rect_index is not None and result_rects.current_rect_index != -1:
                    st.write("Selected Field: ",
                             result_rects.rects_data['words'][result_rects.current_rect_index]['value'])
                    st.markdown("---")

                if ui_width > 1500:
                    render_form_wide(
                        result_rects.rects_data['words'], result_rects, data_processor, proportion)
                elif ui_width > 1000:
                    render_form_avg(
                        result_rects.rects_data['words'], result_rects, data_processor, proportion)
                elif ui_width > 500:
                    render_form_narrow(
                        result_rects.rects_data['words'], result_rects, data_processor, proportion)
                else:
                    render_form_mobile(
                        result_rects.rects_data['words'], result_rects, data_processor, proportion)

                submit = st.form_submit_button("Save", type="primary")
                if submit:
                    with Session(bind=engine) as session:
                        try:
                            # enviar url da imagem
                            buffer = io.BytesIO()
                            # Você pode ajustar o formato conforme necessário
                            docImg.save(buffer, format='PNG')
                            img_bytes = buffer.getvalue()
                            rois = []
                            
                            for dic in result_rects.rects_data['words']:
                                roi = dic['value']
                                roi.append(dic['label'])
                                rois.append(roi)
                                
                            session.add(OcrConfig(name=model, img=img_bytes, rois=rois))
                            session.commit()
                            st.balloons()
                        except Exception as e:
                            session.rollback()
                            print(e)

def render_form_wide(words, result_rects, data_processor, proportion):
    col1_form, col2_form, col3_form, col4_form = st.columns([1, 1, 1, 1])
    num_rows = math.ceil(len(words) / 4)

    for i, rect in enumerate(words):
        if i < num_rows:
            with col1_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)
        elif i < num_rows * 2:
            with col2_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)
        elif i < num_rows * 3:
            with col3_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)
        else:
            with col4_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)


def render_form_avg(words, result_rects, data_processor, proportion):
    col1_form, col2_form, col3_form = st.columns([1, 1, 1])
    num_rows = math.ceil(len(words) / 3)

    for i, rect in enumerate(words):
        if i < num_rows:
            with col1_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)
        elif i < num_rows * 2:
            with col2_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)
        else:
            with col3_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)


def render_form_narrow(words, result_rects, data_processor, proportion):
    col1_form, col2_form = st.columns([1, 1])
    num_rows = math.ceil(len(words) / 2)

    for i, rect in enumerate(words):
        if i < num_rows:
            with col1_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)
        else:
            with col2_form:
                render_form_element(
                    rect, i, result_rects, data_processor, proportion)


def render_form_mobile(words, result_rects, data_processor, proportion):
    for i, rect in enumerate(words):
        render_form_element(rect, i, result_rects, data_processor, proportion)


def render_form_element(rect, i, result_rects, data_processor, proportion):

    value1 = st.text_input("Ponto A", (int(rect['rect']['x1'] * proportion[0]) , int(rect['rect']['y1'] * proportion[1])), key=f"field_value_a_{i}",
                           disabled=True)
    value2 = st.text_input("Ponto B", (int(rect['rect']['x2'] * proportion[0]), int(rect['rect']['y2'] * proportion[1])), key=f"field_value_b_{i}",
                           disabled=True)
    label = st.text_input("Rótulo", key=f"label_{i}", disabled=False if i == result_rects.current_rect_index else True)
    st.markdown("---")

    data_processor.update_rect_data(result_rects.rects_data, i, [value1, value2], label)
    


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

