from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from sortsmart import detector
from sortsmart.annotate import annotate_image

SAMPLES = Path("data/sample_images")


def main():
    img_path = SAMPLES / "sprite_can.jpg"
    img = Image.open(img_path)
    results = detector.predict(img, conf=detector.DEFAULT_CONF)
    annotated = annotate_image(img, results)

    print(f"image: {img_path.name} | detections: {len(results)}")
    for det in results:
        print(f"  {det['class']:<18} {det['conf']:.2f}")

    window = cv2.cvtColor(np.asarray(annotated), cv2.COLOR_RGB2BGR)
    cv2.imshow("SortSmart annotated", window)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
