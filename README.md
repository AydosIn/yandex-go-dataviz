# Yandex Go Uzbekistan — Data Visualization Prep

Synthetic data for two departments of **Yandex Go** in Tashkent:

| File | Department | Rows × Cols | Columns |
|---|---|---|---|
| `data/drivers.csv` | Driver Partnerships | 200 × 6 | `driver_id` (str), `full_name` (str), `car_model` (category), `join_date` (date), `rating` (float), `is_active` (bool) |
| `data/rides.csv` | Ride Operations | 300 × 7 | `ride_id` (str), `driver_id` (str), `ride_datetime` (datetime), `pickup_district` (category), `tariff` (category), `distance_km` (float), `fare_uzs` (int) |

The files share `driver_id`, so rides can be joined to drivers.

Patterns built into the data, for the visualization part of the course:
- Most of the fleet is Chevrolet (Cobalt, Gentra, Nexia), plus a few BYD EVs
- Morning (07–09) and evening (17–19) rush peaks with surge pricing of 1.2–1.6×
- Busier central districts (Chilanzar, Yunusabad, Mirzo Ulugbek)
- Tariffs depend on the car: a Spark only does Start, Business needs a Malibu or BYD
- Drivers with lower ratings are more likely to be inactive

## Run

Works in Anaconda (pandas is included) or any Python 3.9+ with pandas:

```bash
python generate_data.py     # create the two CSV files (fixed seed, same output every run)
python read_csv_files.py    # task 1: read and print both CSVs
python convert_formats.py   # task 2: drivers.csv -> drivers.json + drivers.xml
python read_json_xml.py     # task 3: read and print the JSON and XML files
```
