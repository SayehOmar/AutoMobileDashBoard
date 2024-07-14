import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import shape
import altair as alt

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Cars_data"]
collection = db["Cars_data"]


# Fetch data from MongoDB
def fetch_data():
    cars = collection.find()
    car_list = []
    for car in cars:
        geometry = shape(car["geometry"]) if "geometry" in car else None
        car_list.append(
            {
                "Brand": car.get("Brand", ""),
                "Model": car.get("Model", ""),
                "Manufacture_year": car.get("Manufacture_year", ""),
                "Mileage": car.get("Mileage", ""),
                "Price": car.get("Price", ""),
                "Body_type": car.get("Body_type", ""),
                "Fuel": car.get("Fuel", ""),
                "Horse_Power": car.get("Horse_Power", ""),
                "Gear_box": car.get("Gear_box", ""),
                "Transmission": car.get("Transmission", ""),
                "Announcement_date": car.get("Announcement_date", ""),
                "Governorate": car.get("Governorate", ""),
                "Address": car.get("Address", ""),
                "Shape_Leng": car.get("Shape_Leng", ""),
                "Shape_Area": car.get("Shape_Area", ""),
                "ADM2_EN": car.get("ADM2_EN", ""),
                "geometry": geometry,
            }
        )
    return pd.DataFrame(car_list)


# Streamlit app
st.title("Car Dashboard")
st.write("This is a car dashboard displaying car information from MongoDB.")

# Fetch and display data
df = fetch_data()

# Genres selection - Create dropdown menu for genre selection
Brand_list = df.Brand.unique()
Brand_selection = st.multiselect(
    "Select Brand",
    Brand_list,
    ["Mercedes-Benz", "Mazda", "BMW", "Audi", "Volkswagen", "Fiat"],
)

# Price selection - Create slider for year range selection
Price_list = df.Price.unique()
Price_selection = st.slider("Select Price", 9000, 200000, (9000, 200000))
Price_selection_list = list(np.arange(Price_selection[0], Price_selection[1] + 1))


df_selection = df[
    df.Brand.isin(Brand_selection) & df["Price"].isin(Price_selection_list)
]
reshaped_df = df_selection.pivot_table(
    index="Price", columns="Brand", values="Mileage", aggfunc="sum", fill_value=0
)
reshaped_df = reshaped_df.sort_values(by="Price", ascending=False)


# Convert DataFrame to GeoDataFrame
def convert_to_geodataframe(df):
    gdf = gpd.GeoDataFrame(df, geometry="geometry")
    gdf = gdf.dropna(subset=["geometry"])  # Drop rows without geometry
    return gdf


gdf = convert_to_geodataframe(df_selection)
Tunisia = convert_to_geodataframe(df)
# Layout with columns
col1, space, col2 = st.columns([3, 0.5, 3])  # Adjust column widths as needed
with col1:
    st.data_editor(
        reshaped_df,
        use_container_width=True,
        column_config={"Price": st.column_config.TextColumn("Price Range")},
        num_rows="dynamic",
    )


with col2:
    st.header("Map")
    fig, ax = plt.subplots(1, figsize=(15, 15))

    Tunisia.plot(
        ax=ax,
        legend=True,
        edgecolor="black",
        facecolor="none",
        linewidth=0.4,
    )

    gdf.plot(
        column="Governorate",
        cmap="Reds",
        ax=ax,
        legend=True,
        edgecolor="black",
        linewidth=0.4,
        missing_kwds={"color": "#e9e8ea"},
    )

    ax.set_title("City occurrences based on Cars announcements")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    st.pyplot(fig)

# Column selection for scatter plot
st.title("Scatter Plot of Selected Columns")

all_columns = [
    "Mileage",
    "Price",
    "Body_type",
    "Fuel",
    "Horse_Power",
    "Gear_box",
    "Transmission",
]

print(all_columns)
x_axis = st.selectbox("Select X-axis", all_columns, index=all_columns.index("Price"))
y_axis = st.selectbox("Select Y-axis", all_columns, index=all_columns.index("Mileage"))

# Scatter plot of price vs. mileage correlation
st.header(f"{x_axis} vs. {y_axis} Correlation")
scatter_chart = (
    alt.Chart(df_selection)
    .mark_circle(size=60)
    .encode(
        x=x_axis,
        y=y_axis,
        color="Brand",
        tooltip=["Brand", "Model", "Price", "Mileage"],
    )
    .interactive()
)


st.altair_chart(scatter_chart, use_container_width=True)
