# SortSmart — AI Recycling Assistant

Point your camera at a pile of rubbish and AI tells you exactly which bin each item goes in. UN SDG 12 project for the ESF CoCo 2026 Startup Hackathon.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.14.

```bash
uv sync            # creates .venv, installs deps from pyproject.toml + uv.lock
```

The first time the model runs it downloads the base YOLO-World weights and auto-bakes them into `weights/yolov8s-worldv2_core.pt` (a faster-to-load snapshot). That baked file — or the base `.pt` — is gitignored, so it needs to exist on the machine you demo from. Working fully offline just means running the app once with internet, then the baked weights are reused.

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

## AI Disclosure

*(to be filled in before submission — list every AI tool used and its exact role)*