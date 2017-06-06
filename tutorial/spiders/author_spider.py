#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'authors'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_tags = response.xpath('//div[@class="quote"]//span[last()]')
        for t in author_tags:
            yield response.follow(t.xpath('./a/@href')[0], self.parse_author)

        for t in response.xpath('//li[@class="next"]/a'):
            yield response.follow(t.xpath('./@href')[0], callback=self.parse)

    def parse_author(self, response):
        name = response.xpath('//h3[@class="author-title"]/text()').extract_first()
        birth = response.xpath('//span[@class="author-born-date"]/text()').extract_first()
        bio = response.xpath('//div[@class="author-description"]/text()').extract_first()
        yield dict(name=name.strip(), birth=birth.strip(), bio=bio.strip())

