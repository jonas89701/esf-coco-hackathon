# src/mapping.py

WASTE_RULES = {
    #Plastic Bottles
    "bottle":             ("Plastic bottles", "Recyclable", "Rinse, remove cap & label"),
    "plastic bottle":     ("Plastic bottles", "Recyclable", "Rinse, remove cap & label"),

    #Metals
    "can":                ("Metals",          "Recyclable", "Rinse, remove label"),
    "aluminium can":      ("Metals",          "Recyclable", "Rinse, remove label"),

    #Glass
    "glass bottle":       ("Glass",           "Recyclable", "Rinse, remove cap; no broken glass"),

    #General Waste (Food Waste)
    "banana":             ("General waste (food)", "General", "Compost if your school has food waste collection"),
    "apple":              ("General waste (food)", "General", "Compost if your school has food waste collection"),
    "orange":             ("General waste (food)", "General", "Compost if your school has food waste collection"),
    "carrot":             ("General waste (food)", "General", "Compost if your school has food waste collection"),
    "broccoli":           ("General waste (food)", "General", "Compost if your school has food waste collection"),

    #General Waste (Cups & Containers)
    "paper cup":          ("General waste",   "General",    "Plastic-coated — not recyclable"),
    "plastic cup":        ("General waste",   "General",    "Not accepted in recycling bins"),
    "cup":                ("General waste",   "General",    "Not accepted in recycling bins"),
    "styrofoam container":("General waste",   "General",    "Not accepted in recycling bins"),
    "sandwich":           ("General waste",   "General",    "Greasy food waste — not recyclable"),
    "pizza":              ("General waste",   "General",    "Greasy food waste — not recyclable"),

    #Special Collection (Liquid Cartons)
    "milk carton":        ("Special — Green@Community", "Special", "Wash, dry, remove cap; NOT the street bin"),
    "liquid carton":      ("Special — Green@Community", "Special", "Wash, dry, remove cap; NOT the street bin"),
}

def map_waste_item(class_name: str) -> tuple:
    default_rule = ("Check locally", "Unsure", "Bin in general waste or check the item label")
    return WASTE_RULES.get(class_name.strip().lower(), default_rule)
