from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, \
    String, TIMESTAMP, Float
from flask import g
from utils import timestamp_to_date

DeclBase = declarative_base()


class Base(DeclBase):
    def save(self):
        g.db.add(self)
        g.db.commit()
        return self.id

    def delete(self):
        self_id = self.id
        g.db.delete(self)
        g.db.commit()
        return self_id

    @classmethod
    def query_by_name(cls, name):
        return g.db.query(cls).filter_by(name=name).first()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(collation='utf8'),
                  nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Author object %s>' % self.name


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String(collation='utf8'),
                  nullable=False, unique=True)
    publish_date = Column(TIMESTAMP, nullable=False)
    price = Column(Float, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    author = relationship('Author', back_populates='books')

    def __init__(self, name=None, publish_date=None, price=None,
                 author=None):
        self.name = name
        self.publish_date = publish_date
        self.price = price
        self.author = author

    def __repr__(self):
        return '<Book object %s>' % self.name

    def update_price(self, new_price):
        self.price = new_price
        return self.save()

    def book_to_dict(self):
        return {'id': self.id, 'name': self.name,
                'published': timestamp_to_date(self.publish_date),
                'price': self.price,
                'author': self.author.name}
