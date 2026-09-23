# SortSmart — Team Task Plan

**Goal:** a working Streamlit app that detects items in a photo/webcam and tells you which HK bin each goes in + a prep tip. Demo on a pre-baked sample image so it can never fail.

**Pipeline to build (in dependency order):**
```
detector.py (YOLO) → mapping.py (rules) → annotate.py (draw boxes) → app/main.py (UI) → demo
```

---

## Who does what (based on skill level)

| Person | Skill level | Core role | Small-task zones |
|---|---|---|---|
| **You** | Most experience | Integration lead | YOLO detector, core app logic, wiring, fixing whatever breaks |
| **Ethan** | Strong | Model & logic | annotate.py, mapping logic, tests, + you's backup |
| **Julian** | Intermediate (git/venv/VSCode) | UI & Git keeper | Streamlit UI pieces, environment setup, git conflicts/commits, README |
| **Gareth** | Beginner (knows Python) | Data & docs | Sample images, mapping table data, AI disclosure, video narration |

**Git rules (Julian enforces):**
- Always `git pull` before starting and before pushing.
- Commit small and often with a message like `add: bin mapping for bottles`.
- If a push is rejected → `git pull` first, then push again. Julian resolves conflicts.

---

## Your tasks (Integration Lead)

- [ ] Write `src/detector.py`: load YOLO model once (`@st.cache_resource`), function `predict(image)` returning boxes/classes/confidences.
- [ ] Write the core of `app/main.py`: photo upload (`st.file_uploader`) + webcam (`st.camera_input`).
- [ ] Call the mapping + annotation functions and render results (keep it simple at first: annotated image + a bullet list).
- [ ] Add the "items sorted" counter.
- [ ] Final pass: everything works from `streamlit run app/main.py`.

## Ethan's tasks (Model & Logic)

- [ ] Write `src/annotate.py`: draw bounding boxes + class labels on the image (OpenCV or Pillow), return the annotated image.
- [ ] Write `src/mapping.py` logic: given a COCO class name, return `{bin_type, flag, tip}` using Gareth's data (see below). Unknown class → "Unsure".
- [ ] Write pytest tests: mapping returns correct bin for 5 known classes; unknown class → "Unsure"; annotation function returns an image.
- [ ] Confirm confidence threshold (0.40) and which YOLO model size to use (YOLO11n recommended — small/fast).
- [ ] Backup to You: double-check the app runs and the demo image scores well.

## Julian's tasks (UI & Git keeper)

- [ ] Verify a fresh setup works: clone → `uv venv --python 3.14 .venv` → `uv pip install -r requirements.txt` → app runs. Record the steps for README.
- [ ] Write the UI layout in `app/main.py` around the pieces you/Ethan provide: title, sidebar (model info/threshold), main area (image + per-item cards), counter.
- [ ] Make the per-item "cards" look clean: bin type badge, flag (Recyclable/Organic/General/Unsure), tip.
- [ ] Handle edge cases in the UI: no items detected → friendly "try again" message.
- [ ] Git keeper: keep `git pull`/commit/push discipline; help teammates when push fails.

## Gareth's tasks (Data & Docs — all beginner-friendly)

- [ ] Collect 3–5 sample images (photo your own rubbish at school/home: bottle, can, banana peel, carton) → save into `data/sample_images/`. ✅ You already started: your dataset link in the spec helps here.
- [ ] Fill in the **waste-rule mapping data** (this is just a Python dictionary — copy the table from the spec):
  - `bottle → Plastic & Metals | Recyclable | "Rinse, remove cap"`
  - `cup → Plastic & Metals | Recyclable | "Rinse thoroughly"`
  - `banana / apple / orange → Organic | Organic | "No prep needed"`
  - `sandwich / pizza → General | General | "Greasy food — not recyclable"`
  - `fork / knife / spoon → Plastic & Metals | Recyclable | "Wipe clean"`
  - plus ~4 more classes you pick from COCO (identity, spoon, bowl, …)
  - Everything else → `"Unsure | Check card | Bin in general waste or check label"`
- [ ] Draft the **AI Disclosure Statement** for the README (tools used — Copilot/opencode/ChatGPT/etc. — and what each did).
- [ ] Write the "problem" + "live demo" narration lines for the 2-min video.

---

## 6-day flow

| Day | Build | You | Ethan | Julian | Gareth |
|---|---|---|---|---|---|
| 1 | Detector + input works | detector.py + upload works | mapping logic skeleton | env verified, UI shell | sample images collected |
| 2 | Rules + boxes | wire input→detect | annotate.py + tests | cards layout | mapping data filled in |
| 3 | Full loop | app shows image+list | back up You | counter + edge cases | AI disclosure draft |
| 4 | Polish | threshold/model final | test pass | README steps | narration lines |
| 5 | Demo-proof | baked demo image running | last fixes | fresh-clone check | screenshots for video |
| 6 | Video + submit | record demo | record demo | git cleanup + final push | finalize AI disclosure |

## Never break
- The demo can always fall back to `data/sample_images/` if the camera misbehaves.
- `streamlit run app/main.py` works from a fresh clone.
- Mapping table always handles *unknown* classes gracefully (never crashes).