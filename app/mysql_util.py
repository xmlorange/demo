# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""
from functools import partial

from app import db, app, config


class Execute:
    def __init__(self):
        for db_name in config.SQLALCHEMY_BINDS.keys():
            setattr(self, "{}".format(db_name), partial(self._execute, db_name=db_name))

    @classmethod
    def _execute(cls, sql, db_name):
        return db.session.execute(sql, bind=db.get_engine(app=app, bind=db_name)).fetchall()


ex = Execute()
