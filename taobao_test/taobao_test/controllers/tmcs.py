# coding: utf-8
from datetime import datetime
from taobao_test import db, app
from taobao_test.models.files import ProductFile
from tools import AGENTS_ALL, save_product, get_data
from bs4 import BeautifulSoup

import random
import requests
import traceback


def tmcs_spider():
    product_file = ProductFile(name='天猫超市', create_date=datetime.now(), state='查询中')
    db.session.add(product_file)
    db.session.commit()

    crawl_key_word(product_file.id)

    get_data(product_file.id)

    product_file.state = '已完成'
    db.session.commit()

    return


def crawl_key_word(product_file_id):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'zh-CN,zh;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'sm4=500100; mbk=69fc49ffcdfba424; l=AsvLF15hcSrANNLLhzpOjRC-22W0jt-C; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTcCimdCuMSZg%3D%3D&lng=zh_CN&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false&cookie21=Vq8l%2BKCLjA%2Bl&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0; uc3=sg2=BqeJ4iE93swDom%2FWTyHg0g%2Bt51nDWeRP5it0%2F%2FaElDI%3D&nk2=G5gua0ue5bjBRJE%3D&id2=VAieYnx3LghA&vt3=F8dBzWffmK%2BrmIpSJ4I%3D&lg2=URm48syIIVrSKA%3D%3D; tracknick=xx332093661; _l_g_=Ug%3D%3D; unb=799762535; lgc=xx332093661; cookie1=ACu2apMNwpW2BPyuKODI102NHN%2FfKm1efGVOiEqLxN0%3D; login=true; cookie17=VAieYnx3LghA; cookie2=5cd8beb1f3ac2efbd523e9df1f285d8d; _nk_=xx332093661; uss=Vv6cgfT9iuKUW2y2VjIGJJ%2BPyzfgEXb%2FEiCrPu7S1I9GhjBT0nYfPeh%2Fnw%3D%3D; sg=158; t=da07982c2d81e0e95e4dd41d4dc20d10; _tb_token_=e43eebd569a7e; cna=rfD+EcYaUmsCAT26hMJlAlyZ; _m_h5_tk=09cb707dc4aa786c34d9b3a6908417ef_1505285351672; _m_h5_tk_enc=094f5c0c6aa028992b5dd7d3f22e7c7b; isg=AomJ4XvGNICd6shJ8qq2zuEZmLVPxmMAJkcLXiv-B3CvcqmEcyaN2HeswMmv',
        'referer': 'https://login.tmall.com/?redirectURL=https%3A%2F%2Flist.tmall.com%2Fsearch_product.htm%3Fspm%3Da3204.7933263.0.0.e859a79ubxfk%26cat%3D50514008%26s%3D120%26q%3D%25E5%25A4%25A9%25E7%258C%25AB%25E8%25B6%2585%25E5%25B8%2582%26sort%3Dwd%26style%3Dg%26user_id%3D725677994%26from%3Dchaoshi.index.pc_1_placeholder%26active%3D1%26industryCatId%3D50514008%26smAreaId%3D500100%26smToken%3Dd3d6caea2ed042a8be68ba4a0c466f6c%26smSign%3Dr5KnABGqUkTMvLuk2EvZdQ%253D%253D',
        'upgrade-insecure-requests': '1',
    }

    i = 0

    while i < 100:
        print 'iiiiiii:', i
        try:
            agent = random.choice(AGENTS_ALL)
            headers.update({'User-Agent': agent})

            url = "https://list.tmall.com/search_product.htm?spm=a3204.7933263.0.0.e859a79ubxfk&cat=50514008&s=%s&q=天猫超市&sort=wd&style=g&user_id=725677994&from=chaoshi.index.pc_1_placeholder&active=1&industryCatId=50514008&smAreaId=500100#J_Filter" % (40 * i)
            # url = 'https://list.tmall.com/search_product.htm?q=天猫超市&sort=wd&user_id=725677994&s=%s' % (40 * i)
            content = requests.get(url, headers=headers)
            print content.url
            page2(content, url, product_file_id)

        except Exception:
            app.logger.error(traceback.format_exc())
            print traceback.format_exc()
        finally:
            i += 1


def page2(content, url, product_file_id):

    soup = BeautifulSoup(content.text, 'lxml')
    for li in soup.find_all('li', class_='product'):
        nid = li['data-itemid']
        category = ''
        title = li.div.h3.a.text
        view_price = li.find('div', class_='item-price').span.strong.text
        item_loc = ''
        view_sales = '%s%s' % (li.find('div', class_='item-sum').span.text, li.find('div', class_='item-sum').strong.text)
        nick = ''
        url = None

        save_product(nid, category, title, view_price, item_loc, view_sales, nick, url, product_file_id)

