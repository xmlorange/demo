# -*- coding: utf-8 -*-
import json
from datetime import datetime

import lxml.etree
import requests
import re


class DouBanBook(object):
    # 标签列表页
    tag_list_url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-hot"
    # book info 所有字段
    book_info_details = [("作者", "author"),
                         ("出版社", "publisher"),
                         ("出品方", "producer"),
                         ("原作名", "original_title"),
                         ("译者", "translator"),
                         ("出版年", "publish_time"),
                         ("页数", "page_number"),
                         ("定价", "price"),
                         ("装帧", "pack"),
                         ("丛书", "series"),
                         ("ISBN", "isbn"),
                         ("副标题", "subtitle")]

    # 书列表，根据tag 名称和offset 20
    book_list_from_tag_url = "https://book.douban.com/tag/{tag_name}?start={offset}&type=T"

    def __init__(self, end_offset=980):
        self.end_offset = end_offset

    def get_tags(self):
        """获取tag信息"""
        response = requests.get(self.tag_list_url)
        html = lxml.etree.HTML(response.content)
        for div in html.xpath("//div[@class='article']/div[2]/div"):
            big_tag = div.xpath("./a/@name")
            small_tags = div.xpath("./table//td/a/text()")
            yield big_tag, small_tags

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

    def get_book_detail(self, book_url):
        """获取书籍详情"""
        response = requests.get(book_url)
        html = lxml.etree.HTML(response.content)

        # ret = html.xpath("//div[@class='related_info']/div[@class='indent'][1]//div[@class='intro']//text()")
        # print(ret)

        info_text_list = html.xpath("//div[@id='info']//text()")
        # 使用正则处理
        info_str = re.sub(r"\s", "", "".join(info_text_list))  # 剔除空白字符
        info_str = re.sub(r"\xa0", "", info_str)    # 剔除无用字符

        detail = dict()

        for field, field_name in self.book_info_details:
            ret = re.search("%s:(.*?):" % field, info_str + ":")

            if ret:
                # 剔除掉 '作者:[日]东野圭吾出版社' 末尾的 '出版社', 其它同理
                # value = re.sub("(作者|出版社|出品方|原作名|译者|出版年|页数|定价|装帧|丛书|ISBN|副标题)$", "", _.group(1))
                value = re.sub("(作者|出版社|出品方|原作名|译者|出版年|页数|定价|装帧|丛书|ISBN|副标题)$", "", ret.group(1))
                detail[field_name] = value
            else:
                detail[field_name] = None

        # 选取标题
        book_title = html.xpath("//div[@id='wrapper']/h1/span/text()")
        detail["title"] = book_title

        # 评分
        rating_num = html.xpath("//div[@id='interest_sectl']//strong/text()")
        detail["rating_num"] = rating_num

        # 内容简介
        book_summary = html.xpath("//div[@class='related_info']/div[@class='indent'][1]//div[@class='intro']//text()")
        detail["book_summary"] = book_summary

        # 作者简介
        author_summary = html.xpath("//div[@class='related_info']/div[@class='indent ']//div[@class='intro']//text()")
        detail["author_summary"] = author_summary

        return detail

    @staticmethod
    def clean_data(data):
        _ = data["publish_time"].split('-')
        if len(_) is 1:
            dt = datetime(int(_[0]), 1, 1)
        elif len(_) is 2:
            dt = datetime(int(_[0]), int(_[1]), 1)
        elif len(_) is 3:
            dt = datetime(int(_[0]), int(_[1]), int(_[2]))
        else:
            raise Exception("Can't trans {0} to datetime".format(data["publish_time"]))
        data["publish_time"] = dt.strftime("%Y-%m-%d")
        data["page_number"] = int(data["page_number"])
        data["price"] = float(re.search(r"\d+\.\d+", data["price"]).group())
        data["title"] = data["title"][0].strip()
        data["rating_num"] = float(data["rating_num"][0])
        data["book_summary"] = "".join([i.strip() for i in data["book_summary"]])
        data["author_summary"] = "".join([i.strip() for i in data["author_summary"]])

        return data

    @staticmethod
    def store_to_json(data, file_name):
        with open(file_name, "w") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    book = DouBanBook()

    tags_data = dict()
    for bt, st in book.get_tags():
        tags_data[bt[0]] = st

    details = book.get_book_detail('https://book.douban.com/subject/25862578/')
    new_detail = book.clean_data(details)

    book.store_to_json(tags_data, "tags.json")
    book.store_to_json(new_detail, "{0}.json".format(new_detail["title"]))
