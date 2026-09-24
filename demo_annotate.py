from pathlib import Path
from PIL import Image
import numpy as np
import cv2

from src import detector
from src.annotate import annotateImage

SAMPLES = Path("data/sample_images")

img_path = SAMPLES / "sprite_can.jpg"
img = Image.open(img_path)
results = detector.predict(img, conf=detector.DEFAULT_CONF)
annotated = annotateImage(img, results)

print(f"image: {img_path.name} | detections: {len(results)}")
for det in results:
    print(f"  {det['class']:<18} {det['conf']:.2f}")

window = cv2.cvtColor(np.asarray(annotated), cv2.COLOR_RGB2BGR)
cv2.imshow("SortSmart annotated", window)
cv2.waitKey(0)
cv2.destroyAllWindows()
