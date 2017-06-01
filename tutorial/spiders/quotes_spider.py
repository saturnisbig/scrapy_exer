#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-2]
        html = response.body
        filename = 'quote-%s.html' % page
        with open(filename, 'wb') as fd:
            fd.write(html)
        self.log('Saved file %s' % filename)
