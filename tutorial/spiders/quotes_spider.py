#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    # ]

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # tree = lxml.html.fromstring(response.text)
        tags = response.xpath('//div[@class="quote"]')
        for t in tags:
            text = t.xpath('./span[@class="text"]/text()').extract_first().strip(u'“”')
            author = t.xpath('./span/small/text()').extract_first()
            tags = t.xpath('./div/a/text()').extract_first()
            quote = dict(author=author, text=text, tags=tags)
            yield quote
        try:
            # next_page = tree.xpath('//li[@class="next"]/a')[0]
            next_page = response.xpath('//li[@class="next"]/a/@href')[0]
        except IndexError:
            print(u'没有更多内容可以爬取了，当前URL：%s' % response.url)
        else:
            # url = response.urljoin(next_page)
            # yield scrapy.Request(url, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)
