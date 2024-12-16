import unittest
from unittest.mock import patch, Mock
from bookscraper.models import Hotel, get_engine, get_session, create_tables

class TestModels(unittest.TestCase):
    @patch('bookscraper.models.create_engine')
    def test_get_engine(self, mock_create_engine):
        with patch('bookscraper.models.settings.DATABASE', {
            'drivername': 'postgresql',
            'username': 'test',
            'password': 'test',
            'host': 'localhost',
            'port': '5432',
            'database': 'test_db'
        }):
            get_engine()
            mock_create_engine.assert_called_once()

    @patch('bookscraper.models.sessionmaker')
    def test_get_session(self, mock_sessionmaker):
        mock_engine = Mock()
        mock_session = Mock()
        mock_sessionmaker.return_value = mock_session

        result = get_session(mock_engine)
        
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)
        self.assertEqual(result, mock_session())

    def test_hotel_model(self):
        hotel = Hotel(
            property_title="Test Hotel",
            rating=4.5,
            location="Test Location",
            latitude=51.5074,
            longitude=-0.1278,
            room_type="Standard",
            price="100",
            image_path="test.jpg"
        )

        self.assertEqual(hotel.property_title, "Test Hotel")
        self.assertEqual(hotel.rating, 4.5)
        self.assertEqual(hotel.location, "Test Location")
        self.assertEqual(hotel.latitude, 51.5074)
        self.assertEqual(hotel.longitude, -0.1278)
        self.assertEqual(hotel.room_type, "Standard")
        self.assertEqual(hotel.price, "100")
        self.assertEqual(hotel.image_path, "test.jpg")

if __name__ == '__main__':
    unittest.main()