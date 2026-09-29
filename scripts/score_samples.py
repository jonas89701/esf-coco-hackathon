# scores the sample photos against what each one should detect, for tuning
# the vocabulary and prompt wording. run: uv run python scripts/score_samples.py
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

from PIL import Image

from sortsmart import detector

IMAGES_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_images"
THRESHOLD = 0.10

# what each photo should surface at the default threshold
EXPECTED = {
    "banana_1.jpg": "food",
    "banana_2.jpg": "food",
    "carrots.jpg": "food",
    "orange_1.jpg": "food",
    "orange_2.jpg": "food",
    "milk_carton_1.jpg": "beverage carton",
    "milk_carton_2.jpg": "beverage carton",
    "paper.jpg": "paper",
    "paper_cup_1.jpg": "paper cup",
    "paper_cup_2.jpg": "foam container",
    "plastic_bottle_1.jpg": "plastic bottle",
    "plastic_bottle_2.jpg": "plastic bottle",
    "plastic_fork_amazon.jpg": "plastic fork",
    "plastic_fork_uline.jpg": "plastic fork",
    "plastic_spoon_1.jpg": "plastic spoon",
    "plastic_spoon_2.jpg": "plastic spoon",
    "sprite_can.jpg": "beverage can",
    "styrofoam_1.jpg": "foam container",
    "styrofoam_2.jpg": "foam container",
}

# photos that should show nothing (no class fits them)
NEGATIVES = ["curtains.jpg", "plastic_straws.jpg"]


def bestScores(imagePath):
    img = Image.open(imagePath).convert("RGB")
    dets = detector.predict(img, conf=0.0)
    best = {}
    for d in dets:
        cls = d["class"]
        if d["conf"] > best.get(cls, 0.0):
            best[cls] = d["conf"]
    return best


def main():
    hits = 0
    misses = []
    wrongs = []
    for name, want in EXPECTED.items():
        best = bestScores(IMAGES_DIR / name)
        if best.get(want, 0.0) >= THRESHOLD:
            hits += 1
            noise = [
                f"{c} {s:.2f}"
                for c, s in sorted(best.items(), key=lambda kv: -kv[1])
                if c != want and s >= THRESHOLD
            ]
            if noise:
                wrongs.append((name, noise))
        else:
            got = sorted(best.items(), key=lambda kv: -kv[1])[:3]
            misses.append((name, want, got))

    fps = []
    for name in NEGATIVES:
        best = bestScores(IMAGES_DIR / name)
        loud = [f"{c} {s:.2f}" for c, s in best.items() if s >= THRESHOLD]
        if loud:
            fps.append((name, loud))

    print(f"threshold {THRESHOLD} | {hits}/{len(EXPECTED)} expected classes detected")
    if misses:
        print("\nmisses:")
        for name, want, got in misses:
            shown = ", ".join(f"{c} {s:.2f}" for c, s in got) or "-"
            print(f"  {name:24s} wanted {want:16s} got: {shown}")
    if wrongs:
        print("\nextra classes above threshold:")
        for name, noise in wrongs:
            print(f"  {name:24s} {', '.join(noise)}")
    if fps:
        print("\nfalse positives on negatives:")
        for name, loud in fps:
            print(f"  {name:24s} {', '.join(loud)}")
    if not (misses or wrongs or fps):
        print("clean sweep")


if __name__ == "__main__":
    main()
