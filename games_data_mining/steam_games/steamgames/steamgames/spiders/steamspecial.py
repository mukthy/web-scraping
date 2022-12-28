import sys
import scrapy


class SteamspecialSpider(scrapy.Spider):
    name = 'steamspecial'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/specials']

    custom_settings = {
        'COOKIES_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        # 'FEED_URI': 'games_data.js',
        'FEED_FORMAT': 'json'
        # 'ITEM_PIPELINES': {'__main__.ItemCollectorPipeline': 100}
    }

    def __init__(self, app_id='', *args, **kwargs):
        super(SteamspecialSpider, self).__init__(*args, **kwargs)
        self.app_id = app_id

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Referer': f'https://store.steampowered.com/agecheck/app/{self.app_id}/',
        }
        yield scrapy.Request(url=f'https://store.steampowered.com/app/{self.app_id}/', headers=headers,
                             callback=self.data_parse)

    def data_parse(self, response):

        title = response.xpath('//*[@id="appHubAppName"]/text()').get()
        price = response.css('div.discount_final_price::text').get()
        discount = response.css('div.discount_pct::text').get()
        original_price = response.css('div.discount_original_price::text').get()
        url = response.url

        yield {
            'title': title,
            'price': price,
            'discount': discount,
            'original_price': original_price,
            'url': url
        }

