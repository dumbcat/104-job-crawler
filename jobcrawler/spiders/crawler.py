from jobcrawler.items import JobcrawlerItem
import scrapy
import requests
import pandas as pd
from selenium import webdriver
from scrapy.selector import Selector
import time
from bs4 import BeautifulSoup as bs

# TODO: How to crawl job categories
# TODO: Job detail JSON: ttps://www.104.com.tw/job/ajax/content/63ixm need 'Referer': 'https://www.104.com.tw/job/63ixm?jobsource=2018indexpoc'

class JobSpider(scrapy.Spider):
    name = '104'
    allowed_domains = ['104.com.tw']
    # start_urls = []

    def __init__(self):
        self.browser = webdriver.Chrome()

        """Convert area names of Taiwan from JSON into DataFrame"""
        url = 'https://static.104.com.tw/category-tool/json/Area.json'
        resp = requests.get(url)
        df1 = []

        for i in resp.json()[0]['n']:
            # Only crawler Kaohsing for test
            if i['no'] == '6001016000':
                # Convert the districts of each city into DataFrame
                ndf = pd.DataFrame(i['n'])
                # Add city name field to DataFrame
                ndf['city'] = i['des']
                ndf['city_no'] = i['no']
                df1.append(ndf)

        # Concatenate all DataFrames
        df1 = pd.concat(df1, ignore_index=True)
        # Rearrange the order of columns, and sort data by no
        df1 = df1[['city', 'city_no', 'des', 'no']]
        self.df1 = df1.sort_values('no')

        """ Convert job categories from JSON into DataFrame """
        url = 'https://static.104.com.tw/category-tool/json/JobCat.json'
        resp = requests.get(url)
        df2 = []

        for i in resp.json():
            # Get all sub-categories in a main category
            for j in i['n']:
                # Convert the job title of each sub-category into DataFrame
                ndf = pd.DataFrame(j['n'])
                # Add main category field to DataFrame
                ndf['des1'] = i['des']
                # Add sub-categories field to DataFrame
                ndf['des2'] = j['des']
                df2.append(ndf)

        # Concatenate all DataFrames
        df2 = pd.concat(df2, ignore_index=True)
        # Rearrange the order of columns, and sort data by no
        df2 = df2[['des1', 'des2', 'des', 'no']]
        self.df2 = df2.sort_values('no')

    def start_requests(self):
        for city_no, areades, areacode in zip(self.df1['city_no'], self.df1['des'], self.df1['no']):
        # for jobdes1, jobdes2, jobdes, jobcode in zip(self.df2['des1'], self.df2['des2'], self.df2['des'], self.df2['no']):
            url = (f'https://www.104.com.tw/jobs/search/?ro=0&jobcat=2005002004&jobcatExpansionType=0&area={arecode}&order=11&asc=0&page=1&mode=s&jobsource=n_my104_search')
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={'areades': areades, 'city_no': city_no})

    def parse(self, response, areades, city_no):
        self.browser.get(response.url)

        for i in range(20):
            self.browser.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(0.5)

        k = 1
        while k != 0:
            try:
                self.browser.find_elements_by_class_name(
                    "js-more-page",)[-1].click()
                print(f'手動載入第 {15 + k} 頁')
                k += 1
                time.sleep(0.5)
            except:
                k = 0
                print('No more Job')

        sel = Selector(text=self.browser.page_source)

        # Exclude job advertisements when parsing
        # targets = sel.xpath(
        #     "//article[contains(@class, 'js-job-item') and not(contains(@class, 'b-block--ad'))]")

        # Include job advertisements when parsing
        targets = sel.xpath("//article[contains(@class, 'js-job-item')]")

        items = JobcrawlerItem()

        for index, target in enumerate(targets):
            items['city_no'] = city_no
            items['areades'] = areades
            items['job_titile'] = target.xpath("@data-job-name").get()
            items['company'] = target.xpath("@data-cust-name").get()
            items['company_type'] = target.xpath("@data-indcat-desc").get()
            items['experience'] = target.xpath("div[1]/ul[2]/li[2]/text()").get()
            items['link'] = 'https:' + target.xpath("div[1]/h2/a/@href").get()
            yield(items)
