# 定时爬取知乎"arXiv每日论文速递"专栏

[知乎“arXiv每日论文速递”专栏](https://zhuanlan.zhihu.com/arxivdaily)每日会发出人工智能热门方向论文，包括'自然语言处理', '机器学习', '人工智能'，'计算机视觉'，'音频语音'，'量化金融'六类主题。

本项目可以设置定时爬取知乎"arXiv每日论文速递"专栏，根据给定的主题和关键字筛选结果，并将结果存入到excel表格中。
说明：爬取知乎这部分参考了https://github.com/Milloyy/ZhihuSpider


# 1. 环境

* MacOS
* python3.6
* requirements.txt



# 2. 使用说明

## 2.1 根据主题、关键字爬取

可在run.py下更改爬取时间、主题、关键字，首次执行会爬取所有文章结果。

## 2.2 定时功能

利用Mac launchctl执行定时任务，plist文件已给出（com.arxiv.timer.plist），对应修改编译环境路径、代码路径、错误输出路径即可。
