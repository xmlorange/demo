# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""


class Config:
    SECRET_KEY = b'\xd3%\x0c6\xf9OMP\xd8f\xec\x97\x00\xae-\xf9\xb1\x1d\x03\xbdt\xaf\x07\x07'
    SQLALCHEMY_BINDS = {
        "cm": "mysql+pymysql://root:Hutong_0328@120.26.197.19:3306/common_prod?charset=utf8",
        "bs": "mysql+pymysql://root:Hutong_0328@120.26.197.19:3306/business_prod?charset=utf8",
        "qb": "mysql+pymysql://dubbo:dubbo%40admin@121.41.50.233:31306/cnhutong_content?charset=utf8"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    EMAIL_USERNAME = "auto_sender@shbaoyuantech.com"
    EMAIL_SENDER_NAME = '自动发送'
    EMAIL_PASSWORD = 'Sender365'
    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465
    TO_EMAIL = ['auto_sender@shbaoyuantech.com', ' moxiaolong@cnhutong.com']


config = Config
