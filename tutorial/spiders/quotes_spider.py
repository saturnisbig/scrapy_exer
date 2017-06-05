#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import scrapy
import lxml.html


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
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
        try:
            next_page = tree.xpath('//li[@class="next"]/a/@href')[0]
        except IndexError:
            print(u'没有更多内容可以爬取了，当前URL：%s' % response.url)
        else:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)

