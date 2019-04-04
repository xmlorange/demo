from mongoengine import *


class Tag(Document):

    stag = StringField(required=True, max_length=31)
    btag = StringField(required=True, max_length=31)


class Book(Document):

    author = StringField(max_length=63, required=True)
    publisher = StringField(max_length=63, required=True)
    producer = StringField(max_length=63)
    original_title = StringField(max_length=63)
    translator = StringField(max_length=63)
    publish_time = DateTimeField(null=False)
    page_number = IntField(null=False)
    price = FloatField(null=False)
    pack = StringField(max_length=63)
    series = StringField(max_length=63)
    isbn = StringField(max_length=20, required=True)
    subtitle = StringField(max_length=63)
    title = StringField(max_length=63, required=True)
    rating_num = FloatField(null=False)
    book_summary = StringField(required=True)
    author_summary = StringField(required=True)

    # nosql 这些数据采取冗余存储
    small_tag = StringField(required=True, max_length=31)
    big_tag = StringField(required=True, max_length=31)

