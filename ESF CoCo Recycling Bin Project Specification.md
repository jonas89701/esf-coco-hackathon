**Project title:**  
High-Density Urban Recycling Bin Location Optimizer for Hong Kong

**Problem statement:**  
Public recycling bins in Hong Kong are often placed in a sub-optimal location relative to pedestrian foot traffic, leading to underutilization which causes high waste volume.

**Objective:**  
Build a machine learning optimization model that will take open government geospatial data, identify points of interest (POIs), calculate a predicted demand score for each of them based on foot traffic, and recommend optimal coordinates for where each recycling bin should be placed for maximized waste recycling volume.

**System architecture:**  
\[ Input: Raw POI & Spatial Features \]  
                │  
                ▼  
┌──────────────────────────────────────────────┐  
│  1\. LightGBM Gradient-Boosted Classifier     │  \--\> Predicts Foot Traffic Demand Score  
└──────────────────────────────────────────────┘  
                │  
                ▼  
┌──────────────────────────────────────────────┐  
│  2\. Weighted K-Medoids Optimization Engine   │  \--\> Places Bins at Optimal Coordinates  
└──────────────────────────────────────────────┘  
                │  
                ▼  
\[ Output: Streamlit Map & Capture Metrics \]

**Input data:** government provided geospatial data for POIs and existing bin locations  
**Demand scoring engine:** the LightGBM classifier predicts a probability P(need a bin) for every grid point or coordinate, which serves as the localized demand index (D)  
**Optimization engine:** clusters demand scores to select K optimal bin locations  
**User interface:** renders interactive map layers (existing bins vs recommended bins) and key metrics

