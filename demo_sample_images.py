import glob
import os

import numpy as np
from PIL import Image

from src.detector import predict
from src.mapping import map_waste_item


def main() -> None:
    for path in sorted(glob.glob("data/sample_images/*.jpg")):
        img = np.array(Image.open(path).convert("RGB"))
        dets = predict(img)
        name = os.path.basename(path)

        if not dets:
            print(f"{name}: no detections")
            continue

        best = max(dets, key=lambda d: d["conf"])
        bin_, flag, tip = map_waste_item(best["class"])
        others = ", ".join(f"{d['class']} {d['conf']:.2f}" for d in dets)
        print(
            f"{name}: {best['class']} {best['conf']:.2f} -> {bin_} [{flag}] | all: {others}"
        )


if __name__ == "__main__":
    main()
