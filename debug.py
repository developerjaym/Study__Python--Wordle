#!/usr/bin/env python3


from sqlalchemy import (
                        create_engine)
from sqlalchemy.orm import sessionmaker

from game import Application
from seed import seeder
from models import Base

if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
     # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()
    seeder(session)
    application = Application(session)
    application.start()

    