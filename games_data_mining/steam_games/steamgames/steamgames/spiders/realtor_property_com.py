import scrapy
import json
import pprint

from scrapy.http import JsonRequest


class RealtorComSpider(scrapy.Spider):
    name = 'realtor_property.com'
    allowed_domains = ['realtor.com']
    start_urls = ['http://realtor.com/']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'bestbuy.csv',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    def __init__(self, city, state_code, offset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = city,
        self.state_code = state_code
        self.offset = int(offset)

    def start_requests(self):
        location = self.city[0] + ', ' + self.state_code
        payload = {
            "query": "\n\nquery ConsumerSearchMainQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $sort_type: SearchSortType, $client_data: JSON, $bucket: SearchAPIBucket)\n{\n  home_search: home_search(query: $query,\n    sort: $sort,\n    limit: $limit,\n    offset: $offset,\n    sort_type: $sort_type,\n    client_data: $client_data,\n    bucket: $bucket,\n  ){\n    count\n    total\n    results {\n      property_id\n      list_price\n      primary\n      primary_photo (https: true){\n        href\n      }\n      source {\n        id\n        agents{\n          office_name\n        }\n        type\n        spec_id\n        plan_id\n      }\n      community {\n        property_id\n        description {\n          name\n        }\n        advertisers{\n          office{\n            hours\n            phones {\n              type\n              number\n            }\n          }\n          builder {\n            fulfillment_id\n          }\n        }\n      }\n      products {\n        brand_name\n        products\n      }\n      listing_id\n      matterport\n      virtual_tours{\n        href\n        type\n      }\n      status\n      permalink\n      price_reduced_amount\n      other_listings{rdc {\n      listing_id\n      status\n      listing_key\n      primary\n    }}\n      description{\n        beds\n        baths\n        baths_full\n        baths_half\n        baths_1qtr\n        baths_3qtr\n        garage\n        stories\n        type\n        sub_type\n        lot_sqft\n        sqft\n        year_built\n        sold_price\n        sold_date\n        name\n      }\n      location{\n        street_view_url\n        address{\n          line\n          postal_code\n          state\n          state_code\n          city\n          coordinate {\n            lat\n            lon\n          }\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      tax_record {\n        public_record_id\n      }\n      lead_attributes {\n        show_contact_an_agent\n        opcity_lead_attributes {\n          cashback_enabled\n          flip_the_market_enabled\n        }\n        lead_type\n        ready_connect_mortgage {\n          show_contact_a_lender\n          show_veterans_united\n        }\n      }\n      open_houses {\n        start_date\n        end_date\n        description\n        methods\n        time_zone\n        dst\n      }\n      flags{\n        is_coming_soon\n        is_pending\n        is_foreclosure\n        is_contingent\n        is_new_construction\n        is_new_listing (days: 14)\n        is_price_reduced (days: 30)\n        is_plan\n        is_subdivision\n      }\n      list_date\n      last_update_date\n      coming_soon_date\n      photos(limit: 2, https: true){\n        href\n      }\n      tags\n      branding {\n        type\n        photo\n        name\n      }\n    }\n  }\n}",
            "variables": {
                "query": {
                    "status": [
                        "for_sale",
                        "ready_to_build"
                    ],
                    "primary": True,
                    "search_location": {
                        "location": f"{location}"
                        # "location": "New Milford, CT"
                    }
                },
                "client_data": {
                    "device_data": {
                        "device_type": "web"
                    },
                    "user_data": {
                        "last_view_timestamp": -1
                    }
                },
                "limit": 42,
                "offset": self.offset,
                "sort_type": "relevant",
                "by_prop_type": [
                    "home"
                ]
            },
            "operationName": "ConsumerSearchMainQuery",
            "callfrom": "SRP",
            "nrQueryType": "MAIN_SRP",
            "isClient": True
        }

        # yield scrapy.Request(url=f"https://www.realtor.com/realestateagents/new-york_ny/pg-{self.page}", callback=self.parse)
        yield JsonRequest(url="https://www.realtor.com/api/v1/hulk_main_srp?client_id=rdc-x&schema=vesta", data=payload,
                          callback=self.parse)

    def parse(self, response):
        # print(response.text)
        data = json.loads(response.text)
        print(data)
        # total_results = data['data']['home_search']['total']
        for result in data['data']['home_search']['results']:
            property_id = result['property_id']
            list_price = result['list_price']
            primary_photo = result['primary_photo']
            if primary_photo is None:
                primary_photo = "No Photo Available"
            else:
                primary_photo = result['primary_photo']['href']
            source = result['source']
            if source is None:
                source = "No Source Available"
            else:
                source = result['source']['id']

            agent = result['source']['agents']
            if agent is None:
                agent = "No Agent Available"
            else:
                agent = result['source']['agents']
            type = result['source']['type']
            listing_id = result['listing_id']
            virtual_tour_link = result['virtual_tours']
            if virtual_tour_link is None:
                virtual_tour_link = "No Virtual Tour Available"
            else:
                virtual_tour_link = result['virtual_tours'][0]['href']
            status = result['status']
            permalink = "https://www.realtor.com/realestateandhomes-detail/" + result['permalink']
            price_reduced_amount = result['price_reduced_amount']
            other_listings = result['other_listings']
            property_description = result['description']
            open_house_description = result['open_houses']
            if open_house_description is None:
                open_house_description = "No Open House Available"
            else:
                open_house_description = result['open_houses'][0]
            location = result['location']
            tax_record = result['tax_record']
            if tax_record is None:
                tax_record = "No Tax Record Available"
            else:
                tax_record = result['tax_record']['public_record_id']
            photos = result['photos']
            list_date = result['list_date']
            last_update_date = result['last_update_date']
            branding = result['branding']

            yield {
                'property_id': property_id,
                'list_price': list_price,
                'primary_photo': primary_photo,
                'source': source,
                'agent': agent,
                'type': type,
                'listing_id': listing_id,
                'virtual_tour_link': virtual_tour_link,
                'status': status,
                'permalink': permalink,
                'price_reduced_amount': price_reduced_amount,
                'other_listings': other_listings,
                'property_description': property_description,
                'open_house_description': open_house_description,
                'location': location,
                'tax_record': tax_record,
                'photos': photos,
                'list_date': list_date,
                'last_update_date': last_update_date,
                'branding': branding
            }
