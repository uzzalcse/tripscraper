# from bookscraper.models import Hotel, get_engine, get_session, create_tables

# class PostgresPipeline:

#     def open_spider(self, spider):
#         engine = get_engine()
#         create_tables(engine)  # Create tables dynamically
#         self.session = get_session(engine)

#     def close_spider(self, spider):
#         self.session.close()

#     def process_item(self, item, spider):
#         # Save data to PostgreSQL
#         hotel = Hotel(
#             #city_name=item['city_name'],
#             property_title=item['property_title'],
#             rating=item['rating'],
#             location=item['location'],
#             latitude=item['latitude'],
#             longitude=item['longitude'],
#             room_type=item['room_type'],
#             price=item['price'],
#             #image_url=item['image_url'],
#             image_path=item['image_path']
#         )
#         self.session.add(hotel)
#         self.session.commit()
#         return item

from bookscraper.models import Hotel, get_engine, get_session, create_tables

class PostgresPipeline:

    def open_spider(self, spider):
        engine = get_engine()
        create_tables(engine)  # Create tables dynamically
        self.session = get_session(engine)

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        # Save data to PostgreSQL
        hotel = Hotel(
            property_title=item['property_title'],
            rating=float(item['rating']) if item['rating'] else None,  # Convert to float, handle empty
            location=item['location'] if item['location'] else None,  # Handle empty
            latitude=float(item['latitude']) if item['latitude'] else None,
            longitude=float(item['longitude']) if item['longitude'] else None,
            room_type=item['room_type'] if item['room_type'] else None,  # Handle empty
            price=item['price'] if item['price'] else None,  # Handle empty
            image_path=item['image_path'] if item['image_path'] else 'images\\nophoto.png'  # Default image path
        )
        self.session.add(hotel)
        self.session.commit()
        return item
