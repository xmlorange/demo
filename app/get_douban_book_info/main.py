# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker

from app.get_douban_book_info.get_douban_book_information import DouBanBook
from app.get_douban_book_info.models import engine, BigTag, SmallTag, Book, BookToTag


Session = sessionmaker(bind=engine)

spider = DouBanBook(20)


def store_tag_data():
    session = Session()
    for bt, st in spider.get_tags():
        if not session.query(BigTag).filter(BigTag.btag == bt[0]).first():
            big_tag = BigTag(btag=bt[0])
            session.add(big_tag)
            session.commit()
            for t in st:
                small_tag = SmallTag(stag=t, btag_id=big_tag.id)
                session.add(small_tag)
    session.commit()
    session.close()


def store_detail_data():
    session = Session()
    for t in session.query(SmallTag).all():
        for page, url_list in spider.get_all_pages(t.stag):
            for book_url in url_list:
                detail = spider.get_book_detail(book_url)
                detail = spider.clean_data(detail)
                book = Book(**detail)
                session.add(book)
            break
        break   # 为了不翻页加上break 完整的翻页的话需要去掉这两个break
    session.commit()
    session.close()


if __name__ == '__main__':
    store_tag_data()
    store_detail_data()
