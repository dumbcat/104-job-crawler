from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from jobcrawler.spiders.crawler import JobSpider
import pandas as pd
import requests

class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        """
        Convert districts info of Taiwan from JSON into DataFrame
        """
        url = 'https://static.104.com.tw/category-tool/json/Area.json'
        resp = requests.get(url)
        df_area = []

        
        for i in resp.json()[0]['n']:
            # if i['no'] == '6001016000': # Only crawler Kaohsing for test
            # Convert the districts of each city into DataFrame, the
            # i['n'] include districts name and number
            ndf = pd.DataFrame(i['n'])
            # Add city name and number field to each district
            ndf['city'] = i['des']
            ndf['city_no'] = i['no']
            df_area.append(ndf)

        # Concatenate all DataFrames
        df_area = pd.concat(df_area, ignore_index=True)
        df_area = df_area[['city', 'city_no', 'des', 'no']]
        df_area = df_area.sort_values('no')

        # Group districts dataframe by city no, then generate a dict that city
        # no as key, area dataframe of city as value
        gdf = df_area.groupby('city_no')
        dict_area = {}
        for main_city_no, data in gdf.groups.items():
            dict_area[main_city_no] = df_area.iloc[data]

        """
        Convert job categories from JSON into DataFrame, there are three
        levels of job categories, the i is main categories
        """
        url = 'https://static.104.com.tw/category-tool/json/JobCat.json'
        resp = requests.get(url)
        df_jobcat = []

        
        for i in resp.json():
            # Get sub-categories in main category
            for j in i['n']:
                # Convert the sub-category of each sub-category into DataFrame,
                # the j['n'] include sub-sub-category name and number
                ndf = pd.DataFrame(j['n'])
                # Add main category and sub-categories field to each 
                # sub-sub-category
                ndf['des1'] = i['des']
                ndf['des2'] = j['des']
                df_jobcat.append(ndf)

        # Concatenate all DataFrames
        df_jobcat = pd.concat(df_jobcat, ignore_index=True)
        df_jobcat = df_jobcat[['des1', 'des2', 'des', 'no']]
        df_jobcat = df_jobcat.sort_values('no')

        settings = get_project_settings()
        process = CrawlerProcess(settings)

        for main_city_no in dict_area.keys():
            process.crawl(JobSpider, main_city_no=main_city_no, df_subarea=dict_area[main_city_no], df_jobcat=df_jobcat)
        process.start()