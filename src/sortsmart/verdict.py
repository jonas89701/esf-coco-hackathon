from sortsmart.mapping import map_waste_item

DEFAULT_IOU = 0.5


def _iou(boxA, boxB):
    ax1, ay1, ax2, ay2 = boxA
    bx1, by1, bx2, by2 = boxB
    x1 = max(ax1, bx1)
    y1 = max(ay1, by1)
    x2 = min(ax2, bx2)
    y2 = min(ay2, by2)
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    areaA = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    areaB = max(0, bx2 - bx1) * max(0, by2 - by1)
    union = areaA + areaB - inter
    if union <= 0:
        return 0.0
    return inter / union


def dedupeDetections(detections, iouThreshold=DEFAULT_IOU):
    # one object can fire a pile of boxes — boxes of the same class that
    # overlap the same thing are one object, keep the highest-scoring box
    kept = []
    ordered = sorted(detections, key=lambda d: d.get("conf", 0.0), reverse=True)
    for det in ordered:
        box = det.get("box")
        label = str(det.get("class", ""))
        if not box:
            kept.append(det)
            continue
        duplicate = any(
            k.get("box")
            and k.get("class") == label
            and _iou(box, k["box"]) >= iouThreshold
            for k in kept
        )
        if not duplicate:
            kept.append(det)
    return kept


def combineConfidences(confs):
    # final = 1 - (1 - a)(1 - b) ... independent evidence per object
    miss = 1.0
    for conf in confs:
        conf = max(0.0, min(1.0, conf))
        miss *= 1.0 - conf
    return 1.0 - miss


def pileVerdict(detections):
    # dedupe to real objects, group by the bin they map to, combine each bin
    bins = {}
    for det in dedupeDetections(detections):
        binType, flag, _ = map_waste_item(det.get("class", ""))
        if binType not in bins:
            bins[binType] = {"flag": flag, "confs": []}
        bins[binType]["confs"].append(det.get("conf", 0.0))

    verdict = []
    for binType, info in bins.items():
        verdict.append(
            {
                "bin_type": binType,
                "flag": info["flag"],
                "confidence": combineConfidences(info["confs"]),
                "count": len(info["confs"]),
            }
        )
    verdict.sort(key=lambda v: v["confidence"], reverse=True)
    return verdict