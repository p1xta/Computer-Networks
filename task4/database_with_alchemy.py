from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL = "postgresql://postgres:angl496sql@localhost:5432/parsed_site"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase): pass

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(String)
    year = Column(String)
    mileage = Column(String)
    engine_capacity = Column(String)
    horse_powers = Column(String)
    fuel_type = Column(String)
    transmission = Column(String)
    car_type = Column(String)
    drive = Column(String)
    color = Column(String)

def save_to_db(data):
    session = SessionLocal()
    try:
        cars = [Car(**entry) for entry in data]
        session.add_all(cars)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_from_db():
    session = SessionLocal()
    try:
        cars = session.query(Car).all()
        return [car.__dict__ for car in cars]
    finally:
        session.close()