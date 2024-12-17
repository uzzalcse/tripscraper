
BOT_NAME = "bookscraper"

SPIDER_MODULES = ["tripscraper.spiders"]
NEWSPIDER_MODULE = "tripscraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Activate the PostgresPipeline
ITEM_PIPELINES = {
    'tripscraper.pipelines.PostgresPipeline': 300,
}

# Database configuration
DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',  # Replace with your username
    'password': 'password',      # Replace with your password
    'database': 'uzzaldb'   # Replace with your database name
}

