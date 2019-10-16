# -*- coding:utf-8 -*-
"""
说明：
    这里实现了单篇文章和专栏的爬取。
    article 根据article_id发起网络请求，返回的json文件中包含文章的基本信息和文章主体内容，解析文章的基本信息生成一个msg
字典对象，再将文章主体解析成BeautifulSoup对象，连同msg字典一起交给document模块下的Article解析并保存成markdown文件。
    根据专栏id获得专栏下的文章所有文章id后，逐一看成是单一的文章，由article爬取。
"""
from zhihu_spider.util import net, document
from zhihu_spider.util import const
import re
import os
from zhihu_spider.util import timer
from bs4 import BeautifulSoup
import zhihu_spider

__all__ = ['article', 'articles']

TIME_LIMIT_FLAG = False


def articles(column_id, time_limit, topic_limit, save_path):
    global TIME_LIMIT_FLAG
    # print('正在获取专栏文章 ID ...'.encode('utf-8'))

    # 若不是首次运行，就按time_limit爬；否则，获取过去所有文章
    if bool(time_limit) and os.path.exists(save_path) and bool(os.listdir(save_path)):
        num_limit = (int(time_limit)+1) * 7
    else:
        num_limit = 0
        time_limit = 0
    articles_list = articles_id(column_id, num_limit)
    request_times = dict([(i, 0) for i in articles_list])

    # print('专栏文章总数：'.encode('utf-8'), len(articles_list))
    # print('正在获取文章 ...'.encode('utf-8'))
    ars = []
    while len(articles_list) != 0:
        # if len(articles_list) % 10 == 0:
        #     print(len(articles_list))
        article_id = articles_list.pop(0)
        try:
            ar = article(article_id, topic_limit, time_limit)
            if ar:
                ars.append(ar)
        except ValueError:
            if request_times.get(article_id) < 5:
                articles_list.append(article_id)
                request_times[articles_id] += 1
        except IndexError:
            # 非论文速递的文章
            continue
        timer.random_sleep(end=zhihu_spider.SLEEP)
        if TIME_LIMIT_FLAG:
            break
    for article_id, times in request_times.items():
        if times >= 5:
            print(net.article_spider_url(article_id))
    # print('爬取完毕 ...'.encode('utf-8'))
    return ars


def articles_id(column_id, num_limit):
    article_list = list()
    offset = zhihu_spider.Controller()
    while not offset.is_end():
        response = net.column_spider(column_id, offset.next_offset(), limit=100)
        if response is None:
            raise ValueError('Response is None')
        content = response.text
        totals = re.search(r'"totals":\W(\d+)', content).group(1)
        offset.totals = int(totals)
        article_id_list = re.findall(r'"id":\W(\d+)', content)
        offset.increase(len(article_id_list))
        article_list.extend(article_id_list)
        article_id_list.clear()
        timer.random_sleep(end=zhihu_spider.SLEEP)
        if bool(num_limit) and len(article_list) > num_limit:
            offset.to_stop()
    if num_limit:
        article_list = article_list[:num_limit]
    return article_list


def article(article_id, topic_limit, time_limit):
    global TIME_LIMIT_FLAG
    response = net.article_spider(article_id)
    if response is not None:
        response_json = response.json()
        topic = re.findall(r'(\w*?)每?日?论文速递', response_json['title'])[0]
        create_date = timer.timestamp_to_date(response_json['created'])
        time_diff = timer.time_diff(create_date)
        if bool(time_limit) and time_diff > int(time_limit):
            TIME_LIMIT_FLAG = True
            return
        elif len(topic_limit) > 0 and topic not in topic_limit:
            return
        content = BeautifulSoup(response_json['content'], 'lxml').body
        article_dict = {'topic': topic,
                        'create_date': create_date,
                        'content': str(content.contents)}

        return article_dict
    else:
        raise ValueError('Response is None')


def article_msg(content):
    original_url = const.ARTICLE_URL.format(content['id'])
    title = content['title']
    background_image = content['image_url']
    date = timer.timestamp_to_date(content['created'])
    author = content['author']['name']
    author_page = const.AUTHOR_PAGE_URL.format(content['author']['url_token'])
    avatar = content['author']['avatar_url']
    article_dict = {'author': author, 'author_avatar_url': avatar, 'author_page': author_page, 'title': title,
                    'original_url': original_url, 'created_date': date, 'background': background_image}
    return document.Meta(**article_dict)