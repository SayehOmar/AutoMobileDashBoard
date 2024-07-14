# streamlit_app.py

import streamlit as st
from pymongo import MongoClient
import altair as alt
import pandas as pd
import numpy as np

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Cars_data"]
collection = db["Cars_data"]


# Fetch data from MongoDB
def fetch_data():
    cars = collection.find()
    car_list = []
    for car in cars:
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


# Subset data - Filter DataFrame based on selections
df_selection = df[
    df.Brand.isin(Brand_selection) & df["Price"].isin(Price_selection_list)
]
reshaped_df = df_selection.pivot_table(
    index="Price", columns="Brand", values="Mileage", aggfunc="sum", fill_value=0
)
reshaped_df = reshaped_df.sort_values(by="Price", ascending=False)

print("A    ", df_selection)

# Editable DataFrame - Allow users to made live edits to the DataFrame
df_editor = st.data_editor(
    reshaped_df,
    height=212,
    use_container_width=True,
    column_config={"Price": st.column_config.TextColumn("Price Range")},
    num_rows="dynamic",
)


# st.dataframe(df)
