# Mapping rules
WASTE_RULES = {
    # Plastic Bottles
    "plastic bottle": ("Plastic bottles", "Recyclable", "Rinse, remove cap & label"),
    # Metals
    "beverage can": ("Metals", "Recyclable", "Rinse, remove label"),
    # Paper & Cardboard
    "paper": ("Paper", "Recyclable", "Clean & dry; remove staples & plastic covers"),
    "cardboard box": ("Paper", "Recyclable", "Flatten box; remove tape & staples"),
    # General Waste (Food Waste)
    "food": (
        "General waste (food)",
        "General",
        "Compost if your school has food waste collection",
    ),
    # General Waste (Cups & Containers)
    "paper cup": ("General waste", "General", "Plastic-coated — not recyclable"),
    "plastic cup": ("General waste", "General", "Not accepted in recycling bins"),
    "foam container": (
        "General waste",
        "General",
        "Not accepted in recycling bins",
    ),
    "plastic fork": ("General waste", "General", "Not accepted in recycling bins"),
    "plastic spoon": ("General waste", "General", "Not accepted in recycling bins"),
    # Special Collection (Liquid Cartons)
    "beverage carton": (
        "Special — Green@Community",
        "Special",
        "Wash, dry, remove cap; NOT the street bin",
    ),
    "liquid carton": (
        "Special — Green@Community",
        "Special",
        "Wash, dry, remove cap; NOT the street bin",
    ),
}


def map_waste_item(class_name: str) -> tuple:
    default_rule = (
        "Check locally",
        "Unsure",
        "Bin in general waste or check the item label",
    )
    return WASTE_RULES.get(class_name.strip().lower(), default_rule)
