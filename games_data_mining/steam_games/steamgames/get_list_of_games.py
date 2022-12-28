import requests


def games_with_offers(start, count, region):
    # start = 0
    # count = start + 100
    app_url = f'https://store.steampowered.com/saleaction/ajaxgetsaledynamicappquery?cc={region}&l=english&flavor=popularpurchaseddiscounted&start={start}&count={count}&strContentHubType=specials'
    print(app_url)
    app_ids = requests.get(url=app_url)
    data = app_ids.json()
    app_ids_list = data['appids']
    boolean = data['possible_has_more']
    total_count = data['match_count']
    return app_ids_list, boolean, total_count
