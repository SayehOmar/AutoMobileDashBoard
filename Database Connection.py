from sqlalchemy import create_engine
import geopandas as gpd

# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Create a SQLAlchemy engine
engine = create_engine("postgresql://postgres:0000@localhost:5432/Dash_Board_Data")


import psycopg2

try:
    # Replace 'your_password' with the actual password for the 'postgres' user
    conn = psycopg2.connect(
        dbname="Dash_Board_Data",
        user="postgres",
        host="localhost",
        port="5432",
    )
    print(f"{GREEN}Connection successful!")

    # Close the connection
    conn.close()

except psycopg2.Error as e:
    print("Connection failed:", e)

    # Test the connection

try:
    # Connect to the database
    with engine.connect() as conn:
        # Execute a simple query
        result = conn.execute(text("SELECT 1"))
        print(result.scalar())  # Should print '1' if the query executed successfully

except Exception as e:
    print("Error executing query:", e)

# Load the GeoDataFrame from the GeoPackage
# gdf = gpd.read_file("CleanedCarsData.gpkg", layer="cars_data")

# debug
# print(gdf.head(2))
# print(gdf.crs)
# print(gdf.geometry)


# Use GeoPandas to_sql method to insert the GeoDataFrame into PostgreSQL
# gdf.to_postgis("Cars_data", engine, if_exists="append")
