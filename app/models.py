from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from .database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    bank_account = Column(String)
    ifsc = Column(String)

    books = relationship("Book", back_populates="author")
    withdrawals = relationship("Withdrawal", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    royalty_per_sale = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
    sales = relationship("Sale", back_populates="book")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    sale_date = Column(Date)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="sales")


class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    created_at = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="withdrawals")
