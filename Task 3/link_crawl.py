import scrapy
import json
from scrapy.crawler import CrawlerProcess
import nltk

class CustomSpider(scrapy.Spider):
    name = 'custom_spider'

    def start_requests(self):
        # Load JSON file
        with open('article_links.json', 'r') as file:
            data = json.load(file)

        # Iterate over each entry and yield a request
        for item in data:
            url = "https://" + item['url'] if not item['url'].startswith('http') else item['url']
            yield scrapy.Request(url, meta={'name': item['name']})


    def parse(self, response):
        name = response.meta.get('name', 'default_name')
        text_nodes = response.xpath("//body//text()[not(parent::script or parent::style)]").extract()
        full_content = ' '.join(text_nodes).strip()

        # Define the start and end phrases
        start_phrase = "News Help   Help Privacy Terms About Google Get the Android app Get the iOS app Send feedback Settings   Settings Language & region English (Canada) Sign in Home For you Following News Showcase Canada World Local Business Technology Entertainment Sports Science Health More   News Opening  "
        end_phrase = " Close"

        # Try to slice the content based on the phrases
        try:
            # Find the start index
            start_index = full_content.index(start_phrase) + len(start_phrase)

            # Find the end index
            end_index = full_content.index(end_phrase, start_index)

            # Extract the content
            content = full_content[start_index:end_index].strip()
        except ValueError:
            # If the start or end phrase is not found, use the full content
            content = full_content

        end_phrase = " Opening"
        end_index = content.index(end_phrase, 0)

        # Extract the content
        content = content[0:end_index].strip()

        yield {
            'name': name,
            'url': content,
        }


def run_spider():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'upd_article_url_2.json',
        'LOG_LEVEL': 'INFO'
    })

    process.crawl(CustomSpider)
    process.start()

if __name__ == "__main__":
    run_spider()

# This would be the command to run the spider
# run_spider()
