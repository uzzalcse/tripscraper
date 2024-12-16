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
            city_name=item['city_name'],
            property_title=item['property_title'],
            rating=item['rating'],
            location=item['location'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            room_type=item['room_type'],
            price=item['price'],
            image_url=item['image_url'],
            image_path=item['image_path']
        )
        self.session.add(hotel)
        self.session.commit()
        return item
