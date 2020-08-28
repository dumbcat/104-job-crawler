# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    areades = scrapy.Field()
    job_titile = scrapy.Field()
    company = scrapy.Field()
    company_type = scrapy.Field()
    experience = scrapy.Field()
    link = scrapy.Field()
