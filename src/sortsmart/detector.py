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
    "paper",
    "cardboard box",
    "beverage carton",
    "liquid carton",
    "paper cup",
    "plastic cup",
    "foam container",
    "plastic fork",
    "plastic spoon",
    "food",
]

# extra prompts the model scores with, mapped back to the class we show —
# "banana" fires way harder on fruit than "food" does, but the card still
# says food. every alias belongs to exactly one class so one object never
# votes twice under two labels
PROMPT_ALIASES = {
    "plastic bottle": ["bottle", "PET bottle", "water bottle", "soda bottle"],
    "beverage can": ["soda can", "tin can", "aluminum can"],
    "paper": ["sheet of paper", "newspaper", "notebook paper"],
    "cardboard box": ["cardboard", "shipping box"],
    "beverage carton": ["milk carton", "juice box", "tetra pak"],
    "liquid carton": ["juice carton"],
    "paper cup": ["coffee cup", "disposable cup"],
    "foam container": [
        "styrofoam container",
        "styrofoam box",
        "foam cup",
    ],
    "plastic fork": ["fork"],
    "plastic spoon": ["spoon"],
    "food": [
        "banana",
        "orange",
        "apple",
        "carrot",
        "fruit",
        "food waste",
        "fruit peel",
    ],
}

ALIAS_TO_CLASS = {
    prompt: cls for cls, prompts in PROMPT_ALIASES.items() for prompt in prompts
}
DETECT_VOCAB = DEFAULT_VOCAB + list(ALIAS_TO_CLASS)

DEFAULT_CONF = 0.10


@lru_cache(maxsize=1)
def load_model():
    if BAKED_WEIGHTS.exists():
        try:
            model = YOLOWorld(str(BAKED_WEIGHTS))
            if list(model.names.values()) == DETECT_VOCAB:
                return model
            # baked with an older vocabulary, fall through and re-bake
        except Exception:
            BAKED_WEIGHTS.unlink(missing_ok=True)

    model = YOLOWorld(str(BASE_WEIGHTS))
    model.set_classes(DETECT_VOCAB)
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
            label = names[cls]
            detections.append(
                {
                    "class": ALIAS_TO_CLASS.get(label, label),
                    "conf": float(score),
                    "box": [round(v) for v in box.tolist()],
                }
            )

    return detections