**Data sources:**  
**Recyclable collection points dataset:** [https://data.gov.hk/en-data/dataset/hk-epd-recycteam-waste-less-recyclable-collection-points-data](https://data.gov.hk/en-data/dataset/hk-epd-recycteam-waste-less-recyclable-collection-points-data)

**Routes of public transport and coordinates of bus stop locations:** [https://data.gov.hk/en-data/dataset/hk-td-tis\_23-routes-fares-geojson](https://data.gov.hk/en-data/dataset/hk-td-tis_23-routes-fares-geojson)

**Commercial and residential entrances:** [https://portal.csdi.gov.hk/geoportal/\#metadataInfoPanel](https://portal.csdi.gov.hk/geoportal/#metadataInfoPanel)

**Algorithms and mathematical formulas:**

	**Demand index formula:**  
To calculate the demand index (D) for any coordinate p with varying weights for POIs, we will use the following formula:  
Dp \= w1 ⋅ 𝕀(MTR \< 30m) \+ w2 ⋅ 𝕀(Bus \< 15m) \+ w3 ⋅ 𝕀(Retail) \+ w4 ⋅ 𝕀(Residential)

	**Weights:**

* w1 \= 100  
* w2 \= 50  
* w3 \= 40  
* w4 \= 20

		**Indicator function:**  
		𝕀(𝑥) \= 1 if within buffer distance 0, else 𝕀(𝑥) \= 0

	**Weighted K-Medoids:**  
Takes a matrix of coordinates (xi , yi) paired with their demand weights Di and minimizes total weighted distance between demand points and assigned bin medoids

Total demand-weighted distance between every demand point and its nearest assigned recycling bin \= $\min\limits_{S}$$\sum\limits_{i=1}^{N}$Di ⋅$\min\limits_{j\ ∊\ S}$d(pi , mj)

	**Variable breakdown:**

* **$\min\limits_{S}$**makes the algorithm search for a subset of S of K total bin locations that minimizes the entire sum  
* **N**: Total number of candidate locations/grid points.  
* **Dᵢ**: The Demand Index (weight/foot traffic score) at point **pᵢ**. High-demand areas carry a larger penalty if left far from a bin.  
* **mⱼ**: A selected bin location (medoid) within the chosen set **S** (**j ∈ S**).  
* **d(pᵢ, mⱼ)**: The distance (e.g., Euclidean or geodesic distance in meters) between point **pᵢ** and bin **mⱼ**.  
* **minⱼₑₛ d(pᵢ, mⱼ)**: Finds the distance from point **pᵢ** to its **nearest** placed bin.


**Software stack and API requirements:**

* **Programming language:** Python 3.10+  
* **Core Libraries:**  
*   **geopandas, shapely** (Geospatial data manipulation)  
*   **lightgbm** (POI demand-score classification)  
*   **scikit-learn-extra** (Weighted K-Medoids implementation)
  * **folium, streamlit-folium** (Interactive map rendering)  
  * **streamlit** (Dashboard frontend)  
* **APIs:** CSDI ArcGIS REST API / OGC WFS endpoint for live layer loading

**Functional requirements:**

* **Map Visualization:** the dashboard must render an interactive map showing existing HK recycling bins as blue markers and optimized locations as red markers.  
* **District Filter:** users must be able to filter optimization runs by Hong Kong districts (e.g., Sham Shui Po, Central)  
* **Parameter Tuning:** users must be able to adjust K (number of proposed bins) dynamically via slider controls  
  * The default value of K should be 8858 (the current number of recycling bins in Hong Kong)  
* **Coverage Metric:** display a coverage capture score (% of high-demand zones within a 50m radius of a bin)

**Execution timeline:**

* **Days 1–3:** data acquisition (GeoJSON downloads, bounding-box filtering, coordinate projections).  
* **Days 4–6:** feature engineering (buffer creation, spatial joins, demand index calculations).  
* **Days 7–8:** clustering optimization (Weighted K-Medoids tuning).  
* **Days 9–11:** Streamlit dashboard implementation, documentation, and final pitch deck prep

**Training the model using LGBM:**  
Here is the complete step-by-step pipeline converted into standard Unicode text so you can copy and paste directly into Google Docs:

Here is the step-by-step pipeline for building your recycling bin classifier using LightGBM (LGBM):

### **Step 1: Create the Spatial Grid & Sample Negative Labels (0)**

Since open datasets only provide existing bin locations (positive class), you must generate negative samples across Hong Kong.

* **Define your Region of Interest (ROI):** Select target Hong Kong districts or create a continuous spatial bounding box using geopandas.

* **Generate Grid/Random Points:** Create a dense mesh grid of coordinates (e.g., points spaced 20m apart) or generate random coordinate points (x, y).

* **Filter Out Positive Buffers:** Any sampled point within 15m of an existing recycling bin is excluded to prevent false negatives.

* **Sample Negatives (0):** Select negative points from low-demand zones (e.g., slopes, highway segments, mid-park areas). Aim for a balanced 1:1 or 1:2 ratio of positive (1) to negative (0) labels.

### **Step 2: Feature Engineering (Spatial Joins & Distance Calculations)**

For every coordinate point (both positive bins and negative samples), construct feature columns using your CSDI and OpenStreetMap datasets:

* **Distance to Transport Hubs:** Distance in meters to the nearest MTR exit, bus stop, and minibus stop.

* **Distance to Commercial Entrances:** Distance to the nearest shopping mall entrance, fast-food outlet, or convenience store.

* **Distance to Residential Buildings:** Distance to the nearest residential building footprint centroid.

* **POI Counts within Buffer Radii:** Number of MTR exits within 30m, bus stops within 15m, and commercial POIs within 30m.

* **Building Footprint Density:** Total residential/commercial floor area or count within a 50m radius.

### **Step 3: Train-Test Split & LightGBM Model Training**

* **Dataset Structure:** Prepare a tabular matrix where rows are coordinate points, columns X₁, X₂, ..., Xₙ are spatial features, and target Y ∈ {0, 1}.

* **Spatial Stratified Split:** Split data into training (80%) and testing (20%) sets. Ensure points from the same immediate neighborhood are kept together (Spatial K-Fold) to prevent spatial data leakage.

* **Model Training:** Fit LGBMClassifier:

Python

```

import lightgbm as lgb
from sklearn.model_selection import train_test_split

X = df[['dist_mtr', 'dist_bus', 'dist_commercial', 'dist_residential', 'poi_count_30m']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = lgb.LGBMClassifier(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)
model.fit(X_train, y_train)

```

### 

### **Step 4: Spatial Prediction Grid & Optimization Feed**

* **Score Unmapped Territory:** Run model.predict\_proba(X\_grid) across an unserved target area (e.g., a candidate neighborhood grid) to output probability scores P(Need Bin \= 1\) between 0 and 1\.

* **Filter High-Probability Candidates:** Extract points where P ≥ 0.70.

* **Feed into Weighted K-Medoids:** Use these high-scoring coordinates and their probabilities as weights Dᵢ in your Weighted K-Medoids clustering algorithm to pick K discrete, non-overlapping bin coordinates.

### **Step 5: Model Evaluation & Feature Importance**

* **Metrics:** Evaluate classification performance on the test set using ROC-AUC, Precision, and Recall.  
* **Feature Importance Plot:** Extract LightGBM’s plot\_importance() to show judges which spatial features (e.g., MTR proximity vs. restaurant count) drive optimal bin placement.