import scrapy
import json
import pprint


class RealtorComSpider(scrapy.Spider):
    name = 'realtor_schools_com'
    allowed_domains = ['realtor.com']
    start_urls = ['http://realtor.com/']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'bestbuy.csv',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    def __init__(self, city, state_code, school_level, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = city
        self.state_code = state_code
        self.school_level = school_level
        self.page = page

    def start_requests(self):
        # self.location = self.location.replace(" ", "-")
        # self.location = self.location.replace(",", "_")

        base_url = "https://www.realtor.com/local/api/v1/geo-landing/pages-service/schools?geo={"
        rest_url = f'"area_type":"city","_score":1.004,"city":"{self.city}","state_code":"{self.state_code}","country":"USA"'
        special_char = '}'
        end_url = f'&tab={self.school_level}&pagination={self.page}'

        yield scrapy.Request(url=base_url + rest_url + special_char + end_url,
                             callback=self.parse)

    def parse(self, response):
        # print(response.text)
        data = json.loads(response.text)
        # pprint.pprint(data)
        schools_list = data['result']['result']['schools']['items']
        total_school_count = data['result']['result']['schools']['total']
        print(f'Total Schools: {total_school_count}')
        for school in schools_list:
            yield {
                'name': school['name'],
                'id': school['id'],
                'funding_type': school['funding_type'],
                'parent_rating': school['parent_rating'],
                'rating': school['rating'],
                'location': school['location'],
                'coordinates': school['coordinate'],
                'grades': school['grades'],
                'review_count': school['review_count'],
                'school url': 'https://www.realtor.com/local/schools/' + school['slug_id']
            }
