from flask import jsonify, request, render_template
from lxml import etree, html
import requests
import re

from . import proxy
from .ipManager import ProxyManager


api_list = {
    'get': 'get an usable proxy',
    # 'refresh': 'refresh proxy pool',
    'get_all': 'get all proxy from proxy pool',
    # 'delete?proxy=127.0.0.1:8080': 'delete an unable proxy'
}


@proxy.route('/proxy/')
def index():
    return jsonify(api_list)


@proxy.route('/proxy/get/')
def get():
    proxy = ProxyManager().get()
    if proxy:
        return render_template('proxy.html', proxy=proxy)
    else:
        return 'no proxy!'


@proxy.route('/proxy/check/<proxy>')
def check(proxy):
    # url = 'https://ip.cn/' 
    # url = 'https://httpbin.org/ip'
    url = 'https://geoiptool.com/zh/'
    proxies = {
        'http': 'http://{}'.format(proxy),
        'https': 'http://{}'.format(proxy)
    }
    try:
        res = requests.get(url, proxies=proxies, verify=False).text
        data = etree.HTML(res)
    except Exception as e:
        print(e)
        return '当前代理已经失效'
    else:
        if url == 'https://ip.cn/':
            result = data.xpath('//div[@id="result"]')[0]
            content = html.tostring(result)
            return content
        elif (url == 'https://geoiptool.com/zh/' and data):
            content = data.xpath('//div[contains(@class, "sidebar-data")]')[0] if data.xpath('//div[contains(@class, "sidebar-data")]') else None
            if content is None:
                return '当前代理已经失效'
            content = etree.tounicode(content)
            content = re.sub(r'<img.*?>', '', content)
            content = re.sub(r'hidden-xs hidden-sm', '', content)
            return content
        else:
            return '当前代理已经失效'


@proxy.route('/proxy/get_all/')
def getAll():
    proxies = ProxyManager().getAll()
    if proxies:
        return jsonify(list(proxies))
    else:
        return 'no proxy!'


@proxy.route('/proxy/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@proxy.route('/proxy/get_status/')
def get_status():
    status = ProxyManager().get_status()
    return jsonify(status)
