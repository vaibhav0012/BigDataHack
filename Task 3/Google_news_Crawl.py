import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json
#article_links - 0:25000
#Article_links_1 = 100000:125000
#Article_links_2 = 125001:
class GoogleNewsSpider(scrapy.Spider):
    name = 'google_news_spider'

    def start_requests(self):
        df = pd.read_csv(r'C:\Users\HP\PycharmProjects\BigData\kyc.csv')
        df['Name'] = df['Name'].str.title()
        df = df.drop_duplicates(subset=['Name'])
        df = df['Name']
        df = df[125001:]

        for name in df:
            search_query = "wildlife trafficking " + name
            url = f"https://news.google.com/search?q={search_query}"
            yield scrapy.Request(url, meta={'name': name})

    def parse(self, response):
        name = response.meta['name']
        articles = response.css('div.XlKvRb')
        for article in articles:
            link = article.css('a.WwrzSb::attr(href)').get()
            base_link = "news.google.com"
            if link:
                yield {
                    'name': name,
                    'url': base_link+link
                }

def run_spider():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'article_links_2.json',
        'LOG_LEVEL': 'INFO'
    })

    process.crawl(GoogleNewsSpider)
    process.start()

if __name__ == "__main__":
    run_spider()