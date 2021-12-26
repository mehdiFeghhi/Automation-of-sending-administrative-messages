import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from handler.model.modelDB import User

#for app
file_path = os.path.abspath(os.getcwd()) + "/handler/sample.db"
# for test
# file_path = os.path.abspath(os.getcwd()) + "/sample.db"
engine = create_engine('sqlite:///' + file_path, echo=True, connect_args={"check_same_thread": False})
# engine = create_engine('sqlite:///sample.db')
Session = sessionmaker(bind=engine)
session = Session()
x = session.query(User).all()
for row in x:
    print(row.firs_name)
