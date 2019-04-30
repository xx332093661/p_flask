# coding: utf-8
from datetime import datetime
from taobao_test import db, app
from taobao_test.models.files import ProductFile
from taobao_test.models.product import Product
from tools import AGENTS_ALL, save_product, get_data

import random
import requests
import re
import traceback
import json


def tmgj_spider():
    product_file = ProductFile(name='天猫国际', create_date=datetime.now(), state='查询中')
    db.session.add(product_file)
    db.session.commit()

    crawl_key_word(product_file.id)

    get_data(product_file.id)

    product_file.state = '已完成'
    db.session.commit()

    return


def crawl_key_word(product_file_id):

    i = 0

    while i < 100:
        print 'iiiiiii:', i
        try:
            agent = random.choice(AGENTS_ALL)
            headers = {'User-Agent': agent}

            url = "https://s.taobao.com/search?globalbuy=1&filter_tianmao=tmall&sort=sale-desc&s=%s" % (44 * i)

            content = requests.get(url, headers=headers)

            page2(content, url, product_file_id)

        except Exception:
            app.logger.error(traceback.format_exc())
        finally:
            i += 1


def page2(content, url, product_file_id):

    body = content.text

    products_match = '"auctions":(\[.*?"risk":""\}\])'
    products = re.findall(products_match, body)

    if not products:
        return
    products = json.loads(products[0])

    for product in products:
        nid = product['nid']
        category = product['category']
        title = product['title']
        view_price = product['view_price']
        item_loc = product['item_loc']
        view_sales = product['view_sales']
        nick = product['nick']

        save_product(nid, category, title, view_price, item_loc, view_sales, nick, url, product_file_id)

