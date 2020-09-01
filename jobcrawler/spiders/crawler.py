import urllib

import pandas as pd
import requests
import scrapy

from jobcrawler.items import JobcrawlerItem


class JobSpider(scrapy.Spider):
    name = '104'
    allowed_domains = ['104.com.tw']
    # start_urls = [https://www.104.com.tw/jobs/search/]

    def __init__(self, main_city_no, df_subarea, df_jobcat):
        self.main_city_no = main_city_no
        self.df_subarea = df_subarea
        self.df_jobcat = df_jobcat

    def start_requests(self):
        """Generate the url of each district and job sub-sub-category, and
        sents it to parse_first_page for parse

        Yields:
            object: The request object of first page of each district and job
                sub-sub-category
        """
        self.url = f'https://www.104.com.tw/jobs/search/?'

        for city_no, areades, areacode in zip(self.df_subarea['city_no'],
                                              self.df_subarea['des'],
                                              self.df_subarea['no']):
            for jobdes1, jobdes2, jobdes, jobcode in zip(
                self.df_jobcat['des1'], self.df_jobcat['des2'],
                self.df_jobcat['des'], self.df_jobcat['no']
            ):
                querystring = {
                    'ro': '0',
                    'jobcatExpansionType': '0',
                    'order': '11',
                    'asc': '0',
                    'mode': 's',
                    'jobsource': '2018indexpoc',
                }
                querystring['jobcat'] = jobcode
                querystring['area'] = areacode
                search_url = self.url + urllib.parse.urlencode(querystring)

                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse_first_page,
                    cb_kwargs={'city_no': city_no, 'areades': areades,
                               'jobdes': jobdes, 'querystring': querystring})

    def parse_first_page(self, response, city_no, areades, jobdes, querystring):
        """Parse first page of each district and job sub-sub-category, then
        sents remaining pages to parse_pagination for continue parse and sents
        parse result of first page to pipeline

        Args:
            response (object): Response object of first page
            city_no (string): The city number, used for table name of database
                            in pipeline
            areades (string): The description of districts
            jobdes (string): The description of job sub-sub-category
            querystring (dictionary): The query string of url

        Yields:
            object: Sent the items object has been scraped to the item pipeline
            object: Sent request object of remaining pages to next parse
        """

        # Get total page and query requests of paginations
        res = response.xpath('//script/text()').re_first('"totalPage":\d+')
        if res:
            total_page = int(res.split(':')[1])
        else:
            total_page = 0

        # If total page is 0, means no result of this district and job
        # sub-sub-category
        if total_page != 0:
            info_string = (
                f'First Page: {city_no} '
                f'{areades}({response.url.split("&")[-1]}) '
                f'{jobdes}({response.url.split("&")[-2]}), '
                f'get total page(s): {total_page}'
            )
            print(f'\033[96m{info_string}\033[0m')
            self.logger.info(f'{info_string}')

            targets = response.xpath(
                """
                //article[contains(@class, 'js-job-item') and 
                not(contains(@class, 'b-block--ad')) and 
                not(contains(@class, 'js-job-item--recommend'))]
                """
            )
            items = JobcrawlerItem()
            for target in targets:
                items['city_no'] = city_no
                items['areades'] = areades
                items['job_titile'] = target.xpath("@data-job-name").get()
                items['company'] = target.xpath("@data-cust-name").get()
                items['company_type'] = target.xpath("@data-indcat-desc").get()
                items['experience'] = target.xpath(
                    "div[1]/ul[2]/li[2]/text()").get()
                items['link'] = 'https:' + \
                    target.xpath("div[1]/h2/a/@href").get().split('?')[0]
                yield items

            for page in range(1, total_page):
                querystring['page'] = page + 1
                search_url = self.url + urllib.parse.urlencode(querystring)

                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse_pagination,
                    cb_kwargs={'city_no': city_no,
                               'areades': areades, 'jobdes': jobdes, },
                )
        else:
            warning_string = (
                f'{total_page} Page found: {city_no} '
                f'{areades}({response.url.split("&")[-1]}) '
                f'{jobdes}({response.url.split("&")[-2]})'
            )
            print(f'\033[31m{warning_string}\033[0m')
            self.logger.warning(f'{warning_string}')

    def parse_pagination(self, response, city_no, areades, jobdes):
        """Parse the pagination of each district and job sub-sub-category,
        then sends parse result to pipeline

        Args:
            response (object): Response object of pagination
            city_no (string): The city number, used for table name of database 
                            in pipeline
            areades (string): The description of districts
            jobdes (string): The description of job sub-sub-category

        Yields:
            object: Sents the items object has been scraped to the item pipeline
        """

        info_string = (
            f'Paginations {response.url.split("&")[-1]} of {city_no} '
            f'{areades}({response.url.split("&")[-2]}) '
            f'{jobdes}({response.url.split("&")[-3]})'
        )
        print(f'\033[32m{info_string}\033[0m')
        self.logger.info(f'{info_string}')

        targets = response.xpath(
            """
            //article[contains(@class, 'js-job-item') and 
            not(contains(@class, 'b-block--ad')) and 
            not(contains(@class, 'js-job-item--recommend'))]
            """
        )
        items = JobcrawlerItem()
        for target in targets:
            items['city_no'] = city_no
            items['areades'] = areades
            items['job_titile'] = target.xpath("@data-job-name").get()
            items['company'] = target.xpath("@data-cust-name").get()
            items['company_type'] = target.xpath("@data-indcat-desc").get()
            items['experience'] = target.xpath(
                "div[1]/ul[2]/li[2]/text()").get()
            items['link'] = 'https:' + \
                target.xpath("div[1]/h2/a/@href").get().split('?')[0]
            yield items
