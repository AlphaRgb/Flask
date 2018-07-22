#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from lxml import etree

url = 'https://geoiptool.com/zh/'
res = requests.get(url, verify=False).text

html_data = etree.HTML(res)
result = html_data.xpath('//div[contains(@class, "sidebar-data")]')[0]
print(etree.tounicode(result))
