# SortSmart — AI Recycling Assistant

Point your camera at a pile of rubbish and AI tells you exactly which bin each item goes in. UN SDG 12 project for the ESF CoCo 2026 Startup Hackathon.

## Setup

```bash
uv venv --python 3.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Run

```bash
streamlit run app/main.py
```

## Project structure

```
coco/
├── SortSmart Project Specification.md  # this project's spec
├── requirements.txt                    # dependencies
├── .gitignore
├── app/
│   └── main.py                         # Streamlit entry point
├── src/
│   ├── detector.py                     # YOLO inference wrapper
│   ├── mapping.py                      # COCO class → bin rules
│   └── annotate.py                     # draw boxes + labels
├── data/sample_images/                 # pre-baked demo images
├── notebooks/
└── tests/
```

## AI Disclosure

*(to be filled in before submission — list every AI tool used and its exact role)*