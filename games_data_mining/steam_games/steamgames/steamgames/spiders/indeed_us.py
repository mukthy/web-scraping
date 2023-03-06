import re
import json
import scrapy
from urllib.parse import urlencode
from datetime import datetime

class IndeedUsSpider(scrapy.Spider):
    name = 'indeed_us'
    allowed_domains = ['indeed.com']
    start_urls = ['http://indeed.com/']

    def __init__(self, offset=0, keyword='', location='', *args, **kwargs):
        super(IndeedUsSpider, self).__init__(*args, **kwargs)
        self.offset = offset
        self.keyword = keyword
        self.location = location

    def get_indeed_search_url(self, keyword, location, offset):
        parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    def start_requests(self):
        indeed_jobs_url = self.get_indeed_search_url(self.keyword, self.location, self.offset)
        yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        # print(script_tag)
        json_blob = json.loads(script_tag[0])
        jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
        meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
        page_number = json_blob["metaData"]["mosaicProviderJobCardsModel"]["pageNumber"]
        num_results = sum(category["jobCount"] for category in meta_data)

        # print(jobs_list)
        for index, job in enumerate(jobs_list):
            job_company = job['company']
            job_title = job['title']
            job_location = job['formattedLocation']
            if 'text' not in job['salarySnippet']:
                salary = 'No Salary Mentioned'
            else:
                salary = job['salarySnippet']['text']

            published_date = job['pubDate']
            date = datetime.fromtimestamp(published_date/1000).strftime('%d-%m-%y')

            job_url = 'https://www.indeed.com' + job['viewJobLink']

            if 'companyRating' not in job:
                company_rating = 'No Rating'
            else:
                company_rating = job['companyRating']

            if 'companyReviewCount' not in job:
                company_reviews = 'No Reviews'
            else:
                company_reviews = job['companyReviewCount']

            if 'companyReviewLink' not in job:
                company_review_link = 'No Review Link'
            else:
                company_review_link = 'https://www.indeed.com' + job['companyReviewLink']

            if 'logoUrl' not in job['companyBrandingAttributes']:
                company_logo_url = 'No Logo'
            else:
                company_logo_url = job['companyBrandingAttributes']['logoUrl']

            if job['urgentlyHiring']:
                urgently_hiring = 'Urgently Hiring'
            else:
                urgently_hiring = 'Not Urgently Hiring'

            if 'hiringMultipleCandidatesModel' in job:
                multiple_hiring = job['hiringMultipleCandidatesModel']['hiresNeededExact']
            else:
                multiple_hiring = 'No Multiple Hiring'

            # page = round(int(self.offset) / 10) + 1 if int(self.offset) > 0 else 1

            yield {
                'position': index + 1,
                'company_name': job_company,
                'job_title': job_title,
                'job_location': job_location,
                'salary': salary,
                'date': date,
                'job_url': job_url,
                'urgently_hiring': urgently_hiring,
                'multiple_hiring': multiple_hiring,
                'company_rating': str(company_rating) + '/5',
                'company_reviews': company_reviews,
                'company_review_link': company_review_link,
                'company_logo_url': company_logo_url,
                'page_number': page_number
            }
