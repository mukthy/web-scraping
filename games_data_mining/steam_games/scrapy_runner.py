import subprocess


# Steam Games Data Scrapy Starter
def steam_games_data(app_id, full_name):
    path = '/Users/mukthy/Desktop/office/projects/upwork/steam/steamgames'
    subprocess.call([f'scrapy crawl steamspecial -a app_id={app_id} -o {full_name}'], shell=True, cwd=f'{path}')


# Amazon Reviews Scrapy Starter
def amazon_reviews_starter(asin, domain, pageNum, full_name):
    path = '/Users/mukthy/Desktop/office/projects/upwork/steam/steamgames'
    subprocess.call(
        [f'scrapy crawl amazonreviews -a asin={asin} -a domain={domain} -a pageNum={pageNum} -o {full_name}'],
        shell=True, cwd=f'{path}')


# Bestbuy Scrapy Starter
def bestbuy_data(page, keyword, full_name):
    path = '/Users/mukthy/Desktop/office/projects/upwork/steam/steamgames'
    subprocess.call([f'scrapy crawl bestbuy.com -a page={page} -a keyword={keyword} -o {full_name}'], shell=True, cwd=f'{path}')


# Realtor Property Scrapy Starter
def realtor_property(city, state_code, offset, full_name):
    path = '/Users/mukthy/Desktop/office/projects/upwork/steam/steamgames'
    subprocess.call(
        [f'scrapy crawl realtor_property.com -a city="{city}" -a state_code={state_code} -a offset={offset} -o {full_name}'],
        shell=True, cwd=f'{path}')


# Realtor Agent Scrapy Starter
def realtor_agent(page, city, state_code, full_name):
    path = '/Users/mukthy/Desktop/office/projects/upwork/steam/steamgames'
    subprocess.call(
        [f'scrapy crawl realtor_agent_com -a page={page} -a city="{city}" -a state_code={state_code} -o {full_name}'],
        shell=True, cwd=f'{path}')


# Realtor School Scrapy Starter
def realtor_school(city, state_code, school_level, page, full_name):
    path = '/Users/mukthy/Desktop/office/projects/upwork/steam/steamgames'
    subprocess.call(
        [f'scrapy crawl realtor_schools_com -a city="{city}" -a state_code="{state_code}" -a school_level="{school_level}" -a page="{page}" -o {full_name}'],
        shell=True, cwd=f'{path}')