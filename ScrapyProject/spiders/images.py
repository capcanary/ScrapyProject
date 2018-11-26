# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ScrapyProject.items import ImagesItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['www.aitaotu.com']
    start_urls = ['https://www.aitaotu.com/weimei/']

    headers = {
        "HOST": "www.aitaotu.com",
        "Referer": "https://www.aitaotu.com/weimei/",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }


    #处理列表页
    def parse(self, response):
        #获取列表页中的所有url并交给scrapy下载后并进行解析
        post_urls =  response.css('.Pli-litpic::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), headers=self.headers, callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url = response.css('#pageNum a::attr(href)').extract()[-2]
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), headers=self.headers, callback=self.parse)


    #处理详情页
    def parse_detail(self, response):
        item = ImagesItem()
        image_urls = response.css('#big-pic img::attr(src)').extract_first()
        title = response.css('#photos h2::text').extract_first()
        item['image_urls'] = [image_urls]
        item['title'] = title

        next_url = response.css('#nl > a:nth-child(1)::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), headers=self.headers, callback=self.parse_detail)

        yield item
