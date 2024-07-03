import pandas as pd

# Load the scraped data
df = pd.read_csv("CarsData.csv")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna("NaN", inplace=True)
df.dropna(subset="Brand", inplace=True)

# Standardize date formats if necessary
df["Announcement_date"] = pd.to_datetime(df["Announcement_date"], errors="coerce")

# Save cleaned data
df.to_csv("CleanedCarsData.csv", index=False)
