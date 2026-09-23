# ESF CoCo Hackathon — Team Task Plan

**Project:** High-Density Urban Recycling Bin Location Optimizer for Hong Kong
**Deadline:** 1 week from kickoff — submission + video pitch
**MVP scope:** Prove the full pipeline end-to-end on **one district (Sham Shui Po)**, then scale to all of Hong Kong if time allows.

---

## 1. The big picture (read this first)

We are finding the **K best places to put recycling bins** in Hong Kong.

Three steps, done in order:

```
raw geo data  -->  LightGBM scores every location 0-1  -->  Weighted K-Medoids picks K bin spots
      │                    │                                    │
   download         "how likely is this spot to            "given those hot spots,
   + clean          need a bin?" (probability)             place K bins to cover them"
```

In plain English:

1. **Data** — get lists of where bins already are, plus bus stops, MTR exits, shops and homes.
2. **Train a model** — teach LightGBM to guess "is this a good spot for a bin?" using distance-to-transport/shops/homes as clues.
3. **Place bins** — use the model's guesses to pick the exact K best coordinates (blue = existing bins, red = our suggestions).
4. **Show it** — a Streamlit map the judges can play with (district filter, K slider, coverage score).

---

## 2. Team roles

| Person | Role | Owns these files | Definition of done |
|---|---|---|---|
| **You** | ML Lead / Integration | `src/models/train_model.py`, wiring everything | A model that scores well + a working end-to-end pipeline |
| **Ethan** | Data & Features Engineer | `src/features/build_features.py`, grid/sampling | A clean labeled dataset, no data leakage |
| **Julian** | Visualization & Dashboard | `src/app/dashboard.py` | A map judges can click around on |
| **Gareth** | Data Steward & QA | `src/data/downloader.py`, downloads, tests | All datasets downloaded + sanity-checked |

**Pairing:** Julian pairs with you (dashboard), Gareth pairs with Ethan (data). If someone is stuck, the pair fixes it before moving on.

---

## 3. The 7-day plan

### Day 1 — Foundation

| # | Task | Owner | Details |
|---|---|---|---|
| 1.1 | Clone repo + install packages | Everyone | `git clone`, then `uv venv --python 3.14 .venv && uv pip install -r requirements.txt` |
| 1.2 | Kickoff demo | You | 15-min LightGBM demo on fake data so Julian/Gareth see what a "score" is |
| 1.3 | Agree feature list | Everyone | Finalize which features we build (dist to MTR/bus/commercial/residential, POI counts) |
| 1.4 | Pick Sham Shui Po area | Everyone | Grab its bounding box (lat/lon) and save it in a notebook |
| 1.5 | Download datasets | Gareth | EPD recycling bins + TD bus stops → `data/raw/`. Record source URLs |
| 1.6 | Verify geometry loads | Ethan | `geopandas.read_file()` works, CRS is consistent (WGS84). This blocks Day 2 |
| 1.7 | Start dashboard dummy version | Julian | Static folium map with fake blue/red markers + K slider (default 8858) |

- ✅ **Day 1 done when:** packages installed for everyone, datasets load, dummy map renders in the browser.

### Day 2 — Data + training labels

| # | Task | Owner | Details |
|---|---|---|---|
| 2.1 | Finish downloader script | Julian | `src/data/downloader.py` downloads all raw files into `data/raw/` |
| 2.2 | Get CSDI commercial/residential layers | Julian | ArcGIS REST/WFS endpoint, save as GeoJSON |
| 2.3 | Explore + validate datasets | Gareth | Columns, row counts, coordinate range (should be ~22.2–22.5 N, 114–114.3 E). Notes in a notebook |
| 2.4 | Build 20m grid | Ethan | Dense grid of points for Sham Shui Po |
| 2.5 | Sample negative points (label 0) | You + Ethan | Random grid points, **exclude any within 15m of an existing bin** (avoid false negatives) |
| 2.6 | Assign labels | You + Ethan | Existing bin locations = 1, sampled points = 0. Aim ~1:2 ratio pos:neg |

