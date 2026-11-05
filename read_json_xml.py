"""Step 3: read the generated JSON and XML files and print their contents."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 200)

# --- JSON ---
with open(DATA_DIR / "drivers.json", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print(f"drivers.json  -  department: {data['department']}, {len(data['drivers'])} records")
print("=" * 80)
print("First record as raw JSON:")
print(json.dumps(data["drivers"][0], indent=2, ensure_ascii=False))
print()
print(pd.DataFrame(data["drivers"]).to_string(index=False))
print()

# --- XML ---
root = ET.parse(DATA_DIR / "drivers.xml").getroot()
records = []
for driver_el in root.findall("driver"):
    record = {"driver_id": driver_el.get("id")}
    record.update({child.tag: child.text for child in driver_el})
    records.append(record)

print("=" * 80)
print(f"drivers.xml  -  department: {root.get('department')}, {len(records)} records")
print("=" * 80)
print("First record as raw XML:")
first = root.find("driver")
ET.indent(first, space="  ")
print(ET.tostring(first, encoding="unicode").strip())
print()
print(pd.DataFrame(records).to_string(index=False))
