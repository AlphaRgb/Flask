#!/usr/bin/env python3
# coding=utf-8

import re
import logging
import urllib3

import requests
from lxml import etree

from .chinese_digit import getResultForDigit

urllib3.disable_warnings()


def get_novel(name):
    try:
        url = 'https://sou.xanbhx.com/search?siteid=qula&q={}'.format(name)
        res = requests.get(url)
        if len(res.text):
            html = etree.HTML(res.text)
            books = html.xpath('//div[@class="search-list"]/ul/li')[1:]
            for book in books:
                book_name = book.xpath('./span[2]/a/text()')[0].strip()
                if name == book_name:
                    novel_url = book.xpath('./span[2]/a/@href')[0]
                    return novel_url
        else:
            url = 'https://www.qu.la/SearchBook.php?keyword={}'.format(name)
            res = requests.get(url)
            html = etree.HTML(res.text)
            books = html.xpath('//div[@class="novelslist2"]/ul/li')[1:]
            for book in books:
                book_name = book.xpath('./span[2]/a/text()')[0].strip()
                if name == book_name:
                    novel_url = 'https://www.qu.la' + book.xpath('./span[2]/a/@href')[0]
                    return novel_url
    except Exception as e:
        print(e)


def get_novel_info(novel_url):
    if novel_url is not None:
        res = requests.get(novel_url)
        html = etree.HTML(res.text)
        name = html.xpath('//h1/text()')[0]
        author = html.xpath('//div[@id="info"]/p[1]/text()')[0].split('：')[1]
        return name, author


def get_novel_chapters(url):
    logging.info('get url content {}'.format(url))
    res = requests.get(url)
    html = etree.HTML(res.text)
    # results = html.xpath('//div[@id="list"]/dl/dd/a[contains(text(), "章")]')[:10]
    results = html.xpath('//div[@id="list"]/dl/dd/a')[:10]
    for result in results:
        chapter = result.xpath('./text()')[0]
        chapter_url = url + result.xpath('./@href')[0]
        yield chapter, chapter_url


def get_chapter_content(url):
    res = requests.get(url)
    html = etree.HTML(res.text)
    # content = ''.join(html.xpath('//div[@id="content"]//text()')[:-3])
    content = '<br>'.join(html.xpath('//div[@id="content"]//text()')[:-3])
    index = content.find('Ps')
    if index != -1:
        content = content[:index]
    # content = re.sub(r'Ps.*', '', content)
    return content.strip()


if __name__ == '__main__':
    novel_url = get_novel('太初')
    print(novel_url)
    name, author = get_novel_info(novel_url)
    print(name, author)
    chapters = get_novel_chapters(novel_url)
    for _ in chapters:
        title, chapter_url = _
        try:
            end = title.find('章')
            chapter = re.findall(r'\d{1,}', title)[0] if re.findall(r'\d{1,}', title) else getResultForDigit(''.join(title[1:end]))
        except Exception as e:
            print(e)
        else:
        # chapter = int(title.split()[0][1:-1]) if re.findall(r'\d{1,}', title.split()[0][1:-1]) else getResultForDigit(title.split()[0][1:-1])
            print(chapter, title, chapter_url)
            content = get_chapter_content(chapter_url)
            print(content)
