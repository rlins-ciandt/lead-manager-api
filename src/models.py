from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'lead'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    resume_file = Column(BYTEA)
    status = Column(String)


