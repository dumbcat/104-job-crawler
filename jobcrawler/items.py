# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    areades = scrapy.Field() # The name of the job area
    city_no = scrapy.Field()
    job_titile = scrapy.Field() # job name
    company = scrapy.Field() # Company name
    company_type = scrapy.Field() # Company type
    experience = scrapy.Field() # job experience requirements
    link = scrapy.Field() # job web page link
    # pass