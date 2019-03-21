# -*- coding: utf-8 -*-
import re

import lxml.etree
import requests


class DouBanBook(object):
    # book info 所有字段
    book_info_details = ["作者", "出版社", "出品方", "原作名", "译者", "出版年", "页数", "定价", "装帧", "丛书", "ISBN", "副标题"]

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

        print(info_str)

        for field in self.book_info_details:
            ret = re.search("%s:(.*?):" % field, info_str + ":")
            if ret:
                # 剔除掉 '作者:[日]东野圭吾出版社' 末尾的 '出版社', 其它同理
                # value = re.sub("(作者|出版社|出品方|原作名|译者|出版年|页数|定价|装帧|丛书|ISBN|副标题)$", "", _.group(1))
                value = re.sub("(%s)$" % ("|".join(self.book_info_details)), "", ret.group(1))
                print(field, ":", value)
            else:
                print(field, ":", None)

        # 选取标题
        book_title = html.xpath("//div[@id='wrapper']/h1/span/text()")
        print("书名", book_title)

        # 评分
        rating_num = html.xpath("//div[@id='interest_sectl']//strong/text()")
        print("评分:", rating_num)

        # 内容简介
        book_summary = html.xpath("//div[@class='related_info']/div[@class='indent'][1]//div[@class='intro']//text()")
        print(book_summary)

        # 作者简介
        author_summary = html.xpath("//div[@class='related_info']/div[@class='indent ']//div[@class='intro']//text()")
        print(author_summary)


if __name__ == '__main__':
    book = DouBanBook()
    book.get_book_detail('https://book.douban.com/subject/25862578/')
