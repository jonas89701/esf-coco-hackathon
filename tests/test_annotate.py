# tests for annotate.py

from PIL import Image

from sortsmart.annotate import annotate_image


def make_img():
    return Image.new("RGB", (640, 480), "white")


def test_returns_image():
    out = annotate_image(make_img(), [])
    assert isinstance(out, Image.Image)


def test_original_not_changed():
    img = make_img()
    annotate_image(img, [{"box": [50, 60, 200, 300], "class": "bottle", "conf": 0.87}])
    # box starts at (50, 60), original should still be plain white there
    assert img.getpixel((50, 60)) == (255, 255, 255)


def test_box_drawn():
    out = annotate_image(make_img(), [{"box": [50, 60, 200, 300], "class": "bottle", "conf": 0.87}])
    # (50, 60) is the top-left of the box, should be the green outline now
    assert out.getpixel((50, 60)) != (255, 255, 255)


def test_empty_detections():
    out = annotate_image(make_img(), [])
    assert isinstance(out, Image.Image)


def test_no_box_skipped():
    # missing box / empty dict / box=None should all just get skipped
    out = annotate_image(make_img(), [{"class": "banana"}, {}, {"box": None}])
    assert isinstance(out, Image.Image)


def test_no_conf_ok():
    # conf isnt always there, label should just be the class name
    out = annotate_image(make_img(), [{"box": [10, 10, 100, 100], "class": "cup"}])
    assert isinstance(out, Image.Image)
