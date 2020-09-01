# Scrapy crawler for www.104.com.tw

+ Main Features

    + Use districts of city and job categories to combine search result pages, and then crawl content

    + Each city create a spider for crawling

    + The crawl results are stored in the sqlite database, and each city uses its own data table

## Require Packages

+ scrapy
+ urllib
+ requests
+ pandas
+ sqlite3

## Structure

+ **commands/multi_crawler&#46;py:** Create spiders for each city

+ **spiders/crawler&#46;py:** Crawling and parsing pages

+ **items&#46;py:** Store extracted data from web pages as items 

+ **pipelines&#46;py:** Execute the SQL to create table and insert data to database

+ **crawler_selenium&#46;py:** The early way to use selenium to render web pages to crawl

## Attention

+ Known BUG

    + When multiple processes insert data to the database at the same time, it may be because of Sqlite's default transaction mode that only one insert will succeed

## Reference

[1] https://docs.scrapy.org/en/latest/index.html

[2] https://ithelp.ithome.com.tw/users/20107875/ironman/2209

[3] https://ithelp.ithome.com.tw/users/20107514/ironman/1919

[4] https://ithelp.ithome.com.tw/users/20113582/ironman/2771

[5] https://www.royenotes.com/python-104-employment-agency/

[6] https://tlyu0419.github.io/2019/04/18/Crawl-JobList104/#more

[7] https://medium.com/web-scraper/%E5%A6%82%E4%BD%95%E7%94%A8web-scraper%E7%88%AC%E8%9F%B2-%E7%88%AC%E5%8F%96%E7%84%A1%E9%99%90%E4%B8%8B%E6%8B%89%E6%BB%BE%E5%8B%95%E9%A0%81%E9%9D%A2%E7%9A%84%E8%B3%87%E6%96%99-%E4%BB%A5104%E7%B6%B2%E7%AB%99%E7%82%BA%E4%BE%8B-2e15934a4d73
