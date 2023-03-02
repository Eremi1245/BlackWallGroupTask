from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
host = os.environ['POSTGRESQL_HOST']
user = os.environ['POSTGRESQL_USER']
passw = os.environ['POSTGRESQL_PASSWORD']
db = os.environ['POSTGRESQL_DB']

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{passw}@{host}/{db}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
