# tests for annotate.py

from PIL import Image

from src.annotate import annotateImage


def makeImg():
    return Image.new("RGB", (640, 480), "white")


def testReturnsImage():
    out = annotateImage(makeImg(), [])
    assert isinstance(out, Image.Image)


def testOriginalNotChanged():
    img = makeImg()
    annotateImage(img, [{"box": [50, 60, 200, 300], "class": "bottle", "conf": 0.87}])
    # box starts at (50, 60), original should still be plain white there
    assert img.getpixel((50, 60)) == (255, 255, 255)


def testBoxDrawn():
    out = annotateImage(makeImg(), [{"box": [50, 60, 200, 300], "class": "bottle", "conf": 0.87}])
    # (50, 60) is the top-left of the box, should be the green outline now
    assert out.getpixel((50, 60)) != (255, 255, 255)


def testEmptyDetections():
    out = annotateImage(makeImg(), [])
    assert isinstance(out, Image.Image)


def testNoBoxSkipped():
    # missing box / empty dict / box=None should all just get skipped
    out = annotateImage(makeImg(), [{"class": "banana"}, {}, {"box": None}])
    assert isinstance(out, Image.Image)


def testNoConfOk():
    # conf isnt always there, label should just be the class name
    out = annotateImage(makeImg(), [{"box": [10, 10, 100, 100], "class": "cup"}])
    assert isinstance(out, Image.Image)
