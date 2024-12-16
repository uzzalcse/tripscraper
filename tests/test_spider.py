import os
import shutil
import unittest
from unittest.mock import Mock, patch
from scrapy.http import TextResponse, Request
from bookscraper.spiders.city_hotels_spider import CityAndHotelsSpider

class TestCityAndHotelsSpider(unittest.TestCase):
    def setUp(self):
        self.spider = CityAndHotelsSpider()
        self.sample_response = Mock(spec=TextResponse)
        self.sample_response.url = 'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP'

    def tearDown(self):
        if os.path.exists('images'):
            shutil.rmtree('images')

    # def test_clear_previous_data(self):
    #     # Create a test directory
    #     os.makedirs('images', exist_ok=True)
    #     test_file = os.path.join('images', 'test.txt')
    #     with open(test_file, 'w') as f:
    #         f.write('test')

    #     self.spider.clear_previous_data()
    #     self.assertTrue(os.path.exists('images'))
    #     self.assertTrue(len(os.listdir('images')) == 0)

    # @patch('scrapy.Spider.logger')
    # def test_parse_with_valid_data(self, mock_logger):
    #     script_content = '''
    #     window.IBU_HOTEL = {
    #         "initData": {
    #             "htlsData": {
    #                 "inboundCities": [{"id": "123", "name": "London"}],
    #                 "outboundCities": [{"id": "456", "name": "Paris"}]
    #             }
    #         }
    #     };
    #     '''
        self.sample_response.xpath = Mock(return_value=[Mock(get=Mock(return_value=script_content))])
        
        results = list(self.spider.parse(self.sample_response))
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Request)

    def test_extract_hotel_data(self):
        hotel_data = {
            "hotelBasicInfo": {
                "hotelName": "Test Hotel",
                "price": "100",
                "hotelImg": "test.jpg"
            },
            "positionInfo": {
                "positionName": "City Center",
                "coordinate": {"lat": "51.5074", "lng": "-0.1278"}
            },
            "commentInfo": {"commentScore": "8.5"},
            "roomInfo": {"physicalRoomName": "Standard Room"}
        }

        result = self.spider.extract_hotel_data(hotel_data)
        
        self.assertEqual(result["property_title"], "Test Hotel")
        self.assertEqual(result["rating"], "8.5")
        self.assertEqual(result["location"], "City Center")
        self.assertEqual(result["latitude"], "51.5074")
        self.assertEqual(result["longitude"], "-0.1278")
        self.assertEqual(result["room_type"], "Standard Room")
        self.assertEqual(result["price"], "100")
        self.assertEqual(result["image_path"], "test.jpg")

    # @patch('requests.get')
    # def test_download_image(self, mock_get):
    #     mock_response = Mock()
    #     mock_response.status_code = 200
    #     mock_response.raw = Mock()
    #     mock_get.return_value = mock_response

    #     image_url = "https://example.com/test.jpg"
    #     result = self.spider.download_image(image_url)

    #     self.assertIsNotNone(result)
    #     self.assertTrue(result.startswith("images/"))

if __name__ == '__main__':
    unittest.main()