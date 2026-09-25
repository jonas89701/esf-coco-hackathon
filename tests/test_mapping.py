# tests for mapping.py

from src.mapping import map_waste_item


def testPlasticBottle():
    binType, flag, tip = map_waste_item("plastic bottle")
    assert binType == "Plastic bottles"
    assert flag == "Recyclable"
    assert "Rinse" in tip


def testBeverageCan():
    binType, flag, _ = map_waste_item("beverage can")
    assert binType == "Metals"
    assert flag == "Recyclable"


def testGlassBottle():
    binType, flag, _ = map_waste_item("glass bottle")
    assert binType == "Glass"
    assert flag == "Recyclable"


def testBanana():
    # no organic bin kerbside in hk, food scraps are general waste
    binType, flag, _ = map_waste_item("banana")
    assert binType == "General waste (food)"
    assert flag == "General"


def testMilkCarton():
    binType, flag, _ = map_waste_item("milk carton")
    assert binType == "Special — Green@Community"
    assert flag == "Special"


def testPaperCupIsGeneral():
    # coated cups look like paper but are never recyclable
    binType, flag, _ = map_waste_item("paper cup")
    assert binType == "General waste"
    assert flag == "General"


def testUnknownIsUnsure():
    # umbrella is a real wrong-detection from the sample scoring run
    binType, flag, tip = map_waste_item("umbrella")
    assert binType == "Check locally"
    assert flag == "Unsure"
    assert tip


def testMessyInput():
    # detector output wont always be clean, case/whitespace shouldnt matter
    assert map_waste_item("  Plastic Bottle ")[0] == "Plastic bottles"
    assert map_waste_item("")[1] == "Unsure"
