# High-Density Urban Recycling Bin Location Optimizer for Hong Kong

Public recycling bins in Hong Kong are often placed in sub-optimal locations relative to pedestrian foot traffic, leading to underutilization and high waste volume. This project scores candidate locations with a LightGBM classifier and places bins with a weighted K-Medoids optimizer, exposed through a Streamlit map dashboard.

See `ESF CoCo Recycling Bin Project Specification.md` for the full specification.

## Project structure

```
coco/
├── data/
│   ├── raw/                 # downloaded GeoJSON / CSVs
│   └── processed/           # cleaned engineered features
├── src/
│   ├── data/                # data acquisition
│   ├── features/            # feature engineering (buffers, spatial joins)
│   ├── models/              # LightGBM training and prediction
│   ├── optimization/        # weighted K-Medoids
│   └── app/                 # Streamlit dashboard
├── notebooks/
├── tests/
├── requirements.txt
└── ESF CoCo Recycling Bin Project Specification.md
```

## Setup

```bash
uv venv --python 3.14 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```