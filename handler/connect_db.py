from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sample.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
