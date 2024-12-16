# import scrapy
# import json
# import re
# import random
# from bookscraper.items import HotelItem
# import requests
# import os
# import shutil

# class CityAndHotelsSpider(scrapy.Spider):
#     name = "city_hotels"
#     start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

#     def clear_previous_data(self):
#         folder_path = "images"
#         if os.path.exists(folder_path):
#             shutil.rmtree(folder_path)

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
#                 cities = inbound_cities or outbound_cities
#                 selected_city = random.choice(cities)

#                 city_id = selected_city["id"]
#                 city_name = selected_city["name"]

#                 city_url = f"https://uk.trip.com/hotels/list?city={city_id}"
#                 yield scrapy.Request(
#                     url=city_url,
#                     callback=self.parse_city_hotels,
#                     meta={"city_name": city_name}
#                 )

#     def parse_city_hotels(self, response):
#         city_name = response.meta["city_name"]

#         script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
#         if script_data:
#             json_match = re.search(r'window.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)
#             if json_match:
#                 raw_json = json_match.group(1)
#                 data = json.loads(raw_json)
#                 first_page_list = data.get("initData", {}).get("firstPageList", {})
#                 hotel_list = first_page_list.get("hotelList", [])

#                 for hotel in hotel_list:
#                     hotel_data = self.extract_hotel_data(hotel)
#                     item = HotelItem(city_name=city_name, **hotel_data)
#                     yield item

#     def extract_hotel_data(self, hotel):
#         hotel_basic_info = hotel.get("hotelBasicInfo", {})
#         positionInfo = hotel.get("positionInfo", {})
#         commentInfo = hotel.get("commentInfo", {})
#         return {
#             "property_title": hotel_basic_info.get("hotelName", "N/A"),
#             "rating": commentInfo.get("commentScore", "N/A"),
#             "location": positionInfo.get("positionName", "N/A"),
#             "latitude": positionInfo.get("coordinate", {}).get("lat", "N/A"),
#             "longitude": positionInfo.get("coordinate", {}).get("lng", "N/A"),
#             "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", "N/A"),
#             "price": hotel_basic_info.get("price", "N/A"),
#             "image_url": hotel_basic_info.get("hotelImg", "N/A"),
#             "image_path": None,
#         }




import scrapy
import json
import re
import random
import requests
import os
import shutil
from bookscraper.items import HotelItem

class CityAndHotelsSpider(scrapy.Spider):
    name = "city_hotels"
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def clear_previous_data(self):
        """Clear the previous images directory."""
        folder_path = "images"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)

    def parse(self, response):
        """Main entry point for the spider."""
        self.clear_previous_data()

        script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        if script_data:
            json_match = re.search(r'window.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)
            if json_match:
                raw_json = json_match.group(1)
                data = json.loads(raw_json)
                init_data = data.get("initData", {})
                htls_data = init_data.get("htlsData", {})
                inbound_cities = htls_data.get("inboundCities", [])
                outbound_cities = htls_data.get("outboundCities", [])
                cities = inbound_cities or outbound_cities
                selected_city = random.choice(cities)

                city_id = selected_city["id"]
                city_name = selected_city["name"]

                city_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                #city_url = 'https://uk.trip.com/hotels/list?city=733'
                yield scrapy.Request(
                    url=city_url,
                    callback=self.parse_city_hotels,
                    meta={"city_name": city_name}
                )

    def parse_city_hotels(self, response):
        """Parse hotel data for a specific city."""
        city_name = response.meta["city_name"]

        script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        if script_data:
            json_match = re.search(r'window.IBU_HOTEL\s*=\s*(\{.*?\});', script_data, re.DOTALL)
            if json_match:
                raw_json = json_match.group(1)
                data = json.loads(raw_json)
                first_page_list = data.get("initData", {}).get("firstPageList", {})
                hotel_list = first_page_list.get("hotelList", [])

                for hotel in hotel_list:
                    hotel_data = self.extract_hotel_data(hotel)
                    image_path = self.download_image(hotel_data["image_url"])
                    hotel_data["image_path"] = image_path
                    item = HotelItem(city_name=city_name, **hotel_data)
                    yield item

    def extract_hotel_data(self, hotel):
        """Extract hotel data from JSON."""
        hotel_basic_info = hotel.get("hotelBasicInfo", {})
        positionInfo = hotel.get("positionInfo", {})
        commentInfo = hotel.get("commentInfo", {})
        return {
            "property_title": hotel_basic_info.get("hotelName", "N/A"),
            "rating": commentInfo.get("commentScore", "N/A"),
            "location": positionInfo.get("positionName", "N/A"),
            "latitude": positionInfo.get("coordinate", {}).get("lat", "N/A"),
            "longitude": positionInfo.get("coordinate", {}).get("lng", "N/A"),
            "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", "N/A"),
            "price": hotel_basic_info.get("price", "N/A"),
            "image_url": hotel_basic_info.get("hotelImg", "N/A"),
            "image_path": None,
        }

    def download_image(self, image_url):
        """Download an image and return its local path."""
        if not image_url or image_url == "N/A":
            return None

        folder_path = "images"
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_name = os.path.basename(image_url.split("?")[0])  # Remove query params
                image_path = os.path.join(folder_path, image_name)

                with open(image_path, "wb") as f:
                    shutil.copyfileobj(response.raw, f)

                return image_path
        except Exception as e:
            self.logger.error(f"Error downloading image: {e}")
            return None
