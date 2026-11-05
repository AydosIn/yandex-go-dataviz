"""Step 2: convert drivers.csv into JSON and XML."""

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def typed(row):
    """CSV stores everything as text - restore the real types."""
    return {
        "driver_id": row["driver_id"],
        "full_name": row["full_name"],
        "car_model": row["car_model"],
        "join_date": row["join_date"],
        "rating": float(row["rating"]),
        "is_active": row["is_active"] == "True",
    }


with open(DATA_DIR / "drivers.csv", encoding="utf-8") as f:
    drivers = [typed(row) for row in csv.DictReader(f)]

# --- JSON ---
with open(DATA_DIR / "drivers.json", "w", encoding="utf-8") as f:
    json.dump({"department": "Driver Partnerships", "drivers": drivers},
              f, indent=2, ensure_ascii=False)

# --- XML ---
root = ET.Element("drivers", department="Driver Partnerships")
for d in drivers:
    driver_el = ET.SubElement(root, "driver", id=d["driver_id"])
    for field in ["full_name", "car_model", "join_date", "rating", "is_active"]:
        ET.SubElement(driver_el, field).text = str(d[field]).lower() \
            if field == "is_active" else str(d[field])

tree = ET.ElementTree(root)
ET.indent(tree, space="  ")
tree.write(DATA_DIR / "drivers.xml", encoding="utf-8", xml_declaration=True)

print(f"Converted {len(drivers)} drivers:")
print(f"  -> {DATA_DIR / 'drivers.json'}")
print(f"  -> {DATA_DIR / 'drivers.xml'}")
