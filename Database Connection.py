import geopandas as gpd
import pandas as pd

from pymongo import MongoClient
import json


# ANSI escape codes for colored output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


# Read the GPKG file
gdf = gpd.read_file("CleanedCarsData.gpkg")

# Export to GeoJSON
gdf.to_file("CleanedCarsData.geojson", driver="GeoJSON")
print(f"{YELLOW}", gdf.head(3))

client = MongoClient("mongodb://localhost:27017")

# Convert geometries to GeoJSON format
gdf["geometry"] = gdf["geometry"].apply(
    lambda geom: json.loads(json.dumps(geom.__geo_interface__))
)

# Handle NaT values in datetime columns
for column in gdf.select_dtypes(include=["datetime64[ns, UTC]", "datetime64[ns]"]):
    gdf[column] = gdf[column].apply(lambda x: x.isoformat() if pd.notnull(x) else None)


data = gdf.to_dict(orient="records")


database = client["Cars_data"]


try:
    # Delete all existing documents in the collection
    if database.Cars_data.delete_many({}):
        print("Old data is deleted")

    # Insert the data into MongoDB
    result = database.Cars_data.insert_many(data)
    print(f"{GREEN}Inserted {len(result.inserted_ids)} documents Correctly ")
except Exception as e:
    print(f"{RED}Failed to insert data: {e}")
