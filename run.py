# -*- coding: utf-8 -*-
"""
    author: Q.Y.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=9020, host="127.0.0.1")
