#!/Users/liangsong/anaconda3/bin python3.
# -*- coding:utf-8 -*-

"""
获取Arxiv每日最新论文
启动入口
"""
from zhihu_spider.article import articles
from process.match import keywords_match
from save import save

save_path = "/save"
# 爬取最近N天的paper，N默认为1；如果给出0，就爬取全部
time_limit = 1
# 可选主题，包括'自然语言处理', '机器学习', '人工智能'，'计算机视觉'，'音频语音'，'量化金融';若不给出，默认全部
topics = ['自然语言处理', '机器学习', '人工智能']
# 关键词，若不给出，默认所有文章
keywords = []
# 知乎专栏名称
column_id = 'arxivdaily'


def main():
    # step1 爬
    paper = articles(column_id, time_limit, topics, save_path)
    # step2 处理+存
    if not bool(paper):
        print('该时间段内没有包含任一主题的新文章！'.encode('utf-8'))
    else:
        results = keywords_match(paper, keywords)
        if not bool(results):
            print('该时间段内没有包含任一关键词的新文章！'.encode('utf-8'))
        else:
            save(results, save_path)


if __name__ == '__main__':
    main()



