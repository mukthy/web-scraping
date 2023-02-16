import scrapy
import json
import pprint


class RealtorComSpider(scrapy.Spider):
    name = 'realtor_agent_com'
    allowed_domains = ['realtor.com']
    start_urls = ['http://realtor.com/']

    def __init__(self, page, city, state_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.city = city
        if ' ' in self.city:
            self.city = self.city.replace(' ', '-').lower()
        else:
            self.city = self.city.lower()
        self.state_code = state_code.lower()

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://www.realtor.com/realestateagents/{self.city}_{self.state_code}/pg-{self.page}",
            callback=self.parse)

    def parse(self, response):
        response = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        data = json.loads(response)
        agents = data['props']['pageProps']['pageData']['agents']
        print(len(agents))
        for agent in agents:
            person_name = agent['person_name']
            party_id = agent['party_id']
            phones = agent['phones']
            if phones is None:
                phones = "No Phone Available"
            else:
                phones = agent['phones']
            position = agent['title']
            types = agent['types']
            profile_url = agent['web_url']
            served_zip_codes = agent['zips']
            if 'agent_type' not in agent:
                agent_type = "No Agent Type Available"
            else:
                agent_type = agent['agent_type']
            if 'feed_licenses' not in agent:
                license = "No License Available"
            else:
                license = agent['feed_licenses']
            for_sale = agent['for_sale_price']
            recently_sold = agent['recently_sold']
            if 'agent_team_details' not in agent:
                agent_team_details = "No Agent Team Details Available"
            else:
                agent_team_details = agent['agent_team_details']
            agent_mls = agent['mls']
            marketing_areas = agent['marketing_area_cities']
            is_realtor = agent['is_realtor']
            profile_url_id = 'https://www.realtor.com/realestateagents/' + agent['id']
            joined = agent['first_year'], agent['first_month']
            if 'href' not in agent:
                agent_website = "No Website Available"
            else:
                agent_website = agent['href']
            agent_address = agent['address']
            agent_rating = agent['agent_rating']
            agent_recommendations_count = agent['recommendations_count']
            agent_reviews_count = agent['review_count']
            agent_served_areas = agent['served_areas']
            agent_specializations = agent['specializations']
            if 'slogan' not in agent:
                agent_slogan = "No Slogan Available"
            else:
                agent_slogan = agent['slogan']
            agent_languages = agent['user_languages']
            if 'video' not in agent:
                video_url = "No Video Available"
            else:
                video_url = agent['video']
            agent_photo = agent['photo']
            if agent_photo is None:
                agent_photo = "No Photo Available"
            else:
                agent_photo = agent['photo']['href']

            if 'description' not in agent:
                agent_bio = "No Bio Available"
            else:
                agent_bio = agent['description']

            if agent['office'] is None:
                office_name = "No Office Name Available"
                office_mls = "No Office MLS Available"
                office_phone = "No Office Phone Available"
                office_website = "No Office Website Available"
                office_address = "No Office Address Available"
                office_party_id = "No Office Party ID Available"
            else:
                office_name = agent['office']['name']
                office_mls = agent['office']['mls']
                office_phone = agent['office']['phones']
                office_website = agent['office']['website']
                office_address = agent['office']['address']

                if 'party_id' not in agent['office']:
                    office_party_id = "No Office Party ID Available"
                else:
                    office_party_id = agent['office']['party_id']
            office_fulfillment_id = agent['office']['fulfillment_id']

            yield {
                'person_name': person_name,
                'party_id': party_id,
                'phones': phones,
                'position': position,
                'types': types,
                'profile_url_id': profile_url_id,
                'served_zip_codes': served_zip_codes,
                'agent_type': agent_type,
                'license': license,
                'for_sale': for_sale,
                'recently_sold': recently_sold,
                'agent_team_details': agent_team_details,
                'agent_mls': agent_mls,
                'marketing_areas': marketing_areas,
                'is_realtor': is_realtor,
                'agent_website': agent_website,
                'agent_address': agent_address,
                'agent_rating': agent_rating,
                'agent_recommendations_count': agent_recommendations_count,
                'agent_reviews_count': agent_reviews_count,
                'agent_served_areas': agent_served_areas,
                'agent_photo': agent_photo,
                'agent_bio': agent_bio,
                'agent_specializations': agent_specializations,
                'agent_slogan': agent_slogan,
                'agent_languages': agent_languages,
                'video_url': video_url,
                'office_name': office_name,
                'office_mls': office_mls,
                'office_phone': office_phone,
                'office_website': office_website,
                'office_address': office_address,
                'office_party_id': office_party_id,
                'office_fulfillment_id': office_fulfillment_id,
                'joined': joined,
                'profile_url': profile_url
            }
