from sqlalchemy import create_engine
from models import Base, Products, Locations, Inventory
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+mysqlconnector://root:root@localhost/testdb", echo=True)
Session = sessionmaker(engine)
s = Session()

p1 = Products(name="Телефон", description="Китайский", price=10000.00)
p2 = Products(name="Ноутбук", description="Китайский", price=30000.00)
p3 = Products(name="Планшет", description="Китайский", price=20000.00)

l1 = Locations(name="А1")
l2 = Locations(name="Б2")
l3 = Locations(name="В3")

i1 = Inventory(product_id=1, location_id=1, quantity=50)
i2 = Inventory(product_id=2, location_id=2, quantity=10)
i3 = Inventory(product_id=3, location_id=3, quantity=30)
i4 = Inventory(product_id=3, location_id=1, quantity=5)
i5 = Inventory(product_id=1, location_id=2, quantity=100)

s.add_all([p1, p2, p3, l1, l2, l3, i1, i2, i3, i4, i5])
s.commit()
s.close()
