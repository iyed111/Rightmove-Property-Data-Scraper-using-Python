from bs4 import BeautifulSoup
import requests
import csv
import os

# Mapping of regions to their corresponding Rightmove location identifiers
REGION_MAPPING = {
    "london": "REGION^87490",
    "manchester": "REGION^904",
    "birmingham": "REGION^162",
    "leeds": "REGION^787",
    "bristol": "REGION^182",
    "glasgow": "REGION^1255",
    "liverpool": "REGION^872",
    "newcastle": "REGION^984"
}

def scrape_houses(region):
    region_cleaned = region.strip().lower()

    location_identifier = REGION_MAPPING.get(region_cleaned)
    if not location_identifier:
        print(f"Error: The region '{region}' is not recognized. Please check your input.")
        return

    url = f"https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier={location_identifier}&insId=1&radius=0.0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    house_listings = soup.find_all(class_="propertyCard")
    print(f"Found {len(house_listings)} property listings in {region.capitalize()}.")

    for listing in house_listings:
        try:
            #address
            address_tag = listing.find("address", class_="propertyCard-address")
            address = address_tag.text.strip() if address_tag else "Address not available"

            #price
            price_tag = listing.find(class_="propertyCard-priceValue")
            price = price_tag.text.strip() if price_tag else "Price not available"

            #details
            details_tag = listing.find(class_="propertyCard-details")
            details = details_tag.text.strip() if details_tag else "Details not available"

            print(f"Address: {address}")
            print(f"Price: {price}")
            print(f"Details: {details}")
            print("-" * 50)  #for readability
        except Exception as e:
            print(f"An error occurred while extracting data: {e}")
            continue

if __name__ == "__main__":
    print("Welcome to the Rightmove Property Scraper!")
    print("Here are some regions you can search for:")
    print("- London")
    print("- Manchester")
    print("- Birmingham")
    print("- Leeds")
    print("- Bristol")
    print("- Glasgow")
    print("- Liverpool")
    print("- Newcastle")

    region = input("Enter the name of the region you want to search for: ").strip()


scrape_houses(region)