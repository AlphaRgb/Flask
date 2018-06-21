#!/usr/bin/env python3
# coding=utf-8

import re

import requests
from lxml import etree

from chinese_digit import getResultForDigit


def get_novel(name):
    url = 'https://www.qu.la/SearchBook.php?keyword={}'.format(name)
    res = requests.get(url, verify=False)
    html = etree.HTML(res.text)
    novel_url = html.xpath('//div[@id="main"]//a/@href')[0]
    return 'https://www.qu.la' + novel_url


def get_novel_info(novel_url):
    res = requests.get(novel_url, verify=False)
    html = etree.HTML(res.text)
    name = html.xpath('//h1/text()')[0]
    author = html.xpath('//div[@id="info"]/p[1]/text()')[0].split('：')[1]
    return name, author


def get_novel_chapters(url):
    res = requests.get(url, verify=False)
    html = etree.HTML(res.text)
    results = html.xpath('//div[@id="list"]/dl/dd/a[contains(text(), "章")]')[:10]
    for result in results:
        chapter = result.xpath('./text()')[0]
        chapter_url = url + result.xpath('./@href')[0]
        yield chapter, chapter_url


def get_chapter_content(url):
    res = requests.get(url, verify=False)
    html = etree.HTML(res.text)
    content = ''.join(html.xpath('//div[@id="content"]//text()')[:-3])
    return content


if __name__ == '__main__':
    novel_url = get_novel('一念永恒')
    print(novel_url)
    chapters = get_novel_chapters(novel_url)
    for _ in chapters:
        title, chapter_url = _
        chapter = int(title.split()[0][1:-1]) if re.findall(r'\d{1,}', title.split()[0][1:-1]) else getResultForDigit(title.split()[0][1:-1])
        print(chapter, title, chapter_url)
        content = get_chapter_content(chapter_url)
        print(content)
