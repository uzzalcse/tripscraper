# import scrapy
# import json
# import re
# import random
# import os
# import requests
# import shutil


# class CityAndHotelsSpider(scrapy.Spider):
#     name = "city_hotels"
#     start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

#     def clear_previous_data(self):
#         """Clear previous data and images."""
#         folder_path = "images"
#         if os.path.exists(folder_path):
#             shutil.rmtree(folder_path)  # Recursively delete the folder
#             self.log(f"Deleted folder: {folder_path}")

#         json_file = "city_hotels_data.json"
#         if os.path.exists(json_file):
#             os.remove(json_file)
#             self.log(f"Deleted file: {json_file}")

#     def parse(self, response):
#         self.clear_previous_data()

#         script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

#         if script_data:
#             json_match = re.search(r'window.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)
#             if json_match:
#                 raw_json = json_match.group(1)
#                 data = json.loads(raw_json)
#                 init_data = data.get("initData", {})
#                 htls_data = init_data.get("htlsData", {})
#                 inbound_cities = htls_data.get("inboundCities", [])
#                 outbound_cities = htls_data.get("outboundCities", [])
#                 print("outbound cities")
#                 inbound_or_outbound = random.choice([inbound_cities, outbound_cities,])
#                 if not inbound_or_outbound:
#                     self.log("No cities found in the data.")
#                     return

#                 # Extract city information
#                 cities = [{"name": city.get("name", "N/A"), "id": city.get("id", "N/A")} for city in inbound_or_outbound]

#                 print(cities)

#                 # Select one city
#                 selected_city = random.choice(cities)

#                 city_id = selected_city["id"]
#                 city_name = selected_city["name"]
#                 self.log(f"Selected city: {city_name} with ID: {city_id}")

#                 # Construct URL for the selected city's hotels page
#                 city_url = f"https://uk.trip.com/hotels/list?city={city_id}"

#                 # Make a request to fetch hotels for the selected city
#                 yield scrapy.Request(
#                     url=city_url,
#                     callback=self.parse_city_hotels,
#                     meta={"city_name": city_name}
#                 )
#             else:
#                 self.log("Failed to extract JSON data from script.")

#     def parse_city_hotels(self, response):
#         """Parse hotels from the selected city's hotel page."""
#         city_name = response.meta["city_name"]

#         script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

#         if script_data:
#             json_match = re.search(r'window.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)
#             if json_match:
#                 raw_json = json_match.group(1)
#                 data = json.loads(raw_json)
#                 init_data = data.get("initData", {})
#                 first_page_list = init_data.get("firstPageList", [])
#                 if not first_page_list:
#                     self.log(f"No hotel data found for city: {city_name}")
#                     return

#                 hotel_list = first_page_list.get("hotelList", [])
#                 if not hotel_list:
#                     self.log(f"No hotels found for city: {city_name}")
#                     return

#                 city_hotels = []

#                 for hotel in hotel_list:  # Process all hotels
#                     hotel_data = self.extract_hotel_data(hotel)

#                     # Download and save the image
#                     image_path = None
#                     if hotel_data["image_url"] != "N/A":
#                         image_path = self.download_image(hotel_data["image_url"], city_name, hotel_data["property_title"])

#                     # Append hotel data with image path
#                     hotel_data["image_path"] = image_path
#                     city_hotels.append(hotel_data)

#                 # Save city and hotel data to a JSON file
#                 self.save_to_json(city_name, city_hotels)

#                 self.log(f"Data for city '{city_name}' and its hotels has been saved.")
#             else:
#                 self.log("Failed to extract JSON data from script.")

#     def extract_hotel_data(self, hotel):
#         """Extract and structure hotel data."""
#         hotel_basic_info = hotel.get("hotelBasicInfo", {})
#         commentInfo = hotel.get("commentInfo", {})
#         positionInfo = hotel.get("positionInfo", {})
#         roomInfo = hotel.get("roomInfo", {})
#         return {
#             "property_title": hotel_basic_info.get("hotelName", "N/A"),
#             "rating": commentInfo.get("commentScore", "N/A"),
#             "location": positionInfo.get("positionName", "N/A"),
#             "latitude": positionInfo.get("coordinate", {}).get("lat", "N/A"),
#             "longitude": positionInfo.get("coordinate", {}).get("lng", "N/A"),
#             "room_type": roomInfo.get("physicalRoomName", "N/A"),
#             "price": hotel_basic_info.get("price", "N/A"),
#             "image_url": hotel_basic_info.get("hotelImg", "N/A"),
#         }

#     def download_image(self, image_url, city_name, hotel_name):
#         """Download image and save it to the images folder."""
#         folder_path = os.path.join("images", city_name)
#         os.makedirs(folder_path, exist_ok=True)

#         image_name = f"{hotel_name.replace(' ', '_')}.jpg"
#         image_path = os.path.join(folder_path, image_name)

#         try:
#             response = requests.get(image_url, stream=True)
#             if response.status_code == 200:
#                 with open(image_path, "wb") as f:
#                     for chunk in response.iter_content(1024):
#                         f.write(chunk)
#                 self.log(f"Image saved: {image_path}")
#                 return image_path
#             else:
#                 self.log(f"Failed to download image: {image_url}")
#                 return None
#         except Exception as e:
#             self.log(f"Error downloading image {image_url}: {e}")
#             return None

#     def save_to_json(self, city_name, city_hotels):
#         """Save city and hotel data to a JSON file."""
#         json_file = "city_hotels_data.json"

#         data = {}
#         if os.path.exists(json_file):
#             with open(json_file, "r") as f:
#                 data = json.load(f)

#         data[city_name] = city_hotels

#         with open(json_file, "w") as f:
#             json.dump(data, f, indent=4)

#         self.log(f"Data saved to {json_file}.")
