import unittest
from unittest.mock import Mock, patch
from tripscraper.pipelines import PostgresPipeline
from tripscraper.items import HotelItem

class TestPostgresPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = PostgresPipeline()
        self.spider = Mock()

    @patch('tripscraper.pipelines.get_engine')
    @patch('tripscraper.pipelines.create_tables')
    @patch('tripscraper.pipelines.get_session')
    def test_open_spider(self, mock_get_session, mock_create_tables, mock_get_engine):
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine
        mock_session = Mock()
        mock_get_session.return_value = mock_session

        self.pipeline.open_spider(self.spider)

        mock_get_engine.assert_called_once()
        mock_create_tables.assert_called_once_with(mock_engine)
        mock_get_session.assert_called_once_with(mock_engine)
        self.assertEqual(self.pipeline.session, mock_session)

    def test_close_spider(self):
        self.pipeline.session = Mock()
        self.pipeline.close_spider(self.spider)
        self.pipeline.session.close.assert_called_once()

    @patch('tripscraper.pipelines.Hotel')
    def test_process_item(self, mock_hotel):
        self.pipeline.session = Mock()
        item = HotelItem(
            property_title="Test Hotel",
            rating="4.5",
            location="Test Location",
            latitude="51.5074",
            longitude="-0.1278",
            room_type="Standard",
            price="100",
            image_path="test.jpg"
        )

        result = self.pipeline.process_item(item, self.spider)

        mock_hotel.assert_called_once()
        self.pipeline.session.add.assert_called_once()
        self.pipeline.session.commit.assert_called_once()
        self.assertEqual(result, item)

if __name__ == '__main__':
    unittest.main()