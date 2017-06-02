#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import scrapy
import lxml.html


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
    ]

    def parse(self, response):
        tree = lxml.html.fromstring(response.text)
        tags = tree.xpath('//div[@class="quote"]')
        for t in tags:
            text = t.xpath('./span[@class="text"]/text()')[0].strip(u'“”')
            author = t.xpath('./span/small/text()')[0]
            tags = t.xpath('./div/a/text()')
            quote = dict(author=author, text=text, tags=tags)
            yield quote