- ✅ **Day 2 done when (M1):** a labeled table exists — rows = points, columns = coords + `label` (0 or 1).

### Day 3 — Features + dashboard

| # | Task | Owner | Details |
|---|---|---|---|
| 3.1 | Spatial joins → features | Ethan | For every point: `dist_mtr`, `dist_bus`, `dist_commercial`, `dist_residential`, `poi_count_30m` → save to `data/processed/` |
| 3.2 | Sanity-check with maps | Gareth | Plot sample points + 15m/30m buffers with folium; visually confirm buffers look right |
| 3.3 | Write distance tests | Gareth | 3–4 pytest tests on distance/buffer logic |
| 3.4 | Add district dropdown | Julian | Choose Sham Shui Po (then Central, etc.) to re-run the map |
| 3.5 | Add coverage metric | Julian | "% of high-demand zones within 50m of a bin" on dummy data |

- ✅ **Day 3 done when:** a `pd.DataFrame` exists with 5+ feature columns + labels, and the dashboard has dropdown + coverage %.

### Day 4 — First model + optimization

| # | Task | Owner | Details |
|---|---|---|---|
| 4.1 | Spatial split (no leakage!) | You | Group nearby points together, then 80/20 train/test — **never a random split** |
| 4.2 | Train LightGBM baseline | You | `lgb.LGBMClassifier(n_estimators=100, learning_rate=0.05, max_depth=6, random_state=42)` |
| 4.3 | Evaluate | Ethan | ROC-AUC, precision, recall on test set |
| 4.4 | Feature importance chart | Ethan | `plot_importance()` — good for the judges |
| 4.5 | Score grid + keep hot spots | You | `predict_proba` on the district grid, keep points with P ≥ 0.70 |
| 4.6 | Weighted K-Medoids | You/Ethan | `scikit-learn-extra.KMedoids` on the hot spots, probabilities as weights (see spec formula) |

- ✅ **Day 4 done when (M2):** test ROC-AUC ≥ 0.8 **and** K proposed bin coordinates exist.

### Day 5 — Integration & tuning

| # | Task | Owner | Details |
|---|---|---|---|
| 5.1 | Tune the model | You | Try max_depth 4–8, learning_rate 0.03–0.1; only change one thing at a time |
| 5.2 | Wrap clean functions | You | `get_recommendations(district, K)` + `load_existing_bins(district)` — Julian/Gareth only touch these |
| 5.3 | Plug real data into dashboard | Ethan | Swap dummy markers for real model output (blue = existing, red = recommended) |
| 5.4 | Live K slider | Julian | Slider (default 8858) re-runs clustering and redraws the map |

- ✅ **Day 5 done when:** dashboard shows a **real** district map: blue existing bins, red recommended, slider works.

### Day 6 — Polish + video

| # | Task | Owner | Details |
|---|---|---|---|
| 6.1 | Dashboard polish | Julian | Labels, legend, error-free reload, clean layout |
| 6.2 | README + screenshots | Gareth | Setup instructions that work from a fresh clone |
| 6.3 | Flow graphic | You/Ethan | 1-page diagram: Data → LGBM → K-Medoids → Map |
| 6.4 | Write video script | Julian + Gareth | See §5 for the structure |

- ✅ **Day 6 done when (M3):** dashboard fully working + first video take recorded.

### Day 7 — Submission day

| # | Task | Owner | Details |
|---|---|---|---|
| 7.1 | Record/finish video | Julian + Gareth | Final cut, rendered, submitted |
| 7.2 | Fresh-clone test | Ethan | Clone to a clean folder → install → `streamlit run src/app/dashboard.py` works |
| 7.3 | Final commit + tag | You | `git commit`, push, tag e.g. `v1.0` |
| 7.4 | Submit | Everyone | Upload everything before the deadline |

- ✅ **Day 7 done when:** video + repo submitted.

---

## 4. Master checklist

