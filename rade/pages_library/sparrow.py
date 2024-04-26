import streamlit as st
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
from controllers.logs_controllers import Log
from database.database import *
import io
import cv2 as cv

class Sparrow:
    
    @classmethod
    def draw_canvas(self, img_file, ui_width):
        try:
            img_width, img_height = img_file.size
            
            if img_width > img_height:
                canva_w = 900
                canva_h = 1280
            else:
                canva_w = 1280
                canva_h = 900
                    
            initial_rect = {
                "meta": {
                    "version": "v0.1",
                    "split": "train",
                    "image_id": 1,
                    "image_size": {
                        "width": canva_w,
                        "height": canva_h
                    }
                },
                "words": []
            }

            height = initial_rect['meta']['image_size']['width']
            width = initial_rect['meta']['image_size']['height']
            width_org, height_org = img_file.size

            proportion = self.map_proportion(width_org, height_org, width, height)

            assign_labels = st.checkbox("Adicionar Campos", True)
            mode = "transform" if not assign_labels else "rect"

            data_processor = DataProcessor()

            canvas_width = ui_width/2.1

            result_rects = st_sparrow_labeling(
                fill_color="rgba(0, 151, 255, 0.3)",
                stroke_width=1,
                stroke_color="rgba(0, 50, 255, 0.7)",
                background_image=img_file,
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
        
            return proportion, data_processor, result_rects
        except Exception as e:
            Log.insert_system_log(e)
            return False
    
    
    @classmethod
    def run_scan(self, img_file):
        try:
            col1, col2 = st.columns([1, 1])
            ui_width = st_js.st_javascript("window.innerWidth", key='uiwidth1')

            with col1: 
                proportion, data_processor, result_rects = self.draw_canvas(img_file, ui_width)
            
            with col2:
                if result_rects is not None:
                    with st.form(key="fields_form_scan"):

                        for i, rect in enumerate(result_rects.rects_data['words']):
                            label = st.text_input("Rótulo", key=f"label_{i}", disabled=False if i == result_rects.current_rect_index else True)
                            st.markdown("---")
                            data_processor.update_rect_data(result_rects.rects_data, i, [], label)

                        if st.form_submit_button("Escanear", type="primary"):
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
                                Log.insert_system_log(e)
        except Exception as e:
            Log.insert_system_log(e)
                            

    @classmethod
    def run_save(self, img_file, model):
        try:
            col1, col2 = st.columns([1, 1])
            ui_width = st_js.st_javascript("window.innerWidth", key='uiwidth1')

            with col1:
                proportion, data_processor, result_rects = self.draw_canvas(img_file, ui_width)

            with col2:
                if result_rects is not None:
                    with st.form(key="fields_form_models"):
                        for i, rect in enumerate(result_rects.rects_data['words']):
                            label = st.text_input("Rótulo", key=f"label_{i}", disabled=False if i == result_rects.current_rect_index else True)
                            st.markdown("---")
                            data_processor.update_rect_data(result_rects.rects_data, i, [], label)

                        if st.form_submit_button("Salvar", type="primary"):
                            if model != '':
                                with Session(bind=engine) as session:
                                    try:
                                        buffer = io.BytesIO()
                                        img_file.save(buffer, format='PNG')
                                        img_bytes = buffer.getvalue()
                                        rois = []

                                        for rect in result_rects.rects_data['words']:
                                            p1 = (int(rect['rect']['x1'] * proportion[0]), int(rect['rect']['y1'] * proportion[1]))
                                            p2 = (int(rect['rect']['x2'] * proportion[0]), int(rect['rect']['y2'] * proportion[1]))
                                            roi = [str(p1), str(p2)]
                                            roi.append(rect['label'])
                                            rois.append(roi)


                                        session.add(OcrConfig(name=model, img=img_bytes, rois=rois))
                                        session.commit()
                                        st.success('Modelo Salvo!')
                                        
                                    except Exception as e:
                                        session.rollback()
                                        Log.insert_system_log(e)
                            else:
                                st.warning('Título Vazio!')
        except Exception as e:
            Log.insert_system_log(e)


    @classmethod
    def map_proportion(self, width_org, height_org, width_new, heigt_new):
        try:
            proportion_w = width_org / width_new
            proportion_h = height_org / heigt_new
            return [proportion_w, proportion_h]
        except Exception as e:
            Log.insert_system_log(e)
            return False

