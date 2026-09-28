# tests for mapping.py

from sortsmart.mapping import map_waste_item


def test_plastic_bottle():
    bin_type, flag, tip = map_waste_item("plastic bottle")
    assert bin_type == "Plastic bottles"
    assert flag == "Recyclable"
    assert "Rinse" in tip


def test_beverage_can():
    bin_type, flag, _ = map_waste_item("beverage can")
    assert bin_type == "Metals"
    assert flag == "Recyclable"


def test_glass_bottle():
    bin_type, flag, _ = map_waste_item("glass bottle")
    assert bin_type == "Glass"
    assert flag == "Recyclable"


def test_banana():
    # no organic bin kerbside in hk, food scraps are general waste
    bin_type, flag, _ = map_waste_item("banana")
    assert bin_type == "General waste (food)"
    assert flag == "General"


def test_milk_carton():
    bin_type, flag, _ = map_waste_item("milk carton")
    assert bin_type == "Special — Green@Community"
    assert flag == "Special"


def test_paper_cup_is_general():
    # coated cups look like paper but are never recyclable
    bin_type, flag, _ = map_waste_item("paper cup")
    assert bin_type == "General waste"
    assert flag == "General"


def test_unknown_is_unsure():
    # umbrella is a real wrong-detection from the sample scoring run
    bin_type, flag, tip = map_waste_item("umbrella")
    assert bin_type == "Check locally"
    assert flag == "Unsure"
    assert tip


def test_messy_input():
    # detector output wont always be clean, case/whitespace shouldnt matter
    assert map_waste_item("  Plastic Bottle ")[0] == "Plastic bottles"
    assert map_waste_item("")[1] == "Unsure"
