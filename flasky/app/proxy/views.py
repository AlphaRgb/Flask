from flask import jsonify, request, render_template
from lxml import etree, html
import requests

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
    url = 'https://ip.cn/'
    proxies = {
        'http': 'http://{}'.format(proxy),
        'https': 'http://{}'.format(proxy)
    }
    try:
        res = requests.get(url, proxies=proxies, verify=False).text
    except Exception as e:
        print(e)
        return '当前代理可能已经不能再使用'
    else:
        data = etree.HTML(res)
        result = data.xpath('//div[@id="result"]')[0]
        content = html.tostring(result)
        return content


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
