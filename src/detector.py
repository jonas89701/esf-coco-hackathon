from functools import lru_cache
from pathlib import Path

from ultralytics import YOLOWorld

WEIGHTS_DIR = Path(__file__).resolve().parent.parent / "weights"
BASE_WEIGHTS = WEIGHTS_DIR / "yolov8s-worldv2.pt"
BAKED_WEIGHTS = WEIGHTS_DIR / "yolov8s-worldv2_core.pt"

DEFAULT_VOCAB = [
    "plastic bottle",
    "beverage can",
    "glass bottle",
    "banana",
    "apple",
    "orange",
    "paper cup",
    "plastic cup",
    "styrofoam container",
    "milk carton",
    "plastic fork",
    "plastic spoon",
]

DEFAULT_CONF = 0.10


@lru_cache(maxsize=1)
def load_model():
    weights = BAKED_WEIGHTS if BAKED_WEIGHTS.exists() else BASE_WEIGHTS
    model = YOLOWorld(str(weights))
    if not BAKED_WEIGHTS.exists():
        model.set_classes(DEFAULT_VOCAB)
        WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
        model.save(str(BAKED_WEIGHTS))

    return model


def predict(image, conf=DEFAULT_CONF):
    model = load_model()
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
