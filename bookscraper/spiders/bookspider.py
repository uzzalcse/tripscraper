# import scrapy


# class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com"]

#     def parse(self, response):
#         books = response.css('article.product_pod')
#         for book in books:
#             yield {
#                 'name' : book.css('h3 a::text').get(),
#                 'price' :  book.css('.product_price .price_color::text').get(),
#                 'url' :  book.css('h3 a').attrib['href'],
#             }

#         next_page = response.css('li.next a ::attr(href)').get()

#         if next_page is not None:
#             # if 'catalogue/' in next_page:
#             #     next_page_url = 'https://books.toscrape.com' + next_page
#             # else:
#             #     next_page_url = 'https://books.toscrape.com/catalogue' + next_page
#             yield response.follow(next_page, callback=self.parse)



import scrapy
import json
import re
import os

class HotelsSpider(scrapy.Spider):
    name = "hotels_spider"
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def parse(self, response):
        # Extract the <script> tag containing `window.IBU_HOTEL`
        script_content = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()

        if script_content:
            # Use regex to extract the JSON object from the script content
            json_data_match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*});', script_content)

            if json_data_match:
                try:
                    # Load the JSON data
                    json_data = json.loads(json_data_match.group(1))

                    # Navigate to `htlsData` inside `initData`
                    hotels_data_inbound = json_data.get('initData', {}).get('htlsData', {}).get('inboundCities', [])
                    hotels_data_outbound = json_data.get('initData', {}).get('htlsData', {}).get('outboundCities', [])

                    # Combine data into a single dictionary
                    hotels_combined_data = {
                        "inboundHotels": hotels_data_inbound,
                        "outboundHotels": hotels_data_outbound
                    }

                    # Save combined hotel data to a JSON file
                    output_file = 'hotels_combined_data.json'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(hotels_combined_data, f, ensure_ascii=False, indent=4)

                    self.logger.info(f"Saved combined hotel data to {output_file}")

                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON parsing error: {e}")
            else:
                self.logger.error("No match found for JSON data in script content.")
        else:
            self.logger.error("Script containing 'window.IBU_HOTEL' not found.")
