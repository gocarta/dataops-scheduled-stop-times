# dataops-scheduled-stop-times
> Scheduled Arrival and Departure Times at Stops for CARTA Buses and Shuttles 

## background
We are trying build a GTFS Realtime feed by combining the data from our implementation of Clever's Bus Time API, our static GTFS data, and other data feeds.

## frequency
The pipeline automatically runs once a day to make sure we are in sync, but the underlying data only changes every several months.

## columns
| column | example | description |
| :--- | :--- | :--- |
| **route_id** | `"33"` | The name of the route. |
| **trip_id** | `1010` | The unique identifier of the trip in our static GTFS data. |
| **service_id** | `2` | Which type of service (e.g., weekday, Saturday, or Sunday) |
| **direction_id** | `1` | numerical identifier for the direction |
| **block_id** | `"3304DTS"` | GTFS Block ID |
| **shape_id** | `"shp-33-04"` | GTFS Shape ID |
| **stop_arrival_time** | `"14:26:56"` | Time the bus is scheduled to arrive at the stop |
| **stop_departure_time** | `"14:26:56"` | Time the bus is scheduled to leave from the stop |
| **stop_duration** | `0` | Time (in seconds) that the bus is supposed to dwell at the stop |
| **stop_id** | `794` | Identifier of the stop |
| **stop_code** | `1379` | Stop code |
| **stop_name** | `"Broad & 5th1"` | Human-friendly name of the stop |
| **longitude** | `-85.310790` | longitude location of the stop |
| **latitude** | `35.050629` | latitude location of the stop |
| **stop_sequence** | `4` | The stop number within the trip (e.g. 4th stop in the trip) |
| **stop_headsign** | `"CHOO CHOO"` | the headsign (what displays on the outward-facing bus sign) |
| **stop_pickup_type** | `0` | not sure what this means |
| **stop_drop_off_type** | `0` | not sure what this means |
| **shape_dist_traveled** | `418.71` | how far along the trip we've gone |
| **stop_timepoint** | `false` | whether the stop is a timepoint |
| **trip_start_time** | `"14:25:00"` | when the whole trip started |
| **trip_end_time** | `"14:37:00"` | when the trip is supposed to end |
| **trip_duration** | 720 | how long the trip is supposed to take in seconds |
| **trip_progress** | 116 | how many seconds through the trip the stop is supposed to be |


## download links
- [metadata](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/meta.json)
- [csv](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/data.csv)
- [geojson](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/data.points.geojson)
- [geoparquet](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/data.parquet)
- [json](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/data.json)
- [json lines](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/data.jsonl)
- [shapefile](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_stop_times/v1/data.points.shp.zip)

## preview links
- You can query the data with SQL using [duckdb](https://shell.duckdb.org/#queries=v0,CREATE-TABLE-dataset-AS-SELECT-*-FROM-'s3://gocarta/public/data/scheduled_stop_times/v1/data.parquet'~,Describe-dataset~).

## support
Post an issue [here](https://github.com/gocarta/dataops-scheduled-stop-times/issues) or email the package author at DanielDufour@gocarta.org.
