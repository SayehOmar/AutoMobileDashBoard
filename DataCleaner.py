import pandas as pd
import geopandas as gpd

# Load the scraped data
df = pd.read_csv("CarsData.csv")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna("NaN", inplace=True)
df.dropna(subset="Brand", inplace=True)

# Standardize date formats if necessary
df["Announcement_date"] = pd.to_datetime(df["Announcement_date"], errors="coerce")


Tunisia = gpd.read_file("shpfile/Tunisia.shp")

# Save cleaned data
df.to_csv("CleanedCarsData.csv", index=False)


Tunisia["ADM2_EN"] = Tunisia["ADM2_EN"].str.strip()
df["Governorate"] = df["Governorate"].str.strip()

# All upercase

Tunisia["ADM2_EN"] = Tunisia["ADM2_EN"].str.upper()
df["Governorate"] = df["Governorate"].str.upper()

# Perform the merge
gdf = df.merge(Tunisia, left_on="Governorate", right_on="ADM2_EN", how="outer")


# Convert the merged DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(gdf, geometry="geometry")

# Save the GeoDataFrame to a GeoPackage
gdf.to_file("CleanedCarsData.gpkg", layer="cars_data", driver="GPKG")
