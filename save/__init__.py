# -*- coding:utf-8 -*-
"""
说明：
    本模块用于保存结果
    现支持格式为excel
    保存内容有['序号', '标题', '创建时间', '关键词', '链接', '备注']
"""

from save.util.utils import *
from save.util import EXCEL


def save(data, base_path):
    # print('正在储存文章 ...'.encode('utf-8'))
    mkdir(base_path)
    for key in data.keys():                   # 按类别存
        path = os.path.join(base_path, str(key)+'.xls')
        save_num = save_excel(data[key], path)
        # print('%s新存的文章数：%s'% (key, save_num))


def save_excel(data, path):
    keywords = list(set((k for d in data for k in d['keywords'])))
    excel = EXCEL(path, keywords)
    excel.write_excel(data)
    return excel.save_num


