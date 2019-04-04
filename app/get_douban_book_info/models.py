# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, Index
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:Bytech123@118.31.115.234:3306/business_uat_2?charset=utf8")

Base = declarative_base()


class BigTag(Base):
    __tablename__ = 'big_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    btag = Column(String(31), unique=True, nullable=False)

    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8"  # 表的编码格式
    }


# 一对多
class SmallTag(Base):
    __tablename__ = 'small_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stag = Column(String(31), unique=True, nullable=False)
    btag_id = Column(Integer, ForeignKey("big_tag.id"))

    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8"  # 表的编码格式
    }


class Book(Base):
    __tablename__ = 'book'

    author = Column(String(63), nullable=False)
    publisher = Column(String(63), nullable=False)
    producer = Column(String(63))
    original_title = Column(String(63))
    translator = Column(String(63))
    publish_time = Column(DateTime, nullable=False)
    page_number = Column(Integer)
    price = Column(Float, nullable=False)
    pack = Column(String(63))
    series = Column(String(63))
    isbn = Column(String(63), primary_key=True)
    subtitle = Column(String(63))
    title = Column(String(63), nullable=False)
    rating_num = Column(Float, nullable=False)
    book_summary = Column(Text, nullable=False)
    author_summary = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('title', 'author', name='uix_title_author'),   # 联合约束
        Index('title', 'author', 'publisher'),  # 索引
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8"},
    )


# 多对多
class BookToTag(Base):
    __tablename__ = 'booktotag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String(20), ForeignKey("book.isbn"))
    stag_id = Column(Integer, ForeignKey("small_tag.id"))

    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8"  # 表的编码格式
    }


def create_all_tables():
    # 创建所有表
    Base.metadata.create_all(engine)


# def drop_all_tables():
#     Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_all_tables()
