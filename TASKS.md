# SortSmart — Team Task Plan

**Goal:** a working Streamlit app that detects items in a photo/webcam with **YOLO-World** (open-vocabulary, zero training) and tells you which HK bin each goes in + a prep tip. Demo on a pre-baked sample image so it can never fail.

**Pipeline to build (in dependency order):**
```
bake vocab+weights → detector.py (YOLO-World) → mapping.py (HK rules) → annotate.py (boxes) → app/main.py (UI) → demo
```

---

## Who does what (based on skill level)

| Person | Skill level | Core role | Small-task zones |
|---|---|---|---|
| **You** | Most experience | Integration lead | detector.py, core app logic, threshold tuning, wiring, fixing whatever breaks |
| **Ethan** | Strong | Model & logic | annotate.py, mapping logic, tests, + you's backup |
| **Julian** | Intermediate (git/venv/VSCode) | UI & Git keeper | Streamlit UI pieces, environment setup, git conflicts/commits, README |
| **Gareth** | Beginner (knows Python) | Data & docs | Sample images, mapping table data, AI disclosure, video narration |

**Git rules (Julian enforces):**
- Always `git pull` before starting and before pushing.
- Commit small and often with a message like `add: bin mapping for cans`.
- If a push is rejected → `git pull` first, then push again. Julian resolves conflicts.

---

## Your tasks (Integration Lead)

- [ ] Write `src/detector.py`: load **YOLO-World** once (`@st.cache_resource`), set the core vocabulary, function `predict(image)` returning boxes/names/confidences.
- [ ] Define the core vocabulary (~12 items): `plastic bottle, beverage can, glass bottle, banana, apple, orange, paper cup, plastic cup, styrofoam container, milk carton, plastic fork, plastic spoon`.
- [ ] Bake the vocabulary into the weights **now, while online**: `model.set_classes(VOCAB)` → `model.save("weights/yolov8s-worldv2_core.pt")`. (Offline demo depends on this.)
- [ ] Write the core of `app/main.py`: photo upload (`st.file_uploader`) + webcam (`st.camera_input`).
- [ ] Call the mapping + annotation functions and render results (annotated image + a bullet list first).
- [ ] Tune the confidence threshold (start `conf=0.10` — zero-shot runs lower than 0.40) on Gareth's real photos; pick the best prompt wording per item.
- [ ] Add the "items sorted" counter.
- [ ] Final pass: everything works from `streamlit run app/main.py`, fully offline.

## Ethan's tasks (Model & Logic)

- [ ] Write `src/annotate.py`: draw bounding boxes + class labels on the image (OpenCV or Pillow), return the annotated image.
- [ ] Write `src/mapping.py` logic: given a detected class name, return `{bin_type, flag, tip}` using Gareth's data (below). Unknown → "Unsure". Never crashes.
- [ ] Write pytest tests: mapping returns correct bin for 5 known classes; unknown → "Unsure"; annotate returns an image.
- [ ] Run sample photos through YOLO-World and log which prompts score best per item (share with You for threshold work).
- [ ] Backup to You: double-check the app runs and the demo image scores well.

## Julian's tasks (UI & Git keeper)

- [ ] Verify a fresh setup works: clone → `uv venv --python 3.14 .venv` → `uv pip install -r requirements.txt` → app runs. Record steps for README.
- [ ] Write the UI layout in `app/main.py` around the pieces you/Ethan provide: title, sidebar (model info/threshold), main area (image + per-item cards), counter.
- [ ] Make the per-item "cards" look clean: bin badge, flag (Recyclable / General / Special / Unsure), tip.
- [ ] Handle edge cases: no items detected → friendly "try again" message.
- [ ] Git keeper: keep `git pull`/commit/push discipline; help teammates when push fails.

## Gareth's tasks (Data & Docs — all beginner-friendly)

- [ ] Collect 3–5 sample images (photo your own rubbish: plastic bottle, can, banana, paper cup, carton, styrofoam box) → `data/sample_images/`. ✅ You already started — your dataset link in the spec helps.
- [ ] Fill in the **waste-rule mapping data** (plain Python dictionary — copy from the spec table — HK-fed rules):
  - `plastic bottle → Plastic bottles | Recyclable | "Rinse, remove cap & label"`
  - `beverage can → Metals | Recyclable | "Rinse, remove label"`
  - `glass bottle → Glass | Recyclable | "Rinse, remove cap"`
  - `banana / apple / orange → General waste (food) | General | "Compost if school has food waste"`
  - `paper cup / plastic cup → General waste | General | "Not recyclable"`
  - `styrofoam container → General waste | General | "Not accepted in recycling"`
  - `milk carton → Special — Green@Community | Special | "Wash, dry, remove cap; NOT street bin"`
  - Everything else → `"Unsure | Check locally | Bin in general waste or check label"`
- [ ] Draft the **AI Disclosure Statement** for the README (tools used — Copilot/opencode/ChatGPT/etc. — and what each did).
- [ ] Write the "problem" + "live demo" narration lines for the 2-min video.

---

## 6-day flow

| Day | Build | You | Ethan | Julian | Gareth |
|---|---|---|---|---|---|
| 1 | Detector + offline weights | vocab baked, detector.py + upload works | mapping logic skeleton | env verified, UI shell | sample images collected |
| 2 | Rules + boxes | wire input→detect, threshold tuning | annotate.py + tests | cards layout | mapping data filled in |
| 3 | Full loop | app shows image+list | prompt-score log done | counter + edge cases | AI disclosure draft |
| 4 | Polish | threshold/model final | test pass | README steps | narration lines |
| 5 | Demo-proof | baked demo image running offline | last fixes | fresh-clone check | screenshots for video |
| 6 | Video + submit | record demo | record demo | git cleanup + final push | finalize AI disclosure |

## Never break
- The demo can always fall back to `data/sample_images/` if the camera misbehaves.
- `streamlit run app/main.py` works from a fresh clone **and fully offline** (`weights/yolov8s-worldv2_core.pt` cached).
- Mapping table always handles *unknown* classes gracefully (never crashes).