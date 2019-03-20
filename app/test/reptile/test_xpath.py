# -*- coding: utf-8 -*-
import lxml.etree
from bs4 import BeautifulSoup


def test_html():
    html_data = """<meta charset="utf-8">
                    <title>Hello World</title>
                    <div>Hello World</div>
                """
    parser = lxml.etree.HTMLParser()
    root = lxml.etree.fromstring(html_data, parser)
    print(root.xpath(".//*"))
    # print(lxml.etree.tostring(root))


def test_bs4():
    html_data = """<meta charset="utf-8">
                        <title>Hello World</title>
                        <div id="hello">Hello World</div>
                    """
    soup = BeautifulSoup(html_data, "lxml")
    print(soup.find("p", id="hello").string())


if __name__ == '__main__':
    # test_html()
    test_bs4()