### Setup
- [ ] Everyone: clone repo
- [ ] Everyone: `.venv` created + packages installed
- [ ] Everyone: can run `streamlit run src/app/dashboard.py`
- [ ] Kickoff LGBM demo done
- [ ] Feature list agreed
- [ ] Sham Shui Po bounding box saved

### Data (Gareth + Julian, Ethan reviews)
- [ ] EPD recycling bins downloaded
- [ ] TD bus stops downloaded
- [ ] CSDI commercial/residential layers downloaded
- [ ] All datasets load with `geopandas` (no CRS/encoding errors)
- [ ] Dataset summary (rows/cols/range) written in a notebook
- [ ] `src/data/downloader.py` saves everything into `data/raw/`

### Labels (Ethan + You)
- [ ] 20m grid built for Sham Shui Po
- [ ] Negative points sampled (none within 15m of a bin)
- [ ] `label` column created (bins = 1, grid = 0)
- [ ] Labeled data saved to `data/processed/`

### Features (Ethan, QA: Gareth)
- [ ] `dist_mtr` computed
- [ ] `dist_bus` computed
- [ ] `dist_commercial` computed
- [ ] `dist_residential` computed
- [ ] `poi_count_30m` computed
- [ ] Buffers visually sanity-checked on a map
- [ ] 3–4 pytest tests pass

### Model (You, eval: Ethan)
- [ ] Spatial (grouped) 80/20 split — NOT random
- [ ] LGBMClassifier baseline trained
- [ ] ROC-AUC measured (target ≥ 0.8)
- [ ] Precision/recall measured
- [ ] `plot_importance()` chart saved
- [ ] Model tuned (one parameter at a time)

### Optimization (Ethan + You)
- [ ] Full-grid `predict_proba` run
- [ ] Hot spots kept (P ≥ 0.70)
- [ ] Weighted K-Medoids runs with haversine distances
- [ ] K recommended coordinates output

### Dashboard (Julian + Gareth)
- [ ] Dummy map with blue (existing) + red (recommended) markers
- [ ] District dropdown works
- [ ] K slider works, default 8858
- [ ] Coverage metric (50m) displays
- [ ] Real model output plugged in
- [ ] Legend + labels clear
- [ ] `streamlit run` works from a fresh clone

### Pitch video (Julian + Gareth lead, all help)
- [ ] Script drafted
- [ ] Flow graphic ready
- [ ] Live demo recorded
- [ ] Video rendered + submitted

### Submission
- [ ] Final commit + tag pushed
- [ ] Everything submitted by the deadline

---

## 5. Video pitch structure (~80–90 seconds)

| Time | Content | Who says it |
|---|---|---|
| 0:00–0:30 | The problem: HK bins are badly placed, waste piles up | Gareth |
| 0:30–0:50 | The method: LightGBM scores demand, K-Medoids places bins | You |
| 0:50–1:10 | Live demo: map + slider + coverage metric | Julian |
| 1:10–1:30 | Results + "next steps" (more data, live foot traffic) | Ethan |

---

## 6. Guardrails — if we fall behind, cut in this order

1. Drop the CSDI residential footprint layer — use OpenStreetMap building density instead.
2. Increase grid spacing 20m → 40m (fewer points, much faster).
3. Replace the K slider with 2–3 preset K values.
4. Skip tuning entirely — the Day-4 baseline is fine if AUC ≥ 0.8.
5. Fix K-medoids to one district only; remove "all of HK" scaling from the demo.

Never sacrifice: the spatial split (no data leakage), the live map demo, and at least one coverage metric.

## 7. Judging traps to avoid

- **Spatial leakage** — random 80/20 split lets the model cheat by memorizing neighbors. Always group by neighborhood before splitting.
- **False negatives** — sampled points within 15m of a real bin must be thrown away, or you train the model to say "no bin needed" right next to a bin.
- **Broken demo** — if the model underperforms, demo the dashboard with the P≥0.70 threshold and K fixed; never show a half-working pipeline.
- **Wrong projections** — mixing lat/lon with projected meters silently breaks every distance. Verify CRS before computing distances.