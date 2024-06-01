import scrapy
import json
from scrapy.crawler import CrawlerProcess
import re
import nltk

class CustomSpider(scrapy.Spider):
    name = 'custom_spider'

    def start_requests(self):
        # Load JSON file
        with open('cleaned_data.json', 'r') as file:
            data = json.load(file)

        for item in data:
            url = item['url']
            # Added dont_filter=True to allow duplicates
            yield scrapy.Request(url, meta={'name': item['name']}, dont_filter=True)

    def parse(self, response):
        name = response.meta.get('name', 'default_name')
        url = response.url
        text_nodes = response.xpath("//body//text()[not(parent::script or parent::style)]").extract()
        content = ' '.join([re.sub(r'\s+', ' ', node).strip() for node in text_nodes if not node.isspace()])
        print(url)
        yield {
            'name': name,
            'url': url,
            'content': content
        }

def run_spider():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'final-clean_missed.json',
        'LOG_LEVEL': 'INFO',
        # Added DUPEFILTER_DEBUG setting
        'DUPEFILTER_DEBUG': True
    })

    process.crawl(CustomSpider)
    process.start()

if __name__ == "__main__":
    run_spider()

# To run the spider, execute run_spider()
