# src/mapping.py

WASTE_RULES = {
    #Blue Bin: Plastics & Metals
    "bottle":   ("Blue — Plastics & Metals", "Recyclable", "Rinse, remove lid/cap"),
    "cup":      ("Blue — Plastics & Metals", "Recyclable", "Rinse, remove lid/cap"),
    "bowl":     ("Blue — Plastics & Metals", "Recyclable", "Rinse, remove lid/cap"),
    "fork":     ("Blue — Plastics & Metals", "Recyclable", "Wipe clean, flatten if possible"),
    "knife":    ("Blue — Plastics & Metals", "Recyclable", "Wipe clean, flatten if possible"),
    "spoon":    ("Blue — Plastics & Metals", "Recyclable", "Wipe clean, flatten if possible"),
    "can":      ("Blue — Plastics & Metals", "Recyclable", "Wipe clean, flatten if possible"),

    #Yellow Bin: Waste Paper
    "book":     ("Yellow — Waste Paper",     "Recyclable", "Keep dry, remove plastic coatings"),
    "paper":    ("Yellow — Waste Paper",     "Recyclable", "Keep dry and clean"),

    #Green Bin: Glass
    "wine glass": ("Green — Glass Bin",      "Recyclable", "Rinse clean, do not break"),

    #Brown Bin: Organic Waste
    "banana":   ("Brown — Organic Waste",    "Organic",    "No prep needed"),
    "apple":    ("Brown — Organic Waste",    "Organic",    "No prep needed"),
    "orange":   ("Brown — Organic Waste",    "Organic",    "No prep needed"),
    "carrot":   ("Brown — Organic Waste",    "Organic",    "Compost if available"),
    "broccoli": ("Brown — Organic Waste",    "Organic",    "Compost if available"),

    #Grey Bin: General Waste
    "sandwich": ("Grey — General Waste",     "General",    "Greasy food waste — not recyclable"),
    "pizza":    ("Grey — General Waste",     "General",    "Greasy food waste — not recyclable"),
    "hot dog":  ("Grey — General Waste",     "General",    "Greasy food waste — not recyclable"),
    "donut":    ("Grey — General Waste",     "General",    "Food waste — bin in general"),
    "cake":     ("Grey — General Waste",     "General",    "Food waste — bin in general"),
}

def map_waste_item(class_name: str) -> tuple:
    default_rule = ("Check locally", "Unsure", "Bin in general waste or check the item label")
    return WASTE_RULES.get(class_name.lower(), default_rule)