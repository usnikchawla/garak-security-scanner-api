from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model_id = Column(String, nullable=False)

class Config(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    probes = Column(JSON, nullable=False)
    detectors = Column(JSON, nullable=False)

class Scan(Base):
    __tablename__ = 'scans'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, nullable=False)
    config_id = Column(Integer, nullable=False)
    prompt = Column(String, nullable=False)
    status = Column(String, nullable=False)
    results = Column(JSON)

Base.metadata.create_all(engine)
