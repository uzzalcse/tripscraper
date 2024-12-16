import pytest
from bookscraper.items import HotelItem

def test_hotel_item():
    item = HotelItem(
        city_name="Test City",
        property_title="Test Hotel",
        rating=4.5,
        location="Test Location",
        latitude=51.5074,
        longitude=-0.1278,
        room_type="Single",
        price="£100",
        image_path="images/test.jpg"
    )
    assert item['property_title'] == "Test Hotel"
    assert item['rating'] == 4.5
