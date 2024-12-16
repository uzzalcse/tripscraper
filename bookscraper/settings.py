# Scrapy settings for bookscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "bookscraper"

SPIDER_MODULES = ["bookscraper.spiders"]
NEWSPIDER_MODULE = "bookscraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "bookscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Activate the PostgresPipeline
ITEM_PIPELINES = {
    'bookscraper.pipelines.PostgresPipeline': 300,
}

# Set the database URL
#DATABASE_URL = 'postgresql://postgres:emon@localhost:5432/postgres'

# Database configuration
DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',  # Replace with your username
    'password': 'emon',      # Replace with your password
    'database': 'postgres'   # Replace with your database name
}

