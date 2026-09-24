import sys
from pathlib import Path

# streamlit only puts app/ on the path, add the repo root so `src` resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from src import detector, mapping
from src.annotate import annotateImage

st.set_page_config(page_title="SortSmart", page_icon="🥀", layout="wide")

# title: st.title("SortSmart") + a short caption under it

# sidebar (st.sidebar): model info + threshold
#   - vocab size: len(detector.DEFAULT_VOCAB) items
#   - default threshold: detector.DEFAULT_CONF (0.10)
#   - slider: st.slider("confidence threshold", 0.05, 0.5, detector.DEFAULT_CONF, 0.05)

# inputs: st.file_uploader("upload a photo", type=["jpg", "jpeg", "png"])
#         st.camera_input("or take a photo")
#   camera wins if both are set

# pipeline once we have an image (PIL):
#   detections = detector.predict(img, conf=threshold)  # -> [{class, conf, box}, ...]
#   st.image(annotateImage(img, detections))            # draws the boxes on it

# per-item cards, inside st.container(border=True):
#   binType, flag, tip = mapping.map_waste_item(det["class"])
#   -> class name, conf %, flag badge (green if Recyclable), **binType**, prep tip

# counter: st.metric("items sorted", ...) backed by st.session_state
#   only count each photo once — streamlit reruns the whole script on every
#   click/slider drag, so key off the uploaded image bytes

# edge cases:
#   no image chosen -> friendly st.info to get people started
#   0 detections    -> st.warning "couldn't spot anything, try a clearer photo"
