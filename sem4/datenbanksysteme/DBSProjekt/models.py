# coding: utf-8
from sqlalchemy import Column, Integer, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Article(Base):
    __tablename__ = 'articles'

    Title = Column(Text)
    DOI = Column(Text, primary_key=True)
    Theme = Column(Text)
    Year = Column(Integer)


class Author(Base):
    __tablename__ = 'authors'

    A_Key = Column(Integer, primary_key=True)
    A_Names = Column(String, nullable=False)


class Journal(Base):
    __tablename__ = 'journals'

    Rank = Column(Integer)
    Title = Column(Text, primary_key=True)
    ImpactFactor = Column(Numeric)


class Publish(Base):
    __tablename__ = 'publish'

    Title = Column(Text, primary_key=True, nullable=False)
    DOI = Column(Text, primary_key=True, nullable=False)


class Write(Base):
    __tablename__ = 'writes'

    DOI = Column(Text, primary_key=True, nullable=False)
    A_Key = Column(Integer, primary_key=True, nullable=False)
