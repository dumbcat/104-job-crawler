# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class JobcrawlerPipeline:
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'crawler.db')

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.close()

    def process_item(self, items, spider):
        self.table_name = 'AREA' + items['city_no']
        create_sql = (
            f"CREATE TABLE IF NOT EXISTS {self.table_name} "
            f"(link TEXT PRIMARY KEY, areades TEXT, job_titile TEXT, "
            f"company TEXT, company_type TEXT, experience TEXT);"
            )
        self.db_cur.execute(create_sql)
        self.db_conn.commit()
        self.insert_db(items)
        return items
    
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

        insert_sql = (
            f"INSERT INTO {self.table_name}"
            f"(link, areades, job_titile, company, company_type, experience) "
            f"VALUES(?,?,?,?,?,?) "
            f"ON CONFLICT(link) DO UPDATE SET "
            f"areades=?, job_titile=?, company=?, company_type=?, experience=?;"
            )
        self.db_cur.execute(insert_sql, values)
        self.db_conn.commit()