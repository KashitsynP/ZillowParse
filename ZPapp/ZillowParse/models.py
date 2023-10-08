from sqlalchemy import Date, Column, Integer, String, JSON, SMALLINT, ForeignKey, Computed, Float
from sqlalchemy.orm import relationship
from ZPapp.database import Base
# from app.users.schemas import RoleChoise


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    country = Column(String)
    listingStatus = Column(String)
    zpid = Column(String)
    price = Column(Float)
    livingArea = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)

    def __str__(self):
        return f'address: {self.address}, country: {self.country}, listingStatus: {self.listingStatus}, zpid: {self.zpid}, price: {self.price}'
