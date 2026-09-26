import io
import sys
from pathlib import Path

# streamlit only puts app/ on the path, add the repo root so `src` resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from PIL import Image
from src import detector, mapping
from src.annotate import annotateImage

st.set_page_config(page_title="SortSmart", page_icon="♻️", layout="wide")

# weights are gitignored, so a fresh clone won't have them
WEIGHTS_DIR = Path(__file__).resolve().parent.parent / "weights"

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f6faf7 0%, #eef5ef 100%); }
[data-testid="stSidebar"] { background: #fbfdfb; border-right: 1px solid #e6efe8; }
.main .block-container { padding-bottom: 6.5rem !important; }

.hero {
    background: linear-gradient(135deg, #0b7a3b 0%, #12a355 100%);
    color: #fff; padding: 2.2rem 2rem 1.8rem 2rem;
    border-radius: 20px; margin-bottom: 1.75rem;
    box-shadow: 0 10px 30px rgba(11,122,59,0.20);
}
.hero h1 { margin: 0; font-size: 2.3rem; font-weight: 800; letter-spacing: -0.02em; }
.hero p { margin: 0.5rem 0 0 0; opacity: 0.92; font-size: 1rem; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.itemCard {
    background: #fff; border-radius: 14px; padding: 1rem 1.15rem;
    margin-bottom: 0.75rem; border-left: 6px solid #ccc;
    box-shadow: 0 2px 10px rgba(20,40,30,0.06);
    transition: transform 0.14s ease, box-shadow 0.14s ease;
    animation: fadeInUp 0.42s ease backwards;
}
.itemCard:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(20,40,30,0.12); }
.itemCard .name { font-weight: 700; font-size: 1.05rem; color: #1c2b22; display: flex; align-items: center; gap: 0.5rem; }
.itemCard .tip  { color: #4b5a52; font-size: 0.9rem; margin-top: 0.65rem; line-height: 1.35; }
.itemCard .classIcon { font-size: 1.4rem; line-height: 1; }

.pill { display: inline-block; padding: 3px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; white-space: nowrap; }
.pillBin { background: #eef1f4; color: #3f4a52; }
.pillFlag { color: #fff; }

.progress { background: #eef1f4; height: 6px; border-radius: 999px; overflow: hidden; margin-top: 0.55rem; }
.progressFill { height: 100%; background: linear-gradient(90deg, #0b7a3b, #12a355); border-radius: 999px; transition: width 0.45s ease; }
.progressLabel { display: flex; justify-content: space-between; font-size: 0.72rem; color: #8a978f; margin-top: 0.3rem; }

.statTile { background: #fff; border-radius: 14px; padding: 0.95rem 0.8rem; text-align: center; box-shadow: 0 2px 10px rgba(20,40,30,0.06); }
.statTile .num { font-size: 1.9rem; font-weight: 800; line-height: 1; color: #0b7a3b; }
.statTile .label { font-size: 0.72rem; color: #5a6b62; margin-top: 0.35rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }

.emptyState { background: #fff; border: 2px dashed #cfdcd2; border-radius: 18px; padding: 2.2rem 1.5rem; text-align: center; color: #4b5a52; }
.emptyState .emoji { font-size: 2.6rem; display: block; margin-bottom: 0.6rem; }
.emptyState h4 { margin: 0 0 0.4rem 0; color: #1c2b22; font-size: 1.15rem; }
.emptyState ul { display: inline-block; text-align: left; margin-top: 0.5rem; color: #5a6b62; font-size: 0.92rem; }

.bottomBar {
    position: fixed; left: 0; right: 0; bottom: 0;
    background: rgba(255,255,255,0.92); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid #e6efe8; box-shadow: 0 -6px 24px rgba(20,40,30,0.08);
    padding: 0.7rem 1.5rem; z-index: 999;
    display: flex; align-items: center; justify-content: space-between; font-size: 0.9rem;
}
.bottomBar .bbLabel { color: #4b5a52; font-weight: 600; }
.bottomBar .bbNum { font-size: 1.4rem; font-weight: 800; color: #0b7a3b; line-height: 1; }
.bottomBar .bbRight { display: flex; align-items: baseline; gap: 0.45rem; }
.bottomBar .bbUnit { color: #8a978f; font-size: 0.82rem; }

label[data-testid="stWidgetLabel"] p { font-weight: 600; color: #2a3a30; }

@media (prefers-color-scheme: dark) {
    .stApp { background: linear-gradient(180deg, #0e1411 0%, #080c0a 100%); color: #e8f0ea; }
    [data-testid="stSidebar"] { background: #131a15; border-right: 1px solid #1f2a23; }
    [data-testid="stSidebar"] * { color: #d8e4dc; }
    .hero { box-shadow: 0 10px 30px rgba(11,122,59,0.35); }
    .itemCard { background: #18211a; box-shadow: 0 2px 10px rgba(0,0,0,0.5); color: #e8f0ea; }
    .itemCard:hover { box-shadow: 0 8px 22px rgba(0,0,0,0.65); }
    .itemCard .name { color: #eef5ef; }
    .itemCard .tip  { color: #a3b3a8; }
    .pillBin { background: #232e26; color: #c6d4ca; }
    .progress { background: #232e26; }
    .progressLabel { color: #839588; }
    .statTile { background: #18211a; box-shadow: 0 2px 10px rgba(0,0,0,0.5); }
    .statTile .label { color: #97a89c; }
    .statTile .num { color: #34c46f; }
    .emptyState { background: #141c16; border-color: #2a3a30; color: #a3b3a8; }
    .emptyState h4 { color: #eef5ef; }
    .emptyState ul { color: #97a89c; }
    .bottomBar { background: rgba(19,26,21,0.92); border-top: 1px solid #1f2a23; box-shadow: 0 -6px 24px rgba(0,0,0,0.5); }
    .bottomBar .bbLabel { color: #c6d4ca; }
    .bottomBar .bbNum { color: #34c46f; }
    .bottomBar .bbUnit { color: #839588; }
    label[data-testid="stWidgetLabel"] p { color: #c6d4ca; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- Data maps ----------------
FLAGS = {
    "Recyclable": {"icon": "♻️", "bg": "#0b7a3b"},
    "General":    {"icon": "🗑️", "bg": "#3f4a52"},
    "Special":    {"icon": "⚠️", "bg": "#c98a00"},
    "Unsure":     {"icon": "❓", "bg": "#8a1c1c"},
}

CLASS_ICONS = {
    "bottle": "🍾", "cup": "🥤", "wine glass": "🍷",
    "fork": "🍴", "knife": "🔪", "spoon": "🥄", "bowl": "🥣",
    "banana": "🍌", "apple": "🍎", "orange": "🍊",
    "sandwich": "🥪", "pizza": "🍕", "carrot": "🥕", "broccoli": "🥦",
    "beverage can": "🥫", "book": "📖", "paper": "📄",
    "cell phone": "📱", "keyboard": "⌨️", "mouse": "🖱️",
    "remote": "📺", "scissors": "✂️",
    "teddy bear": "🧸", "handbag": "👜", "backpack": "🎒",
    "umbrella": "☂️", "vase": "🏺", "clock": "🕐",
}

def classIcon(label):
    return CLASS_ICONS.get(label.lower().strip(), "📦")

# ---------------- Caching ----------------
# inference is cached on image bytes so slider drags don't re-run the model
@st.cache_data(show_spinner=False, max_entries=8)
def cachedPredict(imgBytes: bytes):
    img = Image.open(io.BytesIO(imgBytes)).convert("RGB")
    return detector.predict(img, conf=0.0)

# ---------------- Renderers ----------------
def renderCard(n, det, info):
    flag = info.get("flag", "Unsure")
    f = FLAGS.get(flag, FLAGS["Unsure"])
    binType = info.get("bin_type", "Unsure")
    tip = info.get("tip", "Check local rules.")
    confPct = max(0, min(100, int(det.get("conf", 0) * 100)))
    icon = classIcon(det["class"])
    delay = min(n - 1, 8) * 0.05

    st.markdown(f"""
    <div class="itemCard" style="border-left-color: {f['bg']}; animation-delay: {delay:.2f}s;">
        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem;">
            <div class="name"><span class="classIcon">{icon}</span>{det['class'].title()}</div>
            <div class="pill pillBin">{binType}</div>
        </div>
        <div style="margin-top:0.55rem; display:flex; gap:0.6rem; align-items:center;">
            <span class="pill pillFlag" style="background:{f['bg']};">{f['icon']} {flag}</span>
        </div>
        <div class="progress"><div class="progressFill" style="width:{confPct}%;"></div></div>
        <div class="progressLabel"><span>confidence</span><span>{confPct}%</span></div>
        <div class="tip">💡 {tip}</div>
    </div>
    """, unsafe_allow_html=True)


def statTile(num, label):
    return f"""
    <div class="statTile">
        <div class="num">{num}</div>
        <div class="label">{label}</div>
    </div>
    """

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### ♻️ SortSmart")
    st.caption("AI recycling assistant")
    st.divider()
    st.markdown("**Model**")
    st.markdown(
        f"- Classes: `{len(detector.DEFAULT_VOCAB)}`\n"
        f"- Default confidence: `{detector.DEFAULT_CONF}`"
    )
    st.divider()
    threshold = st.slider(
        "Confidence threshold",
        min_value=0.05, max_value=0.5,
        value=float(detector.DEFAULT_CONF), step=0.05,
        help="Detections scoring below this are hidden.",
    )

# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
    <h1>♻️ SortSmart</h1>
    <p>Point at your rubbish — we'll tell you which bin each item goes in.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Weights check ----------------
# weights/ is gitignored, so a fresh clone has no .pt file — fail loudly, not silently
if not (WEIGHTS_DIR.is_dir() and any(WEIGHTS_DIR.glob("*.pt"))):
    st.error(
        "**Model weights not found.** The `weights/` folder is gitignored, so a "
        "fresh clone won't have them. See the README for the download step, then "
        "restart the app."
    )
    st.stop()

# ---------------- Inputs ----------------
colUpload, colCamera = st.columns(2, gap="medium")
with colUpload:
    f = st.file_uploader("📁 Upload a photo", type=["jpg", "jpeg", "png"])
with colCamera:
    shot = st.camera_input("📷 Or take a photo")

imgBytes = None
if shot is not None:
    imgBytes = shot.getvalue()
elif f is not None:
    imgBytes = f.getvalue()

if imgBytes is None:
    st.markdown("""
    <div class="emptyState" style="margin-top:1rem;">
        <span class="emoji">📸</span>
        <h4>Ready when you are</h4>
        <p>Upload a photo or use your camera to see which bin your waste belongs in.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

img = Image.open(io.BytesIO(imgBytes)).convert("RGB")

# ---------------- Pipeline ----------------
with st.spinner("Analysing…"):
    allDets = cachedPredict(imgBytes)
    detections = [d for d in allDets if d.get("conf", 0) >= threshold]
    annotated = annotateImage(img, detections)

# ---------------- Layout ----------------
imgCol, listCol = st.columns([1, 1], gap="large")

with imgCol:
    st.image(annotated, caption="Your photo", width="stretch")

with listCol:
    imgKey = hash(imgBytes)
    if st.session_state.get("lastImgKey") != imgKey:
        st.session_state["lastImgKey"] = imgKey
        st.session_state["itemsSorted"] = (
            st.session_state.get("itemsSorted", 0) + len(detections)
        )

    counts = {k: 0 for k in FLAGS}
    for d in detections:
        _, flag, _ = mapping.map_waste_item(d["class"])
        counts[flag] = counts.get(flag, 0) + 1

    t1, t2, t3 = st.columns(3, gap="small")
    t1.markdown(statTile(st.session_state["itemsSorted"], "Sorted"), unsafe_allow_html=True)
    t2.markdown(statTile(counts.get("Recyclable", 0), "Recyclable"), unsafe_allow_html=True)
    t3.markdown(statTile(counts.get("General", 0) + counts.get("Unsure", 0), "General"), unsafe_allow_html=True)

    st.write("")
    st.markdown(f"#### Detected items ({len(detections)})")

    if not detections:
        st.markdown("""
        <div class="emptyState">
            <span class="emoji">🔍</span>
            <h4>No items detected</h4>
            <p>Nothing stood out in this photo. Try again with:</p>
            <ul>
                <li>A closer shot — one item filling the frame</li>
                <li>Brighter, even lighting</li>
                <li>A plain background</li>
                <li>A lower threshold in the sidebar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        for n, det in enumerate(detections, start=1):
            binType, flag, tip = mapping.map_waste_item(det["class"])
            renderCard(n, det, {"bin_type": binType, "flag": flag, "tip": tip})

# ---------------- Fixed bottom action bar ----------------
sortedCount = st.session_state.get("itemsSorted", 0)
st.markdown(f"""
<div class="bottomBar">
    <span class="bbLabel">♻️ SortSmart</span>
    <span class="bbRight">
        <span class="bbNum">{sortedCount}</span>
        <span class="bbUnit">items sorted this session</span>
    </span>
</div>
""", unsafe_allow_html=True)