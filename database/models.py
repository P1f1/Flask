from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine("mysql+mysqlconnector://root:root@localhost/testdb", echo=True)
Base = declarative_base()


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text)
    price = Column(Float)
    inventory = relationship("Inventory")

    def __repr__(self):
        return f"Product: {self.name}"


class Locations(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    inventory = relationship("Inventory")

    def __repr__(self):
        return f"Locations: {self.name}"


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    quantity = Column(Integer, default=0)


Base.metadata.create_all(engine)
