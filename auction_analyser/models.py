from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Auction(Base):
    __tablename__ = 'auctions'

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, index=True)
    item_id = Column(Integer, index=True)
    stack_size = Column(Integer)
    bid_price = Column(Integer)
    buyout_price = Column(Integer)
    seller = Column(String)
    time_left = Column(Integer)
    timestamp = Column(Integer, index=True)

class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String)
    median_price = Column(Integer)
    last_seen = Column(Integer)


def get_engine(path: str):
    return create_engine(f'sqlite:///{path}')


def init_db(engine):
    Base.metadata.create_all(engine)


def get_session(path: str):
    engine = get_engine(path)
    init_db(engine)
    Session = sessionmaker(bind=engine)
    return Session()
