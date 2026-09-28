# SortSmart — AI Recycling Assistant

Point your camera at a pile of rubbish and AI tells you exactly which bin each item goes in. UN SDG 12 project for the ESF CoCo 2026 Startup Hackathon.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.14.

```bash
uv sync            # creates .venv, installs deps from pyproject.toml + uv.lock
```

The first time the app runs it downloads the base YOLO-World weights (~25 MB)
and auto-bakes them into `weights/yolov8s-worldv2_core.pt` (a faster-to-load
offline snapshot). The baked file — or the base `.pt` — is gitignored, so a
fresh clone triggers this download+bake automatically on first run. To work
fully offline later, just run the app once while online so the baked weights
are cached.

## Run

```bash
uv run streamlit run src/sortsmart/main.py   # launch at http://localhost:8501
```

With the venv activated, plain python works too:

```bash
source .venv/bin/activate
python3 -m streamlit run src/sortsmart/main.py
```

## Project structure

```
coco/
├── SortSmart Project Specification.md  # this project's spec
├── pyproject.toml                      # uv project config + dependencies
├── uv.lock                             # locked dependency versions
├── .python-version                     # pins Python 3.14
├── .gitignore
├── src/sortsmart/
│   ├── main.py                         # Streamlit app
│   ├── detector.py                     # YOLO inference wrapper
│   ├── mapping.py                      # COCO class → bin rules
│   └── annotate.py                     # draw boxes + labels
├── weights/                            # gitignored: base + baked .pt files
├── data/sample_images/                 # pre-baked demo images
├── notebooks/
└── tests/                              # pytest (uv run pytest)
```

## Running the demos

```bash
uv run streamlit run src/sortsmart/main.py    # full app
uv run python demo_annotate.py              # detect + annotate one sample image
uv run python demo_sample_images.py         # batch-predict all sample images
uv run pytest                               # unit tests (no model required)
```

## Libraries & dependencies

Dependencies are managed by uv (`pyproject.toml` + `uv.lock`).

| Library | Purpose | Source |
|---|---|---|
| Ultralytics YOLO-World | Open-vocabulary object detection (zero-shot, no training) | https://github.com/ultralytics/ultralytics |
| CLIP | Text-vocabulary embeddings used by YOLO-World | https://github.com/ultralytics/CLIP |
| Streamlit | Web UI | https://github.com/streamlit/streamlit |
| Pillow | Image decoding + annotation drawing | https://python-pillow.org/ |
| OpenCV | Image handling in demo scripts | https://opencv.org/ |
| NumPy | Array/numpy handling for detections | https://numpy.org/ |
| pi-heif | HEIC photo support | https://github.com/strukturag/libheif |

## AI Disclosure

*(to be filled in before submission — list every AI tool used and its exact role)*