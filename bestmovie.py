#!/usr/bin/python
#coding:utf-8
from multiprocessing import Pool, Manager
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
import re

def useweb2(code):
    '''
    使用https://btso.pw/search/来查找番号
    :param code:
    :return:
    '''
    search_url2 = 'https://btso.pw/search/'
    headers = {
        "Content-Type":"application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
    }
    print search_url2 +code
    r1 = requests.get(search_url2+code, headers=headers)
    content1  = r1.text
    soup1 = BeautifulSoup(content1, 'html.parser')
    url_1 = soup1.find('a', href=re.compile('/detail/hash/'))['href']
    print code +"===="+url_1
    r2 = requests.get(url_1, headers=headers)
    content2 = r2.text
    soup2 = BeautifulSoup(content2, 'html.parser')
    magnet = soup2.find('textarea','magnet-link')
    if magnet:
        return magnet.text
    return ''

def DealCookies(cookie):
    cookies = {}
    for line in cookie.split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    return cookies


def GUrl(starturl):
    '''
    生成URL
    '''
    urls = []
    urls.append(starturl)
    for i in range(2,26):
        u = 'http://www.javlibrary.com/cn/vl_bestrated.php?&mode=2&page='+str(i)
        urls.append(u)
    return urls

def GetAVcode():
    '''
    从URL中获得每一页的AV code
    '''
    codelist = []
    starturl = 'http://www.javlibrary.com/cn/vl_bestrated.php?&mode=2&page='
    urls = GUrl(starturl)
    for url in urls:
        proxies = {
            'http': '127.0.0.1:18080',
            'https': '127.0.0.1:18080'
        }
        headers = {
            "Content-Type":"application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "accept-encoding":"gzip, deflate",
            "cache-control":"no-cache",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
        }
        cookie = '__cfduid=dbe9fd9b0dda128edfbd389939cc637401530945651; over18=18; __atuvc=14%7C45; timezone=-480; cf_clearance=bc9abaf5c8256fb9985cee8b8f181022c41c300c-1541589346-3600-150'
        cookies = DealCookies(cookie)
        r = requests.get(url, proxies=proxies, cookies=cookies,headers=headers)
        content= r.text
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        # 找class为id的div
        codes = soup.find_all('div', 'id')
        for code in codes:
            codelist.append(code.text)
            print('Get====='+code.text)
    return codelist

def write(code,con):
    file_path = './study_movie.txt'
    with open(file_path, 'a+') as f:
        f.write(code+'\n'+con+'\n\n')

def GetAVmagnet(code):
    '''
    通过AV code从磁力搜索引擎上获得磁力链，其中一个获得不到结果，就使用第二个
    '''
    print code 
    magnet = useweb2(code)
    if magnet:
        print magnet
        write(code, magnet)
    print(code + '=====over')


if __name__ == '__main__':
    codelist = GetAVcode()
    cpus = multiprocessing.cpu_count()
    p = Pool(cpus)
    for code in codelist:
        p.apply_async(GetAVmagnet, args=(code,))
    p.close()
    p.join()
