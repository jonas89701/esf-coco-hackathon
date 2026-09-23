**Project title:**
SortSmart — AI Recycling Assistant for Hong Kong Schools

**One-line pitch:**
Point your camera at a pile of rubbish, and AI tells you exactly which bin each item goes in — and how to prep it.

**Problem statement:**
Most people want to recycle, but they don't know which of the four HK bin streams an item belongs to, and contaminated items (greasy pizza boxes, unrinsed bottles) get rejected from the recycling chain. Confusion = contamination = low recycling rates.

**Objective:**
Build a working Streamlit web app where a user takes a photo (or live camera) of one or more items and instantly receives, per detected item: the correct bin type, a confidence score, and a "how to prep" tip. The app should be dependable enough to demo live and simple enough that it runs from a fresh clone.

**Alignment with theme:**
UN SDG 12 — Responsible Consumption and Production (reducing contamination and improving recycling rates at the source). Secondary alignment: SDG 4 (Education — teaching correct recycling behaviour).

---

**System architecture:**

```
[ User takes photo / live camera ]  
                 │  
                 ▼  
┌──────────────────────────────────────────────┐  
│  1. YOLO Object Detection (ultralytics)      │  ──► Detects items + classes + boxes
└──────────────────────────────────────────────┘  
                 │  
                 ▼  
┌──────────────────────────────────────────────┐  
│  2. Waste-Rule Mapping Engine                │  ──► COCO class → HK bin type + prep tip
└──────────────────────────────────────────────┘  
                 │  
                 ▼  
[ Streamlit UI: annotated image + per-item bin cards + confidence + tips ]
```

---

**Target users (personas):**

* **Maya (student)**: eats lunch at the school canteen, plastic container, milk carton, banana peel — would bin them correctly if she knew which.
* **Uncle Keung (school janitor)**: empties bins, spends time pulling wrongly thrown items out of recycling bags.
* **A family at home**: sorting mixed rubbish into HK's bins (blue plastic/metal, green glass, brown organic, grey mixed waste) is confusing, especially for visitors/new residents.

**Key user stories:**

As a user I want to…
* upload a photo **or** use my webcam so I can check a real-life pile of rubbish.
* see **every item in the photo detected and labelled**, not just one.
* know the **bin type for each item** (Paper / Plastic & Metals / Glass / Organic / General waste) with a **confidence score**.
* get a **1-line prep tip** for each item (e.g. "rinse the bottle, remove the lid").
* see a running **"items sorted correctly" counter** during the session to reinforce learning.

---

**How it works (pipeline for developers):**

1. Capture: `st.file_uploader` (photo) and `st.camera_input` (live webcam still).
2. Detect: run a pretrained YOLO model (`ultralytics`) over the image; keep detections with confidence ≥ 0.40.
3. Draw: render boxes + class labels on the image with OpenCV/Pillow.
4. Map: each detected COCO class is looked up in a **waste-rule table** (COCO class → bin type + prep tip + "recyclable/organic/general" flag).
5. Display: annotated image + one card per detected item, plus the session counter.

**Model & AI approach:**

* **Primary — YOLO (ultralytics), pretrained, no training required.** Pretrained weights detect everyday objects (bottles, cups, forks, banana, apple, …) reliably out of the box. We integrate a *generic* detector and author our own mapping/rule logic — this is "pre-existing AI effectively integrated" with substantial custom logic, which is exactly what the rubric rewards.
* **Stretch goal (only if ahead):** fine-tune YOLO on a small custom "waste item" image set using the team's existing YOLO training knowledge.
* **Fallback (if YOLO install/weights are a problem on the day):** a Hugging Face `transformers` image-classification pipeline (single-item classification).

**Waste-rule mapping table (examples — extended in code):**

| Expected object | Bin type | Flag | Prep tip |
| :---- | :---- | :---- | :---- |
| bottle, cup, bowl (plastic) | Blue — Plastics & Metals | Recyclable | "Rinse, remove lid/cap" |
| fork, knife, spoon, can | Blue — Plastics & Metals | Recyclable | "Wipe clean, flatten if possible" |
| banana, apple, orange | Brown — Organic | Organic | "No prep needed" |
| sandwich, pizza, hot dog | Grey — General | General | "Greasy food waste — not recyclable" |
| carrot, broccoli | Brown — Organic | Organic | "Compost if available" |
| *(anything not mapped / unknown)* | Check locally | Unsure | "Bin in general waste or check the item label" |

---

**Software stack:**

* Python 3.14
* **streamlit** — web UI prototype
* **ultralytics (YOLO)** — object detection
* **opencv-python / Pillow** — image annotation
* **numpy** — array handling

**Project structure:**

```
coco/
├── SortSmart Project Specification.md   # this document
├── README.md                            # setup guide + AI disclosure + citations
├── requirements.txt                     # pinned dependency list
├── .gitignore
├── app/
│   └── main.py                          # Streamlit entry point  (streamlit run app/main.py)
├── src/
│   ├── __init__.py
│   ├── detector.py                      # YOLO inference wrapper (load model, predict)
│   ├── mapping.py                       # COCO class → bin type / flag / prep tip rules
│   └── annotate.py                      # draw bounding boxes + labels (OpenCV/Pillow)
├── data/
│   └── sample_images/                   # pre-baked demo images (demo can never fail)
├── notebooks/                           # exploration / troubleshooting notes
└── tests/                               # pytest tests for mapping + annotation logic
```

**Deliverables (rulebook-mapped):**

1. Public GitHub repo with runnable source + `README.md` setup steps (verified from a fresh clone).
2. **AI Disclosure Statement** — tools used (e.g. GitHub Copilot / opencode / ChatGPT), exact role each played, and how the team modified/integrated outputs.
3. **2-minute video pitch** — problem → selected SDG → live prototype walk-through → architecture + AI disclosure review.

---

**Rubric scoring strategy:**

* **A. Innovation (6–7):** "point camera at the whole pile" beats single-photo classifiers; prep-tip output adds originality.
* **B. Problem-solving (7):** clear personas, real contamination problem, education layer (counter + tips).
* **C. Social Impact (8):** strongly aligned with SDG 12; complementing existing bins (not replacing them).
* **D. Technical Complexity (7–8):** working prototype, real computer-vision AI integration, moderately complex code that runs.

**Execution timeline (6 days, roles):**

| Day | Focus | Owners |
| :---- | :---- | :---- |
| 1 | Camera + upload input working, YOLO inference on a sample image | You + Ethan |
| 2 | Annotated-image rendering + confidence thresholding | You + Ethan |
| 3 | Waste-rule mapping table + per-item bin cards in UI | Julian (UI) + Ethan |
| 4 | Webcam live mode + session "sorted" counter + styling | Julian + Gareth |
| 5 | Fallbacks, edge cases, README, AI disclosure, screenshots | Gareth + all |
| 6 | 2-minute video pitch + final commit + submission | Everyone |

**Scope cuts (if behind — cut in order, never the live demo):**

1. Drop webcam mode; photo upload only.
2. Reduce mapping table to ~6 well-tested COCO classes.
3. Remove the session counter; keep per-item cards only.
4. Fallback to Hugging Face classifier if YOLO is bulky to install.

**Risks & mitigation:**

* **Demo must never fail:** pre-bake 2–3 sample images that we know score well; fall back to them if the camera input misbehaves.
* **Model download size/time:** pin a small model variant (e.g. YOLO11n) and cache weights in the repo instructions.
* **Canteen lighting/angles:** run detection on clear top-down photos; mention in the pitch video demo walk-through.

(End of spec)