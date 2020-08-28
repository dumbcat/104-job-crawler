# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

# TODO: Redesign database tables (e.g. one table for each region)
class JobcrawlerPipeline:
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'crawler.db')

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()
        create_sql = """CREATE TABLE IF NOT EXISTS test (
                link TEXT PRIMARY KEY,
                areades TEXT,
                job_titile TEXT,
                company TEXT,
                company_type TEXT,
                experience TEXT);"""
        self.db_cur.execute(create_sql)
        self.db_conn.commit()

    def close_spider(self, spider):
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item
    
    def insert_db(self, items):
        values = (
            items['link'],
            items['areades'],
            items['job_titile'],
            items['company'],
            items['company_type'],
            items['experience'],
            items['areades'],
            items['job_titile'],
            items['company'],
            items['company_type'],
            items['experience'],
        )

        insert_sql = """INSERT INTO test(link, areades, job_titile, company, company_type, experience) VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(link) DO UPDATE SET areades=?, job_titile=?, company=?, company_type=?, experience=?;"""
        self.db_cur.execute(insert_sql, values)
        self.db_conn.commit()