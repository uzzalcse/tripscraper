from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:emon@localhost:5432/postgres')

Base = declarative_base()
metadata = MetaData()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=False)
    property_title = Column(String, nullable=False)
    rating = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(String)
    price = Column(String)
    #image_url = Column(String)
    image_path = Column(String)

def get_engine():
    return create_engine(DATABASE_URL)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables(engine):
    Base.metadata.create_all(engine)
