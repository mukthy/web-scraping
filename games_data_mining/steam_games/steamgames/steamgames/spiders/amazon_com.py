import scrapy


class AmazonComSpider(scrapy.Spider):
    name = 'amazonreviews'
    allowed_domains = ['amazon.com', 'amazon.in', 'amazon.co.uk']
    start_urls = ['http://amazon.com/']

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_FORMAT': 'json',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 2,
    }

    # Path: amazonreviews/amazonreviews/amazonreviews/spiders/amazon_in.py
    # Accepts asin and domain as arguments
    # scrapy crawl amazonreviews -a asin=B0B4JJBX82 -a domain=amazon.in

    def __init__(self, asin='', domain='', pageNum='', *args, **kwargs):
        super(AmazonComSpider, self).__init__(*args, **kwargs)
        self.asin = asin
        self.domain = domain
        self.pageNum = pageNum

    def start_requests(self):
        # asin = 'B06W55K9N6'
        # domain = 'amazon.co.uk'
        url = f'https://www.{self.domain}/product-reviews/{self.asin}/ref=cm_cr_arp_d_paging_btm_3?ie=UTF8&pageNumber={self.pageNum}&reviewerType=all_reviews'

        yield scrapy.Request(url=url, callback=self.parse_reviews)

    def parse_reviews(self, response):
        title = response.css('h1.a-size-large > a::text').get()
        ratings = response.css('i.averageStarRating > span::text').get()
        total_review_count = response.css('div.averageStarRatingNumerical > span::text').get()

        reviews = response.xpath("//div[@id='cm_cr-review_list']/div/div/div")
        reviewers_name = []
        for review in reviews:
            reviewer_name = review.css('span.a-profile-name::text').get()
            stars = review.css('span.a-icon-alt::text').get()
            review_title = review.css('a.review-title > span::text').get()
            review_body = review.css('span.review-text > span::text').get()
            reviews = {
                'reviewer_name': reviewer_name,
                'stars': stars,
                'review_title': review_title,
                'review_body': review_body
            }
            reviewers_name.append(reviews)
        yield {
            'ProductUrl': response.url,
            'ProductName': title,
            'ProductRating': ratings,
            'Total_Review_Count': total_review_count,
            'Reviewers': reviewers_name

        }
