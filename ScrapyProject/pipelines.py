# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
from scrapy.utils.project import get_project_settings
import os
import shutil
import scrapy


class ScrapyprojectPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'jobbole_article', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id, create_date, front_image_url, praise_nums, comment_nums, fav_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (
            item["title"],
            item["url"],
            item["url_object_id"],
            item["create_date"],
            item["front_image_url"],
            item["praise_nums"],
            item["comment_nums"],
            item["fav_nums"],
            item["tags"],
            item["content"]))
        self.conn.commit()
        return item

class MyImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
    headers = {
        "HOST": "www.aitaotu.com",
        "Referer": "https://www.aitaotu.com/weimei/",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    # 下载图片
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, headers=self.headers)

    def item_completed(self, result, item, info)
        image_path = [value["path"] for ok, value in result if ok]
        img_path = "%s\%s" % (self.IMAGES_STORE, item['title'])
        if os.path.exists(img_path) == False:
            os.mkdir(img_path)
        # 将文件从默认下路路径移动到指定路径下
        shutil.move(self.IMAGES_STORE + "\\" +image_path[0], img_path + "\\" +image_path[0][image_path[0].find("full\\")+6:])
        item['image_path'] = img_path + "\\" + image_path[0][image_path[0].find("full\\")+6:]
        return item
