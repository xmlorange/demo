# -*- coding: utf-8 -*-

from mongoengine import *

from app.mongo_orm.models import Tag, Book
from app.mongo_orm.spider import DouBanBook


spider = DouBanBook()
connect('test_db', host='localhost')


def run():
    for bt, st in spider.get_tags():
        if not Tag.objects.filter(btag=bt[0]).all():
            for t in st:
                tag = Tag(btag=bt[0], stag=t)
                tag.save()

    for t in Tag.objects.all():
        for page, url_list in spider.get_all_pages(t.stag):
            for book_url in url_list:
                detail = spider.get_book_detail(book_url)
                detail = spider.clean_data(detail)  # 清洗数据
                detail["small_tag"] = t.stag
                detail["big_tag"] = t.btag
                book = Book(**detail)
                book.save()
            break
        break


if __name__ == '__main__':
    run()
