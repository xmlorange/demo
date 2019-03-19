# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""
import datetime


class StaticParam:
    TIME_POINT = "2019-01-12"


class DateParam:
    @property
    def start(self):
        today = datetime.datetime.now()
        return (today - datetime.timedelta(days=today.weekday() + 7)).strftime("%Y-%m-%d")

    @property
    def end(self):
        today = datetime.datetime.now()
        return (today - datetime.timedelta(days=today.weekday())).strftime("%Y-%m-%d")


STORE_MAP = {29: "七宝", 140: "闵行星宝", 141: "青浦青湖"}

NEW_STORE_MAP = {140: "闵行星宝", 141: "青浦青湖"}

date_param = DateParam()
