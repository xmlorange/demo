# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
