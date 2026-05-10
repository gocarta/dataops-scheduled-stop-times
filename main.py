# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datablob",
#     "requests",
#     "simple-env",
# ]
# ///
from collections import defaultdict
import csv
import datablob
import io
import requests
import simple_env as se
import zipfile

AWS_BUCKET_NAME = se.get("AWS_BUCKET_NAME")
if not AWS_BUCKET_NAME:
    raise Exception("[dataops-scheduled-stop-times] missing AWS_BUCKET_NAME")

AWS_BUCKET_PATH = se.get("AWS_BUCKET_PATH")
if not AWS_BUCKET_PATH:
    raise Exception("[dataops-scheduled-stop-times] missing AWS_BUCKET_PATH")

AWS_REGION = se.get("AWS_REGION")
if not AWS_REGION:
    raise Exception("[dataops-scheduled-stop-times] missing AWS_REGION")

GTFS_URL = se.get("GTFS_URL")
if not GTFS_URL:
    raise Exception("[dataops-scheduled-stop-times] missing GTFS_URL")


def calc_duration(start_time, end_time):
    start_hours, start_minutes, start_seconds = map(int, start_time.split(":"))
    start_ts = start_hours * 3600 + start_minutes * 60 + start_seconds
    end_hours, end_minutes, end_seconds = map(int, end_time.split(":"))
    end_ts = end_hours * 3600 + end_minutes * 60 + end_seconds

    if end_ts < start_ts:
        end_ts += 24 * 60 * 60

    return end_ts - start_ts


response = requests.get(GTFS_URL)
zip_data = io.BytesIO(response.content)

trip_stop_times = defaultdict(list)

direction_ids = {"0": "Outbound", "1": "Inbound"}

stop_times_count = 0
trips = {}
results = []

with zipfile.ZipFile(zip_data) as z:
    # group stop_times by trip
    with z.open("stop_times.txt") as f:
        for row in csv.DictReader(f.read().decode("utf-8-sig").splitlines()):
            stop_times_count += 1
            trip_id = int(row["trip_id"])
            trip_stop_times[trip_id].append(row)

    with z.open("trips.txt") as f:
        for row in csv.DictReader(f.read().decode("utf-8-sig").splitlines()):
            trip_id = int(row["trip_id"])

            trip = {
                "trip_id": trip_id,
                "route_id": row["route_id"],
                "service_id": int(row["service_id"]),
                "headsign": row["trip_headsign"],
                "direction_id": int(row["direction_id"]),
                "block_id": row["block_id"],
                "shape_id": row["shape_id"],
            }

            trips[trip_id] = trip

trip_count = len(trips.keys())

running_stop_time_count = 0

for trip_id, stop_times in trip_stop_times.items():
    num_stop_times = len(stop_times)
    stop_times_sorted = sorted(stop_times, key=lambda r: int(r["stop_sequence"]))
    trip_start_time = stop_times_sorted[0]["departure_time"]
    trip_end_time = stop_times_sorted[-1]["arrival_time"]
    trip_duration = calc_duration(trip_start_time, trip_end_time)

    for i_stop_time, stop_time in enumerate(stop_times):
        running_stop_time_count += 1
        # print("stop_time:", stop_time)
        arrival_time = stop_time["arrival_time"]
        departure_time = stop_time["departure_time"]
        stop_duration = calc_duration(arrival_time, departure_time)
        stop_id = stop_time["stop_id"]
        trip = trips[trip_id]

        trip_progress = calc_duration(trip_start_time, arrival_time)

        row = {
            "route_id": trip["route_id"],
            "trip_id": trip_id,
            "service_id": trip["service_id"],
            "direction_id": trip["direction_id"],
            "block_id": trip["block_id"],
            "shape_id": trip["shape_id"],
            "stop_arrival_time": arrival_time,
            "stop_departure_time": departure_time,
            "stop_duration": stop_duration,
            "stop_id": stop_id,
            "stop_sequence": int(stop_time["stop_sequence"]),
            "stop_headsign": stop_time["stop_headsign"],
            "stop_pickup_type": stop_time["pickup_type"],
            "stop_drop_off_type": stop_time["drop_off_type"],
            "shape_dist_traveled": float(stop_time["shape_dist_traveled"]),
            "stop_timepoint": stop_time["timepoint"] == "1",
            "trip_start_time": trip_start_time,
            "trip_end_time": trip_end_time,
            "trip_duration": trip_duration,
            "trip_progress": trip_progress,
        }
        results.append(row)
        # print(str(round(100 * running_stop_time_count / stop_times_count, 2)) + "%")

client = datablob.DataBlobClient(
    bucket_name=AWS_BUCKET_NAME, bucket_path=AWS_BUCKET_PATH
)

client.update_dataset(
    name="scheduled_stop_times",
    description="Scheduled Arrival and Departure Times at Stops for CARTA Buses and Shuttles",
    version="1",
    data=results,
    column_names=[
        "route_id",
        "trip_id",
        "service_id",
        "direction_id",
        "block_id",
        "shape_id",
        "stop_arrival_time",
        "stop_departure_time",
        "stop_duration",
        "stop_id",
        "stop_sequence",
        "stop_headsign",
        "stop_pickup_type",
        "stop_drop_off_type",
        "shape_dist_traveled",
        "stop_timepoint",
        "trip_start_time",
        "trip_end_time",
        "trip_duration",
        "trip_progress",
    ],
)

print(f"[dataops-scheduled-stop-times] updated {len(results)} rows")
