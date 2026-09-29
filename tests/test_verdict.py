import pytest

from sortsmart.verdict import combineConfidences, dedupeDetections, pileVerdict


def makeDet(cls, conf, x1, y1, x2, y2):
    return {"class": cls, "conf": conf, "box": [x1, y1, x2, y2]}


def testSameObjectDropped():
    # the milk carton case: ~30 overlapping boxes -> one object, highest score
    dets = [makeDet("milk carton", 0.63, 10, 10, 210, 210) for _ in range(30)]
    dets[0] = makeDet("milk carton", 0.71, 10, 10, 210, 210)
    kept = dedupeDetections(dets)
    assert len(kept) == 1
    assert kept[0]["conf"] == pytest.approx(0.71)


def testDistinctObjectsKept():
    # two bottles far apart are two objects
    dets = [
        makeDet("plastic bottle", 0.80, 0, 0, 50, 50),
        makeDet("plastic bottle", 0.60, 200, 200, 250, 250),
    ]
    assert len(dedupeDetections(dets)) == 2


def testLowOverlapKept():
    # barely overlapping boxes of the same class are different things
    dets = [
        makeDet("bottle", 0.70, 0, 0, 100, 100),
        makeDet("bottle", 0.65, 95, 95, 200, 200),
    ]
    assert len(dedupeDetections(dets)) == 2


def testDifferentClassesNeverDeduped():
    # its "same class" only — newspaper + paper are two separate votes
    dets = [
        makeDet("newspaper", 0.72, 0, 0, 100, 100),
        makeDet("paper", 0.84, 0, 0, 100, 100),
    ]
    assert len(dedupeDetections(dets)) == 2


def testCombineTwoIndependent():
    # spec example: newspaper 72% + paper 84% -> 1 - 0.28*0.16 = 0.9552
    assert combineConfidences([0.72, 0.84]) == pytest.approx(0.9552)


def testCombineSingle():
    # one object in a bin keeps its own percentage unchanged
    assert combineConfidences([0.63]) == pytest.approx(0.63)


def testCombineEmpty():
    assert combineConfidences([]) == 0.0


def testCombineClamped():
    assert combineConfidences([1.5, -0.3]) == pytest.approx(1.0)


def testMilkCartonOneVote():
    # 30 boxes at 63% dedupe to one object, still counts as one 63%
    dets = [makeDet("milk carton", 0.63, 10, 10, 210, 210) for _ in range(30)]
    objects = dedupeDetections(dets)
    verdict = pileVerdict(objects)
    assert len(verdict) == 1
    assert verdict[0]["bin_type"] == "Special — Green@Community"
    assert verdict[0]["count"] == 1
    assert verdict[0]["confidence"] == pytest.approx(0.63)


def testSpecExampleGroupedByBin():
    # newspaper + cardboard box -> Paper 95.52%; cup stays its own General 63%
    dets = [
        makeDet("newspaper", 0.72, 0, 0, 50, 50),
        makeDet("cardboard box", 0.84, 100, 100, 200, 200),
        makeDet("paper cup", 0.63, 300, 300, 400, 400),
    ]
    verdict = pileVerdict(dets)
    assert len(verdict) == 2
    byBin = {v["bin_type"]: v for v in verdict}
    assert byBin["Paper"]["confidence"] == pytest.approx(0.9552)
    assert byBin["Paper"]["count"] == 2
    assert byBin["General waste"]["confidence"] == pytest.approx(0.63)
    assert verdict[0]["bin_type"] == "Paper"


def testVerdictSortedByConfidence():
    dets = [
        makeDet("banana", 0.90, 0, 0, 50, 50),
        makeDet("newspaper", 0.72, 100, 100, 200, 200),
    ]
    verdict = pileVerdict(dets)
    assert verdict[0]["bin_type"] == "General waste (food)"
    assert verdict[0]["confidence"] == pytest.approx(0.90)


def testNoBoxesKeptWithoutBox():
    dets = [{"class": "apple", "conf": 0.9}]
    assert dedupeDetections(dets) == dets
    assert len(pileVerdict(dets)) == 1


def testSingleLowConfidenceNoSplit():
    # one shy object (below WEAK) is low confidence, never a "mixed pile"
    v = pileVerdict([makeDet("apple", 0.20, 0, 0, 50, 50)])
    assert len(v) == 1
    assert v[0]["confidence"] == pytest.approx(0.20)
