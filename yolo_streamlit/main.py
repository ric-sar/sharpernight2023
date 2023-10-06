import streamlit as st

import tkinter

import cv2
from pygrabber.dshow_graph import FilterGraph

from ultralytics import YOLO
import torch

def get_camera():
    devices = FilterGraph().get_input_devices()
    camera_dict = {}

    for i, name in enumerate(devices):
        camera_dict[name] = i

    return camera_dict

def get_screen_width():
    app = tkinter.Tk()
    screen_width = app.winfo_screenwidth()
   
    return screen_width/2-100

# Page title
st.set_page_config(page_title="SHARPER Night 2023", page_icon = "./logo/perceive_lab_favicon.ico", layout="wide")

# Hide menu, deploy button, full screen button and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
button[title="View fullscreen"]{visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Sidebar
st.sidebar.image("./logo/perceive_lab_logo.png", use_column_width="always")
st.sidebar.title("Segment and Pose for SHARPER Night 2023")
st.sidebar.markdown('Made with :heart: in [PeRCeiVe Lab](http://www.perceivelab.com)')

camera_device = st.sidebar.selectbox("Select camera device", options=get_camera().keys(), placeholder="-")
start_button = st.sidebar.button("Start")

if start_button:
    stop_button_pressed = st.sidebar.button("Stop capturing")

    screen_width = get_screen_width()
    image_placeholder = st.empty()
    
    with st.spinner("Loading YOLO models..."):
        model = "n"
        inference_device = "cuda" if torch.cuda.is_available() else "cpu"
        segment = YOLO(f"yolov8{model}-seg.pt").to(inference_device)
        pose = YOLO(f"yolov8{model}-pose.pt").to(inference_device)

    with st.spinner("Starting camera device..."):
        cap = cv2.VideoCapture(get_camera()[camera_device])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("The video capture has ended")
            break

        frame = cv2.flip(frame, 1)

        # Inference
        res_segment = segment.predict(source=frame)
        pose_segment = pose.predict(source=frame)
        
        # Plot
        segment_frame = res_segment[0].plot(labels=True, line_width=3)
        pose_frame = pose_segment[0].plot(labels=False)
        image_placeholder.image(image=[segment_frame, pose_frame], width=screen_width, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
            cap.release()
            cv2.destroyAllWindows()
            break
