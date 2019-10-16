# coding=utf-8
"""
说明：
    本模块是筛选爬取结果
    利用关键词选取文章
"""
import re


def keywords_match(articles, keywords):
    # print('正在进行关键词匹配 ...'.encode('utf-8'))
    results = {}
    num = 0
    for article in articles:
        res = content_analysis(article, keywords)
        if bool(res):
            if article['topic'] not in results:
                results[article['topic']] = []
            results[article['topic']].extend(res)
            num += len(res)
    # print('与关键词匹配的文章总数：'.encode('utf-8'), num)
    return results


def content_analysis(article, keywords):
    create_date = article['create_date']
    text = str(article['content'])
    contents = re.findall(r'【\d+】(.*?)</span></a><br/> <br/>', text)
    res = []
    for content in contents:
        title = content.split('<br/>')[0]
        match_word = [w.lower() for w in keywords if w.lower() in title.lower()]
        if bool(keywords) and not bool(match_word):
            continue
        author = re.findall(r'作者：(.*?)<br/>', content)[0]
        link = re.findall(r'链接：.*?href="(.*?)"', content)[0]
        annotation = re.findall(r'备注：(.*?)<br/>', content)
        title_ch = re.findall(r'<br/>(标题：)?(.*?)<br/>作者', content)[0][1]
        res.append({'title': title,
                    'title_ch': title_ch,
                    'time': create_date,
                    'keywords': match_word,
                    'author': author,
                    'link': link,
                    'annotation': annotation[0] if bool(annotation) else None})
    return res

