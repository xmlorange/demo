# -*- coding: utf-8 -*-

from urllib.parse import quote


class Config:
    SECRET_KEY = b'\xd3%\x0c6\xf9OMP\xd8f\xec\x97\x00\xae-\xf9\xb1\x1d\x03\xbdt\xaf\x07\x07'
    SQLALCHEMY_BINDS = {
        "cm": "mysql+pymysql://root:{0}@118.31.115.234:3306/staff_uat_2?charset=utf8".format(quote('Bytech123')),
        "bs": "mysql+pymysql://root:{0}@118.31.115.234:3306/business_uat_2?charset=utf8".format(quote('Bytech123')),
        "qb": "mysql+pymysql://dubbo:dubbo%40admin@121.41.50.233:31306/cnhutong_content?charset=utf8",
        "cs": "mysql+pymysql://hutong:Hutong_1226@cshutong.mysql.rds.aliyuncs.com:3306/hutong_20161010?charset=utf8"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    EMAIL_USERNAME = "auto_sender@shbaoyuantech.com"
    EMAIL_SENDER_NAME = '自动发送'
    EMAIL_PASSWORD = 'Sender365'
    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465
    TO_EMAIL = ['auto_sender@shbaoyuantech.com', ' moxiaolong@cnhutong.com']


config = Config
