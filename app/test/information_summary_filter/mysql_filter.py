# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from app.test.information_summary_filter import BaseFilter

Base = declarative_base()


# class Filter(Base):
#     __tablename__ = 'filter'
#
#     id = Column(Integer, primary_key=True)
#     hash_value = Column(String(40), index=True, unique=True)
#

class MySqlFilter(BaseFilter):
    """基于mysql的去重判断依据存储"""

    def __init__(self, *args, **kwargs):
        # class Filter(Base):
        #     __tablename__ = kwargs["mysql_table_name"]
        #
        #     id = Column(Integer, primary_key=True)
        #     hash_value = Column(String(40), index=True, unique=True)

        # 利用type()创建类 x需要三个参数
        filter_class = type("Filter", (Base,), dict(
            __tablename__=kwargs["mysql_table_name"],
            id=Column(Integer, primary_key=True),
            hash_value=Column(String(40), index=True, unique=True)))
        self.table = filter_class
        BaseFilter.__init__(self, *args, **kwargs)

    def _get_storage(self):
        """返回一个mysql连接对象 (sqlalchemy 的数据库连接对象)"""
        engine = create_engine(self.mysql_url, echo=False, convert_unicode=True)
        Base.metadata.create_all(engine)    # 创建表 如果有忽略
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        return session

    def _save(self, hash_value):
        session = self._get_storage()
        filter_value = self.table(hash_value=hash_value)
        session.add(filter_value)
        session.commit()
        session.close()

    def _is_exists(self, hash_value):
        """判断mysql对应的无序集合中是否有对应的数据"""
        session = self._get_storage()
        ret = session.query(self.table).filter(self.table.hash_value == hash_value).first()
        session.close()
        if ret is None:
            return False
        return True

