from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

DB_PATH = os.environ.get('MEDLENS_DB', 'sqlite:///medlens.db')
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False} if 'sqlite' in DB_PATH else {})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    age = Column(Integer)
    sex = Column(String(10))
    notes = Column(Text)

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    raw = Column(Text)
    patient = relationship('Patient')

class Finding(Base):
    __tablename__ = 'findings'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'))
    name = Column(String(200))
    value = Column(String(100))
    unit = Column(String(50))
    reference_range = Column(String(100))
    flag = Column(String(20))
    provenance = Column(Text)

def init_db():
    Base.metadata.create_all(engine)
