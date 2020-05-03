#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/2 21:49
# @Author  : justin.郑 3907721@qq.com
# @File    : __init__.py.py
# @Desc    : 新闻类站点自动化抽取类

from web_extractor.new_extractor.AuthorExtractor import AuthorExtractor
from web_extractor.new_extractor.ContentExtractor import ContentExtractor
from web_extractor.new_extractor.TimeExtractor import TimeExtractor
from web_extractor.new_extractor.TitleExtractor import TitleExtractor
from web_extractor.utils import html2element, pre_parse, remove_noise_node, config


class NewsExtractor:
    def extract(self,
                html,
                title_xpath='',
                author_xpath='',
                publish_time_xpath='',
                host='',
                noise_node_list=None,
                with_body_html=False):
        """
        新闻类站点自动化抽取
        :param html:                新闻页面源代码
        :param title_xpath:         新闻标题xpath
        :param author_xpath:        作者xpath
        :param publish_time_xpath:  发布时间xpath
        :param host:                站点网址
        :param noise_node_list:     去除多余list内容
        :param with_body_html:
        :return:    输出json
        """
        element = html2element(html)

        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element, publish_time_xpath=publish_time_xpath)
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)

        element = pre_parse(element)
        remove_noise_node(element, noise_node_list)
        content = ContentExtractor().extract(element, host, with_body_html)
        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'content': content[0][1]['text'],
                  'images': content[0][1]['images']}
        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']
        return result

