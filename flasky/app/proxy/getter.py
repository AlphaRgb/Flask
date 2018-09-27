#!/usr/bin/env python3
# coding=utf-8

import requests
from lxml import etree
import re
import json


class ProxyGetter(object):

    def get_html(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return etree.HTML(r.text)
        except ConnectionError:
            print('Crawling Failed', url)

    # 爬取66代理
    def crawl_daili66(self):
        url = 'http://www.66ip.cn/nmtq.php?getnum=&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip'
        html = self.get_html(url)
        if html is not None:
            try:
                ips = html.xpath('//body//text()')
                for ip in ips:
                    if ':' in ip:
                        yield ip.strip()
            except Exception as e:
                print(e)

    # 爬虫快代理
    def crawl_kuaidaili(self):
        url = 'https://www.kuaidaili.com/free/inha/'
        html = self.get_html(url)
        if html is not None:
            try:
                trs = html.xpath('//div[@id="list"]//tr')[1:]
                for tr in trs:
                    host = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    ip = ':'.join([host, port])
                    yield ip
            except Exception as e:
                pass

    # # 爬取米扑代理 (端口是图片,暂时不处理)
    # def crawl_mimvo(self):
    #     url = 'https://proxy.mimvp.com/free.php'
    #     html = self.get_html(url)
    #     if html is not None:
    #         try:
    #             ips = html.xpath('//div[@class="free-list"]//tr')[1:]
    #             for ip in ips:
    #                 if ':' in ip:
    #                     yield ip.strip()
    #         except Exception as e:
    #             print(e)


    # # 爬取西刺代理
    # def crawl_xici(self, page_count=10):
    #     start_url = 'http://www.xicidaili.com/nn/{}'
    #     urls = [start_url.format(str(page)) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         html = self.get_html(url)
    #         try:
    #             trs = html.xpath('//table[@id="ip_list"]/tr')
    #             for tr in trs[1:]:
    #                 yield ':'.join(tr.xpath('./td/text()')[0:2])
    #         except Exception as e:
    #             print(e)
    #             pass
    #
    # # 爬取360代理
    #
    # def crawl_360(self):
    #     url = 'http://www.proxy360.cn/Region/China'
    #     html = self.get_html(url)
    #     try:
    #         trs = html.xpath('//div[@class="proxylistitem"]')
    #         for tr in trs:
    #             proxy = ':'.join([tr.xpath('./div/span/text()')[0].strip(), tr.xpath('./div/span/text()')[1].strip()])
    #             yield proxy
    #     except Exception as e:
    #         print(e)
    #         pass
    #
    # # 爬取全网代理
    #
    # def crawl_quanwang(self, page_count=10):
    #     start_url = 'http://www.goubanjia.com/free/gngn/index{}.shtml'
    #     urls = [start_url.format(page) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         html = self.get_html(url)
    #         try:
    #             trs = html.xpath('//div[@id="list"]//tr')
    #             for tr in trs[1:]:
    #                 yield ''.join(tr.xpath('./td[1]//text()'))
    #         except Exception as e:
    #             print(e)
    #             pass
    #

    # 爬取无忧代理
    def crawl_wuyou(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = self.get_html(url)
        try:
            trs = html.xpath('//ul[@class="l2"]')
            for tr in trs[1:]:
                yield tr.xpath('./td/a/@href')[0]
        except Exception as e:
            print(e)
            pass

    # 爬取代理列表, 可以爬取国外代理
    def crawl_proxydocker(self):
        url = 'https://www.proxydocker.com/zh/proxylist/country/China'
        html = self.get_html(url)
        try:
            trs = html.xpath('//a/@href')
            for tr in trs:
                if ':' in tr:
                    yield tr.split('/')[-1]
        except Exception as e:
            print(e)
            pass
    #
    # # 爬取ip181代理
    #
    # def crawl_ip181(self):
    #     url = 'http://www.ip181.com/'
    #     html = self.get_html(url)
    #     try:
    #         trs = html.xpath('//tr')
    #         for tr in trs[1:]:
    #             yield ':'.join(tr.xpath('./td/text()')[0:2])
    #     except Exception as e:
    #         print(e)
    #         pass

    # 爬取代理服务器网
    def crawl_cnproxy(self):
        # cnproxy url = 'http://www.cnproxy.com/proxy1.html'
        url = 'http://proxylist.fatezero.org/proxy.list'
        res = requests.get(url)
        proxy_list = re.findall(r'{.*?}', res.text)
        for _ in proxy_list:
            origin_proxy = json.loads(_)
            proxy = ''.join([origin_proxy.get('host'), ':', str(origin_proxy.get('port'))])
            yield proxy

    def run(self):
        s = dir(self)
        crawl_funcs = []
        for _ in s:
            if 'crawl_' in _:
                crawl_funcs.append(_)
        print(crawl_funcs)
        for crawl_func in crawl_funcs:
            print(crawl_func)
            results = eval('self.' + crawl_func + '()')
            for result in results:
                yield result


if __name__ == '__main__':
    p = ProxyGetter()
    for _ in p.crawl_cnproxy():
        print(_)
