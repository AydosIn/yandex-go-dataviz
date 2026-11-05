"""
Generate synthetic data for two Yandex Go Uzbekistan departments.

  data/drivers.csv  - Driver Partnerships department (200 rows, 6 columns)
  data/rides.csv    - Ride Operations department     (300 rows, 7 columns)

Both files share `driver_id`, so they can be joined later for visualization.
The data is fictional but modelled on how Yandex Go works in Tashkent.
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(2026)  # same output every run

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Driver Partnerships department
# ---------------------------------------------------------------------------
MALE_FIRST = ["Aziz", "Bobur", "Doston", "Jasur", "Javlon", "Sardor", "Sherzod",
              "Otabek", "Rustam", "Ulugbek", "Akmal", "Timur", "Farrukh", "Aydos",
              "Bekzod", "Islom", "Nodir", "Shoxrux", "Kamol", "Alisher", "Davron",
              "Murod", "Anvar", "Oybek", "Zafar"]
FEMALE_FIRST = ["Dilnoza", "Madina", "Gulnora", "Malika", "Nigora", "Shahnoza",
                "Zarina", "Feruza"]
SURNAMES = ["Karimov", "Rahimov", "Tursunov", "Yusupov", "Abdullayev", "Ismoilov",
            "Nazarov", "Qodirov", "Saidov", "Ergashev", "Xolmatov", "Mirzayev",
            "Rashidov", "Sobirov", "Tojiboyev", "Umarov", "Hamidov", "Jumaniyozov",
            "Ortiqov", "Bakirov"]

# (model, share of fleet) - Chevrolet dominates Uzbek roads (UzAuto Motors)
CAR_MODELS = [
    ("Chevrolet Cobalt", 35), ("Chevrolet Nexia 3", 14), ("Chevrolet Gentra", 15),
    ("Chevrolet Onix", 10), ("Chevrolet Spark", 7), ("Chevrolet Malibu", 7),
    ("Chevrolet Tracker", 6), ("BYD Song Plus", 6),
]


def make_name():
    surname = random.choice(SURNAMES)
    if random.random() < 0.08:  # few women drive taxis
        return f"{random.choice(FEMALE_FIRST)} {surname}a"
    return f"{random.choice(MALE_FIRST)} {surname}"


def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


drivers = []
for i in range(1, 201):
    model = random.choices([m for m, _ in CAR_MODELS], [w for _, w in CAR_MODELS])[0]
    rating = round(min(5.0, random.triangular(4.3, 5.0, 4.9)), 2)
    drivers.append({
        "driver_id": f"DRV-{i:04d}",                                       # str
        "full_name": make_name(),                                          # str
        "car_model": model,                                                # category
        "join_date": random_date(date(2019, 3, 1), date(2026, 9, 30)).isoformat(),  # date
        "rating": rating,                                                  # float
        "is_active": random.random() < (0.9 if rating >= 4.7 else 0.55),   # bool
    })

with open(DATA_DIR / "drivers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=drivers[0].keys())
    writer.writeheader()
    writer.writerows(drivers)

# ---------------------------------------------------------------------------
# Ride Operations department
# ---------------------------------------------------------------------------
# (district, weight) - busier central districts get more pickups
DISTRICTS = [
    ("Yunusabad", 14), ("Chilanzar", 15), ("Mirzo Ulugbek", 13), ("Yakkasaray", 9),
    ("Shaykhantahur", 10), ("Mirabad", 11), ("Yashnabad", 8), ("Sergeli", 6),
    ("Uchtepa", 6), ("Almazar", 5), ("Bektemir", 2), ("Yangihayot", 1),
]

# tariff: (minimum fare, price per km) in UZS
TARIFFS = {
    "Start":    (9_000, 1_800),
    "Comfort":  (12_000, 2_400),
    "Comfort+": (16_000, 3_100),
    "Business": (30_000, 5_200),
}

# which tariffs each car qualifies for
CAR_TARIFFS = {
    "Chevrolet Spark":   ["Start"],
    "Chevrolet Nexia 3": ["Start", "Comfort"],
    "Chevrolet Cobalt":  ["Start", "Comfort"],
    "Chevrolet Gentra":  ["Start", "Comfort", "Comfort+"],
    "Chevrolet Onix":    ["Start", "Comfort", "Comfort+"],
    "Chevrolet Tracker": ["Comfort", "Comfort+"],
    "Chevrolet Malibu":  ["Comfort+", "Business"],
    "BYD Song Plus":     ["Comfort+", "Business"],
}

# relative demand per hour of day: morning and evening rush peaks
HOUR_WEIGHTS = [2, 1, 1, 1, 1, 2, 4, 9, 12, 8, 5, 5,
                6, 6, 5, 5, 6, 9, 12, 11, 8, 6, 5, 3]
RUSH_HOURS = {7, 8, 9, 17, 18, 19}

active_drivers = [d for d in drivers if d["is_active"]]
month_start = datetime(2026, 10, 1)

rides = []
for i in range(1, 301):
    driver = random.choice(active_drivers)
    tariff = random.choice(CAR_TARIFFS[driver["car_model"]])

    day = random.randint(0, 30)
    hour = random.choices(range(24), HOUR_WEIGHTS)[0]
    ride_time = month_start + timedelta(days=day, hours=hour, minutes=random.randint(0, 59))

    distance = round(min(35.0, random.lognormvariate(1.7, 0.6)), 1)  # mostly 3-10 km
    minimum, per_km = TARIFFS[tariff]
    surge = random.uniform(1.2, 1.6) if hour in RUSH_HOURS else 1.0
    fare = max(minimum, distance * per_km) * surge
    fare = int(round(fare / 500) * 500)  # app rounds to 500 so'm

    rides.append({
        "ride_id": f"RIDE-{i:05d}",                               # str
        "driver_id": driver["driver_id"],                         # str (foreign key)
        "ride_datetime": ride_time.strftime("%Y-%m-%d %H:%M"),    # datetime
        "pickup_district": random.choices([d for d, _ in DISTRICTS],
                                          [w for _, w in DISTRICTS])[0],  # category
        "tariff": tariff,                                         # category
        "distance_km": distance,                                  # float
        "fare_uzs": fare,                                         # int
    })

rides.sort(key=lambda r: r["ride_datetime"])
with open(DATA_DIR / "rides.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rides[0].keys())
    writer.writeheader()
    writer.writerows(rides)

print(f"Wrote {len(drivers)} drivers -> {DATA_DIR / 'drivers.csv'}")
print(f"Wrote {len(rides)} rides   -> {DATA_DIR / 'rides.csv'}")
