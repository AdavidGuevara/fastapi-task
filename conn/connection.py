from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ["MYSQL_USER"]
password = os.environ["MYSQL_PASS"]
host = os.environ["MYSQL_HOST"]
database = os.environ["MYSQL_DB"]

DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}/{database}"

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()

Base = declarative_base()
