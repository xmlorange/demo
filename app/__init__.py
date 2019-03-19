# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""

from app.extend import app, db
from app.config import config
from app import view


def create_app():
    app.config.from_object(config)

    reg_app(app)

    @app.route("/test")
    def test():
        return "Test Success"

    return app


def reg_app(app_obj):
    db.init_app(app_obj)
