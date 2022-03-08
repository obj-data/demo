# -*- codeing = utf -*-
# @Time : 2021/11/28 21:50
# @Author : 陈迪曙
# @File : test1.py
# @software : PyCharm
import re

import bs4
import requests
import os
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError
from tqdm import tqdm
import time


# 根据书名进行搜索
def book_names(domain, bookname):
    book_url = domain + '/search.php?q=' + bookname
    res = requests.get(book_url).text
    link_list = []
    title_list = []
    link = re.findall(re.compile('<a cpos="title" href="(.*)" title="(.*)" class=.*'), res)
    for name in link:
        if name[1] == bookname:
            book = domain + name[0]
            first_html = requests.get(book).text
            pages = re.findall(re.compile('<option value="(.*?)".*'), first_html)
            for i in pages:
                i = domain + i
                res = requests.get(i).text
                chapter = re.findall(re.compile('href="(.*?\.html)">(第.*.*)</a>'), res)[1::]
                if not chapter:
                    chapter =  chapter = re.findall(re.compile('href="(.*?\.html)">(.*)</a>'), res)[1::]
                for a in chapter:
                    title_list.append(a[1])
                    link_list.append(domain + a[0])
            return link_list, title_list

    else:
        print('该网站可能没有此书，请检查后再进行下载')
        exit()


def gettext(link):
    res = requests.get(link).text
    res = re.sub(re.compile('&nbsp;'), '', res)
    title = re.findall(re.compile('<div class=".*" id="n.*">(.*)</div>'), res)
    # body = re.findall(re.compile('<div id="nr1">(.*?)</div>.*'), res)
    body = re.findall(re.compile('<div id="nr1">(.*)<br>'), res)
    try:
        data = title[0] + '\n\n' + body[0]
        data = re.sub(re.compile('<br><br>'), '\n\n', data)
        data += '\n\n'
        return data
    except:
        soup = BeautifulSoup(res, 'html.parser')
        body = soup.select("#nr1")
        header = re.findall('^.*', str(body))
        # tail = re.findall(re.compile('.*$'), str(body))
        tail = re.findall(re.compile('.*&lt;!.*'), str(body))
        body = re.findall('.*', str(body))
        text = ''
        for t in body:
            if t == tail[0]:
                break
            elif t != header[0]:
                text += t
        data = title[0] + '\n\n' + text + '\n\n'
        data = re.sub(re.compile('<br/><br/>'), '\n\n', data)
        data += '\n\n\n\n————————————分割线——————————————'
        return data


def add_book(start, links, bookname, titles):
    n = 1
    new_links = []
    for i in titles:
        if start in i:
            new_links = links[n::]
        else:
            n += 1
    writebook(new_links, bookname)


def writebook(links, name):
    print('{}一共有{}章，开始下载：'.format(name, len(links) + 1))
    for i in tqdm(range(0, len(links) + 1)):
        try:

            data = gettext(links[i])
            time.sleep(0.01)
            with open('{}.txt'.format('./books/' + name), 'a', encoding='utf-8') as f:
                f.write('\n\n\n' + data)
        except IndexError:
            print('下载结束————>——————————>————————————>')


def testfile(bookname, url):
    result = os.walk('../')
    pathThat = {}
    for root, dirs, files in result:
        pathThat['{}'.format(root)] = files
    if './books' not in pathThat:
        print(pathThat)
        os.mkdir('../books')
    all_links = book_names(domain=url, bookname=name)
    links, title_list = all_links

    if links is not None:
        if bookname + '.txt' in pathThat['./books']:
            judge = input('当前文件夹存在同名文件（小说），是否覆盖(不覆盖则视为更新至最新章节):(y/n)')
            if judge == 'y':
                with open('{}.txt'.format('./books/' + name), 'w') as f:
                    f.write('')
                writebook(links, name=bookname)
            elif judge == 'n':
                start_chapter = input('更新的起点章节（如：第一章）:')
                add_book(start=start_chapter, links=links, bookname=bookname, titles=title_list)
        else:
            writebook(links, name=bookname)
    else:
        return None
    return title_list


if __name__ == '__main__':
    url = 'https://m.biquyue.com/'
    name = input('请输入书名：')
    # name = '紫川'
    try:
        last_table = testfile(name, url)
    except ProxyError as e:
        print('请关闭代理！')
        log_data = {'Time': time.strftime('%Y-%m-%d %H:%M:%S\t%A'), 'Error': e}
        open('../books/test.log', 'a').write(str(log_data) + '\n')
