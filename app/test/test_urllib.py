# -*- coding: utf-8 -*-

import urllib.request
import socket
import urllib.error
from urllib import request, parse
from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, build_opener

# URL = 'https://www.python.org'
# URL = 'https://wb.shbaoyuantech.com'
# URL = 'http://httpbin.org/post'
URL = 'https://wb.uat.shbaoyuantech.com/contract/update-student'
login_url = 'https://wb.uat.shbaoyuantech.com/login'


def get_html():
    response = urllib.request.urlopen(URL)
    print(response.read().decode('utf-8'))
    print(type(response))
    print(response.status)
    print(response.getheaders())
    print(response.getheader('Server'))
    print(response.getheader('Date'))


def set_timeout():
    try:
        response = urllib.request.urlopen(URL, timeout=0.01)
        print(response)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print("TIME OUT")


def send_parm():
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)',
    #     'Host': 'httpbin.org'
    # }
    dict = {
        'name': 'Germey'
    }
    data = bytes(parse.urlencode(dict), encoding='utf-8')
    # req = request.Request(url=URL, data=data, headers=headers, method='POST')
    req = request.Request(url=URL, data=data, method='POST')
    req.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64)  ')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


def login():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)',
        'Authorization': 'Bearer ',
        'Host': 'wb.uat.shbaoyuantech.com',
        'Referer': 'https://wb.uat.shbaoyuantech.com/static/'
    }
    dict = {
        'mobile': 'admin',
        'password': '123456'
    }
    data = bytes(parse.urlencode(dict), encoding='utf-8')
    req = request.Request(url=login_url, data=data, headers=headers, method='GET')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


def need_auth():
    # 登录
    login()

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)',
        'Authorization': 'Bearer OWU4NzNmYWYtNzNiMC00NDkxLWIyMDQtMGQ5OGE0N2E4ZmUw',
        'Host': 'wb.uat.shbaoyuantech.com',
        'Referer': 'https://wb.uat.shbaoyuantech.com/static/'
    }
    dict = {
        'contractId': '105161',
        'studentId': '931043',
        'contractStudentId': '1171706',
        'name': '杨璟',
        'gender': 'gender',
        'birthday': '2019-01-28',
        'mobile': '13570589622'
    }
    data = bytes(parse.urlencode(dict), encoding='utf-8')
    req = request.Request(url=URL, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


def test():
    username = '13916212570'
    password = '123456'
    p = HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, login_url, username, password)
    auth_handler = HTTPBasicAuthHandler(p)
    opener = build_opener(auth_handler)
    try:
        result = opener.open(URL)
        html = result.read().decode('utf-8')
        print(html)
    except urllib.error.URLError as e:
        print(e.reason)


if __name__ == '__main__':
    # set_timeout()
    # get_html()
    # need_auth()
    login()
    # test()
