# -*- coding: utf-8 -*-

import lxml.etree
import requests


class DouBanBook(object):

    def __init__(self, end_offset=980):
        # 偏移量超过980 很有可能获取不到数据
        self.end_offset = end_offset

    # 书列表，根据tag 名称和offset 20
    book_list_from_tag_url = "https://book.douban.com/tag/{tag_name}?start={offset}&type=T"

    def get_one_page(self, tag_name, offset):
        """获取书籍详情页地址"""
        response = requests.get(self.book_list_from_tag_url.format(tag_name=tag_name, offset=offset))
        xpath_url = "//ul[@class='subject-list']/li/div[@class='pic']/a/@href"
        html = lxml.etree.HTML(response.content)
        book_url_list = html.xpath(xpath_url)

        # 判断是否还有下一页
        next_page = html.xpath("//span[@class='next']/a/@href")

        # 如果有下一页 就递归
        if next_page and offset < self.end_offset:
            return True, book_url_list
        else:
            return False, book_url_list

    def get_all_pages(self, tag_name, offset=0):
        """翻页"""
        # 最后一个判断条件 1 判断页面是否有下一页  2 判断offset是否超过 1000 (豆瓣50页取不到数据)
        have_next, book_url_list = self.get_one_page(tag_name, offset)
        yield int((offset / 20) + 1), book_url_list
        if have_next:  # 如果有下一页,递归执行
            yield from self.get_all_pages(tag_name, offset + 20)


if __name__ == '__main__':
    # spider = DouBanBook()
    # for page, url_list in spider.get_all_pages("UCD"):
    #     print(page, url_list)

    spider = DouBanBook(80)
    for page, url_list in spider.get_all_pages("小说"):
        print(page, url_list)
