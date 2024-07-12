import requests
from bs4 import BeautifulSoup
import pandas as pd


# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Accessing the website and extracting the div containing the HREF
base_url = "https://www.automobile.tn/fr/occasion/"
page_number = 1
href = []

while True:
    url = f"{base_url}{page_number}"
    print("Fetching URL:", url)
    response = requests.get(url)

    if response.status_code != 200 or page_number > 50:
        break

    soup = BeautifulSoup(response.content, "html.parser")
    car_announcements = soup.find_all("div", class_="occasion-item-v2")

    for announcement in car_announcements:
        link = announcement.find("a")["href"]

        if "financement-zitouna" not in link and "vendeurs-pro" not in link:
            href.append(link)
            print(link, "is appended to the href list")

    page_number += 1


# Function to request the html of each link provided by the href list
def extract(href):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0"
    }
    url = f"https://www.automobile.tn{href}"
    r = requests.get(url, headers=headers)
    print(f"{GREEN} {url} {RESET}")
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


# Creating Lists to contain the data
Brand = []
Model = []
Manufacture_year = []
Mileage = []
Price = []
Body_type = []
Fuel = []
Horse_Power = []
Gear_box = []
Transmission = []
Exterior_Color = []
Interior_Color = []
Seating = []
Doors = []
Announcement_date = []
Governorate = []
Address = []

# Extracting the data
for link in href:
    soup = extract(link)
    price_div = soup.find("div", class_="price")
    price = price_div.get_text(strip=True).replace("DT", "") if price_div else None
    Price.append(price)

    main_specs = soup.find("div", class_="main-specs")
    if main_specs:
        specs = main_specs.find_all("li")
        spec_dict = {
            spec.find("span", class_="spec-name")
            .get_text(strip=True): spec.find("span", class_="spec-value")
            .get_text(strip=True)
            for spec in specs
        }

        Mileage.append(spec_dict.get("Kilométrage", None))
        Manufacture_year.append(spec_dict.get("Mise en circulation", None))
        Fuel.append(spec_dict.get("Énergie", None))
        Horse_Power.append(spec_dict.get("Puissance fiscale", None))
        Gear_box.append(spec_dict.get("Boite vitesse", None))
        Transmission.append(spec_dict.get("Transmission", None))
        Body_type.append(spec_dict.get("Carrosserie", None))
        Announcement_date.append(spec_dict.get("Date de l'annonce", None))
        Governorate.append(spec_dict.get("Gouvernorat", None))
    else:
        Mileage.append(None)
        Manufacture_year.append(None)
        Fuel.append(None)
        Horse_Power.append(None)
        Gear_box.append(None)
        Transmission.append(None)
        Body_type.append(None)
        Governorate.append(None)
        Announcement_date.append(None)

    # Extracting brand and type from the header
    divided_specs = soup.find("div", class_="divided-specs")
    if divided_specs:
        specs = divided_specs.find_all("li")
        spec_dict = {
            spec.find("span", class_="spec-name")
            .get_text(strip=True): spec.find("span", class_="spec-value")
            .get_text(strip=True)
            for spec in specs
        }

        Brand.append(spec_dict.get("Marque", None))
        Model.append(spec_dict.get("Modèle", None))
        Exterior_Color.append(spec_dict.get("Couleur extérieure", None))
        Interior_Color.append(spec_dict.get("Couleur intérieure", None))
        Seating.append(spec_dict.get("Nombre de places", None))
        Doors.append(spec_dict.get("Nombre de portes", None))
    else:
        Brand.append(None)
        Model.append(None)
        Exterior_Color.append(None)
        Interior_Color.append(None)
        Seating.append(None)
        Doors.append(None)

    address_element = soup.find("p", class_="address")
    Address.append(address_element.get_text(strip=True) if address_element else None)


# Check the length of each list
data_lists = [
    Brand,
    Model,
    Manufacture_year,
    Mileage,
    Price,
    Body_type,
    Fuel,
    Horse_Power,
    Gear_box,
    Transmission,
    Announcement_date,
    Governorate,
    Address,
]
list_names = [
    "Brand",
    "Type",
    "Manufacture_year",
    "Mileage",
    "Price",
    "Body_type",
    "Fuel",
    "Horse_Power",
    "Gear_box",
    "Transmission",
    "Announcement_date",
    "Governorate",
    "Address",
]

# Check lengths and find the minimum length
min_length = min(len(data_list) for data_list in data_lists)
print("Minimum list length:", min_length)

for name, data_list in zip(list_names, data_lists):
    print(f"{name} length: {len(data_list)}")
    # Truncate lists to the minimum length
    if len(data_list) > min_length:
        data_list = data_list[:min_length]


# Collecting the data
Cars_data = {
    "Brand": Brand,
    "Model": Model,
    "Manufacture_year": Manufacture_year,
    "Mileage": Mileage,
    "Price": Price,
    "Body_type": Body_type,
    "Fuel": Fuel,
    "Horse_Power": Horse_Power,
    "Gear_box": Gear_box,
    "Transmission": Transmission,
    "Announcement_date": Announcement_date,
    "Governorate": Governorate,
    "Address": Address,
}

df = pd.DataFrame(Cars_data)
df.to_csv("CarsData.csv", index=False)
