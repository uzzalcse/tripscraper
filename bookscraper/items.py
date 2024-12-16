import scrapy

class HotelItem(scrapy.Item):
    city_name = scrapy.Field()
    property_title = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
