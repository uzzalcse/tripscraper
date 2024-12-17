# Trip.com Property Scraper

This project is a Scrapy-based web scraper designed to gather property information from Trip.com. It dynamically fetches details about properties, including titles, ratings, locations, coordinates, room types, prices, and images, storing the data in a PostgreSQL database. Images are saved locally, and their references are stored in the database for easy retrieval.

## Features
- Scrapes property data from [Trip.com](https://uk.trip.com/hotels/?locale=en-GB&curr=GBP).
- Stores scraped data in a PostgreSQL database using SQLAlchemy.
- Automatically creates database tables.
- Saves property images in a local directory and stores their references in the database.
- Provides 60% or higher code coverage.
- Includes a detailed `README.md` for usage guidelines.

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.8+**
2. **PostgreSQL 17**
3. **Git**


## Project Directory Structure

```
tripscraper/
│  
├── scrapy.cfg  
├── requirements.txt  
├── .gitignore  
├── README.md  
├── tests/  
│   ├── __init__.py  
│   ├── test_models.py  
│   ├── test_pipelines.py  
│   ├── test_items.py  
│   └── test_spider.py  
│
├── tripscraper/  
│   ├── __init__.py  
│   ├── items.py  
│   ├── middlewares.py  
│   ├── pipelines.py  
│   ├── settings.py  
│   ├── models.py  
│   └── spiders/  
│       ├── __init__.py  
│       └── city_hotels_spider.py

```



## Project Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/uzzalcse/tripscraper.git

   ```

2. **Go to the project directory**

   ```bash
   cd tripscraper

   ```





3. **Install Python Dependencies**


   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. **If above commands (No. 3) does not work**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```


5. **Build the project using dokcer**

   ```bash
   docker compose build

   ```

6. **Run the project using docker**

  ```bash
   docker compose up

   ```

## To see result first go to the following link

http://127.0.0.1:8080/ Log in using: 

```Email: admin@admin.com
Password: admin
```




## Connect pg admin with the postgresql database using the following things. Look for `hotels` table.  


```
DATABASE = {
    'drivername': 'postgresql',
    'host': 'db',
    'port': '5432',
    'username': 'postgres', 
    'password': 'postgres',     
    'database': 'trip_scraper'  
}

```



7. **Set Up PostgreSQL Database(If you don't use docker)**

   Go to the official postgre website and download the database according to your OS. https://www.postgresql.org/download/ 
   

 
   Ensure PostgreSQL is running and create a database. Go to the `settings.py` file and according to your database change the `DATABASE` configuration in `settings.py`. Or you can create a database as per the following database configuration.

   ```bash
   DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',  # Replace with your username
    'password': 'postgres',      # Replace with your password
    'database': 'trip_scraper'   # Replace with your database name
    }
   ```



## Running the Scraper(If you don't use docker)

1. **Basic Command**

   Run the Scrapy spider from `tripscraper/tripscraper/spiders/` directory. When you are in root directory the following commands will run the spider.

   ```bash
   cd tripscraper/spiders/
   scrapy crawl city_hotels
   ```

   This will start scraping and save data to the database. To see the result in database go to the `pgadmin` of your database. Then you will be able to see the results.





## Testing

Run the test suite using `pytest`. It will test with code coverage. You have to run the test from project root directory. If you are in some other directory like `spiders` you have to first go to the project root directory using `cd` command.

```bash
pytest --cov=tripscraper
```


## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries, please contact the project maintainer at uzzal.cse42@gmail.com

