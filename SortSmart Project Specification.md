**Project title:**
SortSmart — AI Recycling Assistant for Hong Kong Schools

**One-line pitch:**
Point your camera at a pile of rubbish, and AI tells you exactly which bin each item goes in — and how to prep it.

**Problem statement:**
Most people want to recycle, but they don't know what HK's bins actually accept, and contaminated items (greasy pizza boxes, unrinsed bottles, plastic cups) get rejected from the recycling chain. Confusion = contamination = low recycling rates.

**Objective:**
Build a working Streamlit web app where a user takes a photo (or live camera) of one or more items and instantly receives, per detected item: the correct bin type, a confidence score, and a "how to prep" tip. The app must be dependable enough to demo live **offline** and simple enough that it runs from a fresh clone.

**Alignment with theme:**
UN SDG 12 — Responsible Consumption and Production (reducing contamination and improving recycling rates at the source). Secondary alignment: SDG 4 (Education — teaching correct recycling behaviour).

---

**System architecture:**

```
[ User takes photo / live camera ]
                 │
                 ▼
┌──────────────────────────────────────────────┐
│ 1. YOLO-World Detection (open-vocabulary)    │ ──► Detects our ~12 named items + boxes
│    (ultralytics, vocabulary baked into       │
│     weights for offline use)                 │
└──────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────┐
│ 2. Waste-Rule Mapping Engine                │ ──► detected name → HK bin type + prep tip
└──────────────────────────────────────────────┘
                 │
                 ▼
[ Streamlit UI: annotated image + per-item bin cards + confidence + tips ]
```

---

**Target users (personas):**

* **Maya (student)**: eats lunch at the school canteen — plastic bottle, milk carton, banana peel — would bin them correctly if she knew which.
* **Uncle Keung (school janitor)**: empties bins, spends time pulling wrongly thrown items out of recycling bags.
* **A family at home**: sorting mixed rubbish into HK's bins (recycling vs general waste) is confusing, especially for visitors/new residents.

**Key user stories:**

As a user I want to…
* upload a photo **or** use my webcam so I can check a real-life pile of rubbish.
* see **every item in the photo detected and labelled**, not just one.
* know the **bin type for each item** (Paper / Plastic bottles / Metals / Glass / General waste / Special) with a **confidence score**.
* get a **1-line prep tip** for each item (e.g. "rinse the bottle, remove the cap").
* see a running **"items sorted correctly" counter** during the session to reinforce learning.

---

**How it works (pipeline for developers):**

1. Capture: `st.file_uploader` (photo) and `st.camera_input` (live webcam still).
2. Detect: run **YOLO-World** (`ultralytics.YOLOWorld`) with our core vocabulary pre-set; keep detections above a tuned confidence threshold (zero-shot scores run low — start at ~0.10, not 0.40).
3. Draw: render boxes + class labels on the image (results `.plot()` or OpenCV).
4. Map: each detected class name is looked up in a **waste-rule table** (name → bin type + prep tip + flag). Anything unmapped or below threshold → "Unsure".
5. Display: annotated image + one card per detected item, plus the session counter.

**Model & AI approach:**

* **Primary — YOLO-World (ultralytics), open-vocabulary, zero training.** We supply a short vocabulary of ~12 core items via `model.set_classes([...])`. Unlike fixed-COCO YOLO, this lets us detect gaps like *beverage can*, *milk carton*, *styrofoam container*, *paper cup* that COCO's 80 classes don't cover. We author the entire vocab-to-bin rule logic ourselves — "pre-existing AI effectively integrated" with substantial custom logic, exactly what the rubric rewards.
* **Offline packaging:** bake the vocabulary into the weights (`model.set_classes(...)` → `model.save("yolov8s-worldv2_core.pt")`) **once, while online**, so demo day is fully offline and loads fast.
* **Vocabulary discipline:** keep the list short and visually distinct (research: long/open class lists sharply hurt zero-shot precision). Validate prompts against real sample photos and keep the winners.
* **Stretch goal (only if ahead):** fine-tune on a small custom "waste item" detection set (e.g. TACO or re-annotated TrashNet in YOLO format) using the team's YOLO knowledge.
* **Fallback:** switch to the fixed-COCO YOLOv8n we already use — it trims which items detect, but still demos.

