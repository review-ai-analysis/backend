from sqlalchemy import Column, Integer, Text, VARCHAR, ForeignKey, create_engine, Float, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship


engine = create_engine("postgresql://darkfox:11cana11@database:5432/darkfox")

Base = declarative_base(bind=engine)


class Reviews(Base):
    __tablename__ = "reviews"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    publication_date = Column(DateTime)
    review = Column(Text)
    rating = Column(Float)
    username = Column(VARCHAR)
    bank = Column(VARCHAR)
    url = Column(VARCHAR)
    address = Column(VARCHAR)
    source = Column(VARCHAR)
    category_name = Column(VARCHAR)
    category_percent = Column(Float)
    custom_categories = Column(VARCHAR)
