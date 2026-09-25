import sys
from pathlib import Path

# streamlit only puts app/ on the path, add the repo root so `src` resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from PIL import Image
from src import detector, mapping

# ---- defensive: teammates' modules may still be empty stubs ----
try:
    from src.annotate import annotateImage
except ImportError:
    def annotateImage(img, dets):
        return img

if not hasattr(detector, "DEFAULT_VOCAB"):
    detector.DEFAULT_VOCAB = []
if not hasattr(detector, "DEFAULT_CONF"):
    detector.DEFAULT_CONF = 0.10
if not hasattr(detector, "predict"):
    def _noop_predict(img, conf=0.1):
        return []
    detector.predict = _noop_predict

if not hasattr(mapping, "map_waste_item"):
    def _noop_map(cls):
        return ("Unsure", "Unsure", "Check the bin label, or use general waste.")
    mapping.map_waste_item = _noop_map

st.set_page_config(page_title="SortSmart", page_icon="🥀", layout="wide")

FLAG_STYLES = {
    "Recyclable": ("♻️", "#0b7a3b", "#e6f4ea"),
    "General":    ("🗑️", "#3f4a52", "#eceff1"),
    "Special":    ("⚠️", "#7a5c00", "#fdf3d8"),
    "Unsure":     ("❓", "#8a1c1c", "#fdecea"),
}


def flag_badge(flag):
    icon, fg, bg = FLAG_STYLES.get(flag, FLAG_STYLES["Unsure"])
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:999px;font-size:0.8rem;font-weight:600;">'
        f'{icon} {flag}</span>'
    )


with st.sidebar:
    st.header("Model")
    st.write(f"**Classes:** {len(detector.DEFAULT_VOCAB)}")
    st.write(f"**Default confidence:** {detector.DEFAULT_CONF}")
    st.divider()
    threshold = st.slider(
        "Confidence threshold",
        min_value=0.05,
        max_value=0.5,
        value=float(detector.DEFAULT_CONF),
        step=0.05,
    )

st.title("SortSmart")
st.caption("Point at your rubbish — we'll tell you which bin each item goes in.")

f = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
shot = st.camera_input("Or take a photo")

img = None
if shot is not None:
    img = Image.open(shot).convert("RGB")
elif f is not None:
    img = Image.open(f).convert("RGB")

if img is None:
    st.info("Upload a photo or take one with your camera to get started.")
    st.stop()

with st.spinner("Analysing…"):
    detections = detector.predict(img, conf=threshold)
    annotated = annotateImage(img, detections)

img_col, list_col = st.columns([1, 1], gap="large")

with img_col:
    st.image(annotated, caption="Your photo", use_container_width=True)

with list_col:
    img_key = hash(img.tobytes())
    if st.session_state.get("last_img_key") != img_key:
        st.session_state["last_img_key"] = img_key
        st.session_state["items_sorted"] = (
            st.session_state.get("items_sorted", 0) + len(detections)
        )

    st.metric("Items sorted (session)", st.session_state["items_sorted"])
    st.subheader(f"Items detected ({len(detections)})")

    if not detections:
        st.warning("Couldn't spot anything — try a clearer photo.")
    else:
        for n, det in enumerate(detections, start=1):
            binType, flag, tip = mapping.map_waste_item(det["class"])
            with st.container(border=True):
                left, right = st.columns([3, 2])
                with left:
                    st.markdown(f"**{n}. {det['class'].title()}**")
                with right:
                    st.markdown(
                        f'<div style="text-align:right;">**{binType}**</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(flag_badge(flag), unsafe_allow_html=True)
                st.caption(f"💡 {tip}  ·  confidence {det['conf']:.0%}")
