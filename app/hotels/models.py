from sqlalchemy import Column, Integer, String, JSON

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_count = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)
