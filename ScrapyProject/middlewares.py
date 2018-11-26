# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

class ImagesSpiderMiddleware(object):

    def process_request(self, request, spider):
        referer = request.url
        if referer:
            request.headers['referer'] = referer