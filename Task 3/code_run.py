import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json


class GoogleNewsSpider(scrapy.Spider):
    name = 'google_news_spider'

    def start_requests(self):
        df = pd.read_csv('kyc.csv')
        df['Name'] = df['Name'].str.title()
        df = df.drop_duplicates(subset=['Name'])
        df = df['Name']
        df = df[25001:100000]

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
                    'url': base_link + link
                }


def run_spider():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'article_links.json',
        'LOG_LEVEL': 'INFO',
        # Consider additional settings like DOWNLOAD_DELAY and CONCURRENT_REQUESTS_PER_DOMAIN for polite scraping
    })

    process.crawl(GoogleNewsSpider)
    process.start()

    # Read the resulting JSON into a DataFrame after the spider finishes
    df = pd.read_json('article_links.json')
    print(df)


if __name__ == "__main__":
    run_spider()
