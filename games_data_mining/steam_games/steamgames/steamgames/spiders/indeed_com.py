import re
import json
import scrapy
from urllib.parse import urlencode
import time


class IndeedSearchSpider(scrapy.Spider):
    name = "indeed_search"

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
        return "https://de.indeed.com/jobs?" + urlencode(parameters) + "&vjk=2600ec987a69ff9b"

    def start_requests(self):
        keyword_list = ['LKW Fahrer']
        location_list = ['Germany']
        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_url = self.get_indeed_search_url(keyword, location)
                yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results,
                                     meta={'keyword': keyword, 'location': location, 'offset': 0}, dont_filter=True)

    def parse_search_results(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        offset = response.meta['offset']
        script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])

            ## Extract Jobs From Search Page
            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            for index, job in enumerate(jobs_list):
                urgent_needed = job.get('urgentlyHiring')
                print(urgent_needed)
                if urgent_needed is True:
                    urgent_needed = 'Urgently needed'
                else:
                    urgent_needed = 'No'

                if 'hiringMultipleCandidatesModel' in job:
                    hiring_multiple_candidates = 'Hiring Multiple Candidates'
                else:
                    hiring_multiple_candidates = 'No'
                yield {
                    'keyword': keyword,
                    'location': location,
                    'page': round(offset / 10) + 1 if offset > 0 else 1,
                    # 'page': job.get('pageNumber'),
                    'position': index,
                    'company': job.get('company'),
                    'companyRating': job.get('companyRating'),
                    # 'companyReviewCount': job.get('companyReviewCount'),
                    # 'companyRating': job.get('companyRating'),
                    # 'highlyRatedEmployer': job.get('highlyRatedEmployer'),
                    # 'jobkey': job.get('jobkey'),
                    'jobTitle': job.get('title'),
                    'jobLocationCity': job.get('jobLocationCity'),
                    # 'jobLocationPostal': job.get('jobLocationPostal'),
                    'jobLocationState': job.get('jobLocationState'),
                    # 'maxSalary': job.get('estimatedSalary').get('max') if job.get('estimatedSalary') is not None else 0,
                    # 'minSalary': job.get('estimatedSalary').get('min') if job.get('estimatedSalary') is not None else 0,
                    # 'salaryType': job.get('estimatedSalary').get('max') if job.get(
                    #     'estimatedSalary') is not None else 'none',
                    'salary': job.get('salarySnippet').get('text') if job.get('salarySnippet') is not None else 'none',
                    'pubDate': time.strftime("%d-%b-%Y", time.localtime(job.get('pubDate') / 1000)),
                    'url': "https://de.indeed.com" + job.get('link'),
                    'Hiring Multiple Canditates': hiring_multiple_candidates,
                    'Urgently Needed': urgent_needed,
                }

            ## Paginate Through Jobs Pages
            # if offset == 0:
            #     meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
            #     num_results = sum(category["jobCount"] for category in meta_data)
            #     if num_results > 1000:
            #         num_results = 50
            num_results = 31
            for offset in range(10, num_results, 10):
                url = self.get_indeed_search_url(keyword, location, offset)
                yield scrapy.Request(url=url, callback=self.parse_search_results,
                                     meta={'keyword': keyword, 'location': location, 'offset': offset})
