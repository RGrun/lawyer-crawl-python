# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LawyercrawlItem(scrapy.Item):
    # define the fields for your item here like:
    lawyer_name = scrapy.Field()
    lawyer_phone = scrapy.Field()
    lawyer_site = scrapy.Field()
    lawyer_image_url = scrapy.Field()
    lawyer_location = scrapy.Field()
    lawyer_state = scrapy.Field()
    lawyer_firm = scrapy.Field()
    lawyer_addresses = scrapy.Field()
    lawyer_cornell_url = scrapy.Field()

