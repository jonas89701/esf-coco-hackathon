from functools import lru_cache
from pathlib import Path

import numpy as np
from ultralytics import YOLOWorld

WEIGHTS_DIR = Path(__file__).resolve().parent.parent.parent / "weights"
BASE_WEIGHTS = WEIGHTS_DIR / "yolov8s-worldv2.pt"
BAKED_WEIGHTS = WEIGHTS_DIR / "yolov8s-worldv2_core.pt"

DEFAULT_VOCAB = [
    "plastic bottle",
    "beverage can",
    "glass bottle",
    "glass jar",
    "paper",
    "cardboard box",
    "milk carton",
    "liquid carton",
    "paper cup",
    "plastic cup",
    "styrofoam container",
    "plastic fork",
    "plastic spoon",
    "food waste",
]

DEFAULT_CONF = 0.10


@lru_cache(maxsize=1)
def load_model():
    if BAKED_WEIGHTS.exists():
        try:
            model = YOLOWorld(str(BAKED_WEIGHTS))
            if list(model.names.values()) == DEFAULT_VOCAB:
                return model
            # baked with an older vocabulary, fall through and re-bake
        except Exception:
            BAKED_WEIGHTS.unlink(missing_ok=True)

    model = YOLOWorld(str(BASE_WEIGHTS))
    model.set_classes(DEFAULT_VOCAB)
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    model.save(str(BAKED_WEIGHTS))

    return model


def predict(image, conf=DEFAULT_CONF):
    model = load_model()
    if isinstance(image, np.ndarray):
        image = image[:, :, ::-1]

    results = model.predict(image, conf=conf, verbose=False)
    detections = []

    for r in results:
        names = r.names
        boxes = r.boxes.xyxy.cpu().numpy()
        scores = r.boxes.conf.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy().astype(int)

        for box, score, cls in zip(boxes, scores, classes):
            detections.append(
                {
                    "class": names[cls],
                    "conf": float(score),
                    "box": [round(v) for v in box.tolist()],
                }
            )

    return detections
