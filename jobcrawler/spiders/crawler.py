from jobcrawler.items import JobcrawlerItem
import scrapy
import requests
import pandas as pd
from selenium import webdriver
from scrapy.selector import Selector
import time
from bs4 import BeautifulSoup as bs

class JobSpider(scrapy.Spider):
    name = '104'
    allowed_domains = ['104.com.tw']
    start_urls = ['https://www.104.com.tw/jobs/search/?ro=0&jobcat=2005002004&jobcatExpansionType=0&area=6001016007&order=11&asc=0&page=1&mode=s&jobsource=n_my104_search',]

    def __init__(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        self.browser = webdriver.Chrome()

        # url = 'https://static.104.com.tw/category-tool/json/Area.json'
        # resp = requests.get(url)
        # df1 = []

        # # Convert area names of Taiwan from JSON into DataFrame
        # for i in resp.json()[0]['n']:
        #     # Convert the districts of each city into DataFrame
        #     ndf = pd.DataFrame(i['n'])
        #     # Add city name field to DataFrame
        #     ndf['city'] = i['des']
        #     df1.append(ndf)

        # # Concatenate all DataFrames
        # df1=pd.concat(df1, ignore_index=True)
        # # Rearrange the order of columns, and sort data by no
        # df1 = df1[['city','des','no']]
        # df1 = df1.sort_values('no')

        # url= 'https://static.104.com.tw/category-tool/json/JobCat.json'
        # resp = requests.get(url)
        # df2 = []

        # # Convert job categories from JSON into DataFrame
        # for i in resp.json():
        #     # Get all sub-categories in a main category
        #     for j in i['n']:
        #         # Convert the job title of each sub-category into DataFrame
        #         ndf = pd.DataFrame(j['n'])
        #         # Add main category field to DataFrame
        #         ndf['des1'] = i['des']
        #         # Add sub-categories field to DataFrame
        #         ndf['des2'] = j['des']
        #         df2.append(ndf)

        # # Concatenate all DataFrames
        # df2 = pd.concat(df2, ignore_index=True)
        # # Rearrange the order of columns, and sort data by no
        # df2 = df2[['des1', 'des2', 'des', 'no']]
        # df2 = df2.sort_values('no')
    
    # def start_requests(self):
    #     # start_urls = []
    #     # for areades, areacode in zip(self.df1['des'],self.df1['no']):

    #     for jobdes1, jobdes2, jobdes, jobcode in zip(self.df2['des1'], self.df2['des2'], self.df2['des'], self.df2['no']):

    #         url = f'https://www.104.com.tw/jobs/search/?ro=0&jobcat={jobcode}&jobcatExpansionType=0&area=6001001005&order=11&asc=0&page=1&mode=s&jobsource=2018indexpoc'
    #         yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):

        self.browser.get(response.url)

        for i in range(16):
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
        k = 1

        while k != 0:
            try:
                self.browser.find_elements_by_class_name("js-more-page",)[-1].click() 
                print(f'手動載入第 {15 + k} 頁')
                k += 1
                time.sleep(1)
            except:
                k = 0
                print('No more Job')

        sel = Selector(text=self.browser.page_source)
        targets = sel.xpath("//article[contains(@class, 'js-job-item') and  not(contains(@class, 'b-block--ad'))]")
        print(len(targets))
        for index, target in enumerate(targets):
            jobname = target.xpath("@data-job-name").get()
            company = target.xpath("@data-cust-name").get()
            comptype = target.xpath("@data-indcat-desc").get()
            print(f'{index}. [{comptype}] {company} - {jobname}')
