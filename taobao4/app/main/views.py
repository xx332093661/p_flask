# -*-coding: utf-8-*-

from flask import render_template, flash, current_app, request, make_response
from . import main
from .. import documents
from forms import UploadForm
from ..models import ProductFile, Product
from datetime import datetime
from app import db
from bs4 import BeautifulSoup


import logging
import traceback
import threading
import os
import xlrd
import random
import re
import jieba
import requests
import tablib
import json

_logger = logging.getLogger(__name__)

AGENTS_ALL = [
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)"]


@main.route('/', methods=['GET', 'POST'])
@main.route('/upload_file', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if form.validate_on_submit():
        filename = documents.save(form.document.data)
        origin = form.origin.data
        print 'origin:', origin
        # file_url = documents.url(filename)
        try:
            # 开启线程
            app = current_app._get_current_object()
            t = threading.Thread(target=taobao_spider, args=([app, filename, origin]))
            t.setDaemon(True)
            t.start()
            flash(u'采集数据需要一定时间，请稍后查看', 'info')
            return render_template('index.html', form=form)
        except Exception:
            return traceback.format_exc()

    return render_template('index.html', form=form)


@main.route('/get_file_list', methods=['GET', 'POST'])
def get_file_list():

    product_files = ProductFile.query.order_by(db.desc('id')).all()
    datas = []
    for product_file in product_files:
        datas.append({
            'id': product_file.id,
            'name': product_file.name,
            'create_date': product_file.create_date,
            'state': product_file.state
        })

    return render_template('files.html', datas=datas)


@main.route('/get_datas/<int:product_file_id>')
def get_datas(product_file_id=None):
    datas = get_data(product_file_id)
    return render_template('data.html', datas=datas)


@main.route('/export_excel', methods=['POST'])
def export_excel():
    if request.method == 'POST':
        headers = (u"关键字", u"产品名称", u"店铺", u"地址", u'包装数量', u'价格', u'单价', u'销售量')

        key_words = eval(request.form['kwds'])

        datas = get_data(key_words)

        rows = [
        ]
        for data in datas:
            rows.append(
                (data['key_word'], data['product_name'], data['nick'], data['address'], data['package_num'], data['price'], data['unit_price'], data['sales'])
            )

        data = tablib.Dataset(*rows, headers=headers)

        resp = make_response(data.xlsx)

        resp.headers["Content-Disposition"] = "attachment; filename=产品.xlsx"

        return resp


def taobao_spider(app, filename, origin):
    with app.app_context():
        product_file = ProductFile(name=filename, create_date=datetime.now(), state='查询中')
        db.session.add(product_file)
        db.session.commit()

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../files/%s' % filename))

        data = xlrd.open_workbook(path)
        table = data.sheets()[0]

        nrows = table.nrows

        key_words = []

        for row in range(nrows):
            if row == 0:
                continue

            key_word = table.row_values(row)[0]

            if not isinstance(key_word, unicode):
                print 'aaaa:', key_word, type(key_word)
                continue

            if key_word not in key_words:
                key_words.append(key_word)

        if origin == 'taobao':
            for key_index, key_word in enumerate(key_words):
                # 淘宝
                crawl_key_word(key_word, product_file.id)
                print 'key_word:', key_word
                product_file.state = '%s/%s' % (key_index + 1, len(key_words))
                db.session.commit()
                print product_file.state

                # # 京东
                # crawl_key_word_jd(key_word, product_file.id)
        elif origin == 'vip':
            for key_index, key_word in enumerate(key_words):
                # 唯品会
                crawl_key_word_vip(key_word, product_file.id)
                print 'key_word:', key_word
                product_file.state = '%s/%s' % (key_index + 1, len(key_words))
                db.session.commit()
                print product_file.state
        elif origin == 'dj':
            for key_index, key_word in enumerate(key_words):
                # 京东
                crawl_key_word_jd(key_word, product_file.id)
                print 'key_word:', key_word
                product_file.state = '%s/%s' % (key_index + 1, len(key_words))
                db.session.commit()
                print product_file.state

        get_data(product_file.id)

        product_file.state = '已完成'

        db.session.commit()

        return


def crawl_key_word(key_word, product_file_id):

    total_count = 0
    i = 0

    while total_count < 20 and i <= 10:
        try:
            agent = random.choice(AGENTS_ALL)
            headers = {
                'authority': 's.taobao.com',
                'User-Agent': agent,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': 't=5946a512a4a1428471723076a7833a49; cna=/V7tFKQukWYCAT26hMJmLdL5; thw=cn; _cc_=WqG3DMC9EA%3D%3D; tg=0; enc=H0OcFdmbfx1GvlhR%2B7D7yWLejbRR5tA1KK6Rb7lBKQiaxdQ8TWp%2FS5U2FZabFFUq3Bxb9F3sxqLfqjdvTRAJhg%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=277767; cookie2=1e8c86be0612c9828d01559e4180df88; _tb_token_=fd1e3e6301ff3; miid=70716671493773963; mt=ci=0_0; v=0; JSESSIONID=092A8BAC2C61E412B06E230DDBFF0B14; l=bBMaMpRHvwTD8NOsBOCwNQKboDQtjIRAguSJGxZJi_5Qc6L_TN7Oly2PXFp6Vj5R_BLB4q0AiPv9-etki; isg=BKKiGFeyCoKhQhZZzzz1s7tR8yio48C2FvTqaew7yZXAv0I51IHuHYg967vmrx6l',
            }

            # 关键词分词
            key_word_mach = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", key_word)
            seg_list = jieba.cut(key_word_mach)

            url = "https://s.taobao.com/search?q=%s&commend=all&search_type=item&s=%s" % (key_word, 44 * i)
            # 验证改url是否已抓取
            products = Product.query.filter_by(url=url, product_file_id=product_file_id).all()

            if products and len(products) >= 20:
                print u'该产品已爬取，跳过'
                break

            content = requests.get(url, headers=headers)
            print content.url
            page_count = page2(content, key_word, url, list(seg_list), product_file_id)

            total_count += page_count

        except Exception:
            _logger.error(traceback.format_exc())
        finally:
            i += 1


def page2(content, key_word, url, seg_list, product_file_id):
    count = 0   # 当前页面爬取数量

    body = content.text
    patid = '"nid":"(.*?)"'
    patprice = '"view_price":"(.*?)"'
    patname = '"raw_title":"(.*?)"'
    pataddress = '"item_loc":"(.*?)"'
    sales = '"view_sales":"(.*?)"'
    nicks = '"nick":"(.*?)"'

    allid = re.compile(patid).findall(body)  # 商品Id集合
    allprice = re.compile(patprice).findall(body)  # 商品价格集合
    allname = re.compile(patname).findall(body)  # 商品名称集合
    alladdress = re.compile(pataddress).findall(body)  # 商户地址集合
    allsales = re.compile(sales).findall(body)  # 付款人数集合
    allnicks = re.compile(nicks).findall(body)  # 店铺合集
    print 'allid:', allid
    for j in range(0, len(allid)):

        if count >= 20:
            break

        thisid = allid[j]
        price = allprice[j]
        name = allname[j]
        address = alladdress[j]
        sale = allsales[j]
        nick = allnicks[j]

        if sale in [u'0人付款', u'0人收货']:
            continue

        sales = re.findall('\d+', sale)[0]

        if save_product(seg_list, key_word, thisid, name, address, price, sales, url, nick, product_file_id, '淘宝'):
            count += 1

    return count


def crawl_key_word_vip(key_word, product_file_id):
    total_count = 0
    i = 0

    while total_count < 20 and i <= 10:
        try:
            agent = random.choice(AGENTS_ALL)
            headers = {'User-Agent': agent}

            # 关键词分词
            key_word_mach = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", key_word)
            seg_list = jieba.cut(key_word_mach)

            url = "http://category.vip.com/suggest.php?keyword=%s&page=%s&count=100" % (key_word, i+1)
            # 验证改url是否已抓取
            products = Product.query.filter_by(url=url, product_file_id=product_file_id).all()

            if products and len(products) >= 20:
                print u'该产品已爬取，跳过'
                break

            content = requests.get(url, headers=headers)

            page_count = page2_vip(content, key_word, url, list(seg_list), product_file_id)

            total_count += page_count

        except Exception:
            _logger.error(traceback.format_exc())
        finally:
            i += 1


def page2_vip(content, key_word, url, seg_list, product_file_id):
    count = 0   # 当前页面爬取数量

    body = content.text

    products_match = '"products":(\[.*?\])'
    products = re.findall(products_match, body)

    if not products:
        return count

    products = json.loads(products[0])

    for product in products:

        if count >= 20:
            break

        thisid = product.get('product_id')
        price = product.get('price_info').get('sell_price_min_tips', 0)
        name = product.get('product_name')
        address = product.get('brand_name')
        sales = 0
        nick = product.get('brand_store_name')

        if save_product(seg_list, key_word, thisid, name, address, price, sales, url, nick, product_file_id, '唯品会'):
            count += 1

    return count


def crawl_key_word_jd(key_word, product_file_id):
    total_count = 0
    i = 0

    while total_count < 20 and i <= 10:
        try:
            agent = random.choice(AGENTS_ALL)
            headers = {'User-Agent': agent}

            # 关键词分词
            key_word_mach = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", key_word)
            seg_list = jieba.cut(key_word_mach)

            url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&page=%s" % (key_word, (i+1)*2)
            # 验证改url是否已抓取
            products = Product.query.filter_by(url=url, product_file_id=product_file_id).all()

            if products and len(products) >= 20:
                print u'该产品已爬取，跳过'
                break

            content = requests.get(url, headers=headers)

            page_count = page2_jd(content, key_word, url, list(seg_list), product_file_id)

            total_count += page_count

        except Exception:
            _logger.error(traceback.format_exc())
        finally:
            i += 1


def page2_jd(content, key_word, url, seg_list, product_file_id):
    count = 0   # 当前页面爬取数量

    soup = BeautifulSoup(content.content, 'lxml')
    items = soup.find_all('li', class_='gl-item')

    # 获取店铺
    pidList = []

    for item in items:
        pidList.append(item.get('data-sku'))

    pidList = ','.join(pidList)
    r2 = requests.get('https://chat1.jd.com/api/checkChat?pidList=' + pidList)

    res = re.findall(r'null\((.*?)\)', r2.content)
    store_dict = {}
    if res:
        store_list = json.loads(res[0])

        for store in store_list:
            if not isinstance(store, dict):
                continue
            if not store.get('seller'):
                continue
            store_dict.update({
                str(store['shopId']): store['seller']
            })

    for item in items:
        flag_item = item.div.find('span', class_='p-promo-flag')
        if flag_item and flag_item.get_text() == u'广告':
            continue

        product_item = item.find('div', class_='p-name p-name-type-2')
        price_item = item.find('div', class_='p-price')
        shop_item = item.find('div', class_='p-shop')

        thisid = product_item.a.i['id']
        price = price_item.strong.get('data-price')
        name = product_item.a.get('title')
        address = ''
        sales = 0
        nick = store_dict.get(shop_item.get('data-shopid'))

        if save_product(seg_list, key_word, thisid, name, address, price, sales, url, nick, product_file_id, '京东'):
            count += 1

    return count


def save_product(seg_list, key_word, thisid, name, address, price, sales, url, nick, product_file_id, origin):
    seg_res = True
    for seg in seg_list:
        # 全英文
        if re.match(r'[a-zA-Z]+', seg):
            # 过滤全英文
            continue
        if seg not in name:
            seg_res = False
            break

    if not seg_res:
        _logger.info('产品名称不匹配，过滤')
        return

    # 查询是否有重复商品
    if Product.query.filter_by(product_name=name, nick=nick, product_file_id=product_file_id).all():
        return

    # 获取包装数量
    num = 1

    nums = re.compile('\*\d+').findall(name)
    if nums:
        num = nums[0].replace('*', '')

    # 计算单价
    unit_price = float(price) / int(num)

    p = Product(key_word=key_word,
                product_id=thisid,
                product_name=name,
                address=address,
                package_num=num,
                price=price,
                unit_price=round(unit_price, 2),
                sales=sales,
                url=url,
                nick=nick,
                product_file_id=product_file_id,
                origin=origin)
    db.session.add(p)
    db.session.commit()
    _logger.info('保存数据来源:%s' % origin)
    return True


def get_data(product_file_id):
    all_products = Product.query.filter_by(product_file_id=product_file_id).order_by('origin', db.desc('sales')).all()

    datas = []

    for p in all_products:
        datas.append({
            'key_word': p.key_word,
            'product_name': p.product_name,
            'address': p.address,
            'package_num': p.package_num,
            'price': p.price,
            'unit_price': p.unit_price,
            'sales': p.sales,
            'nick': p.nick,
            'product_file_id': p.product_file_id,
            'origin': p.origin,
        })

    return datas

