# -*- coding: utf-8 -*-
import lxml.etree
import requests


class DouBanBook(object):
    # 书列表，根据tag 名称和offset 20
    book_list_from_tag_url = "https://book.douban.com/tag/{tag_name}?start={offset}&type=T"

    def get_one_page(self, tag_name, offset):
        """获取书籍详情页地址"""
        response = requests.get(self.book_list_from_tag_url.format(tag_name=tag_name, offset=offset))
        xpath_url = "//ul[@class='subject-list']/li/div[@class='pic']/a/@href"
        html = lxml.etree.HTML(response.content)
        book_url_list = html.xpath(xpath_url)
        return book_url_list


if __name__ == '__main__':
    spider = DouBanBook()
    url_list = spider.get_one_page("小说", 0)
    print(url_list)

