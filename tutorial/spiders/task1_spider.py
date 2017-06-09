#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import scrapy


class BasicExtractSpider(scrapy.Spider):
    name = 'basic_task1'
    start_urls = ['http://127.0.0.1:8000/content/detail_basic']

    def parse(self, response):
        print(response.text)
