# models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact_Details(Base):
    __tablename__ = "Contact_Details"
    Sl_NO = Column(Integer, primary_key=True)
    phone = Column(String)
    Contact_First_Name = Column(String)
    Contact_Last_Name = Column(String)
    Contact_Designation = Column(String)
    Contact_eMail = Column(String)

class Intrest_Table(Base):
    __tablename__ = "Intrest_Table"
    Id = Column(Integer, primary_key=True)
    Sl_NO = Column(Integer, ForeignKey("Contact_Details.Sl_NO"))
    Interest = Column(String)