**Waste-rule mapping table (HK-aware; extended in code):**

HK kerbside recycling bins accept: **paper**, **plastic bottles (PET/HDPE)**, **metal cans**, **glass bottles/jars**. Everything else — cups, styrofoam, plastic bags, food scraps, coated paper — is **general waste**. Liquid cartons need special collection (Green@Community / Mil Mill).

| Expected object | Bin type | Flag | Prep tip |
| :---- | :---- | :---- | :---- |
| bottle / plastic bottle | Plastic bottles | Recyclable | "Rinse, remove cap & label" |
| can / beverage can | Metals | Recyclable | "Rinse, remove label" |
| glass bottle | Glass | Recyclable | "Rinse, remove cap; no broken glass" |
| banana, apple, orange | General waste (food) | General | "Compost if your school has food waste collection" |
| paper cup | General waste | General | "Plastic-coated — not recyclable" |
| plastic cup, styrofoam container | General waste | General | "Not accepted in recycling bins" |
| milk carton / liquid carton | Special — Green@Community | Special | "Wash, dry, remove cap; NOT the street bin" |
| *(anything not mapped / below threshold)* | Check locally | Unsure | "Bin in general waste or check the item label" |

---

**Software stack:**

* Python 3.14
* **streamlit** — web UI prototype
* **ultralytics (YOLO-World)** — open-vocabulary object detection
* **opencv-python / Pillow** — image annotation
* **numpy** — array handling

**Project structure:**

```
coco/
├── SortSmart Project Specification.md   # this document
├── README.md                            # setup guide + AI disclosure + citations
├── requirements.txt                     # pinned dependency list
├── .gitignore
├── weights/                             # cached YOLO-World weights w/ baked vocabulary
├── app/
│   └── main.py                          # Streamlit entry point  (streamlit run app/main.py)
├── src/
│   ├── __init__.py
│   ├── detector.py                      # YOLO-World wrapper: load model, set vocab, predict
│   ├── mapping.py                       # item name → bin type / flag / prep tip rules
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

* **A. Innovation (6–7):** "point camera at the whole pile" with open-vocabulary detection beats canned classifiers; prep-tip output adds originality.
* **B. Problem-solving (7):** clear personas, real contamination problem, education layer (counter + tips).
* **C. Social Impact (8):** strongly aligned with SDG 12; complementing existing bins (not replacing them).
* **D. Technical Complexity (7–8):** working offline prototype, genuinely integrated pre-trained vision AI (open-vocabulary zero-shot), moderately complex code that runs.

**Execution timeline (6 days, roles):**

| Day | Focus | Owners |
| :---- | :---- | :---- |
| 1 | Vocab + weights baked offline; photo input works; detect on a sample image | You + Ethan |
| 2 | Annotated-image rendering + confidence threshold tuning on real photos | You + Ethan |
| 3 | Waste-rule mapping table (HK-aware) + per-item bin cards in UI | Julian (UI) + Gareth (data) |
| 4 | Webcam live mode + session "sorted" counter + styling | Julian + Gareth |
| 5 | Fallbacks, edge cases, README, AI disclosure, screenshots | Gareth + all |
| 6 | 2-minute video pitch + final commit + submission | Everyone |

**Scope cuts (if behind — cut in order, never the live demo):**

1. Drop webcam mode; photo upload only.
2. Shrink the vocabulary to the 6 best-scoring items (fewer prompts = higher accuracy).
3. Remove the session counter; keep per-item cards only.
4. Fall back to fixed-COCO YOLOv8n (already installed) if YOLO-World misbehaves.

**Risks & mitigation:**

* **Demo must never fail:** pre-bake 2–3 sample images that we know score well; fall back to them if the camera input misbehaves.
* **Offline weights missing:** bake `yolov8s-worldv2_core.pt` into `weights/` now (while online); document it in the README so fresh clones/downloads work.
* **Low zero-shot confidences:** tune the threshold (start ~0.10) per item on Gareth's real photos; pick the best prompt wording per item.
* **Canteen lighting/angles:** run detection on clear top-down photos; mention in the pitch video demo walk-through.

(Optional reference — training dataset for the stretch goal / mapping study: https://www.kaggle.com/datasets/techsash/waste-classification-data?resource=download)

(End of spec)