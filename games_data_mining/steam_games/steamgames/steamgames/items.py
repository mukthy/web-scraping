# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

import scrapy


def clean_permonth(per_month):
    if per_month is not None:
        return per_month
    else:
        per_month = ''
        return per_month


def clean_offer_percent(offer_percent):
    if offer_percent is not None:
        return offer_percent
    else:
        return 'No Offer'


def clean_regular_price(regular_price):
    if regular_price is not None:
        return regular_price
    else:
        return 'No Offer - Regular Price'


def clean_for_months(for_months):
    if for_months is not None:
        return for_months
    else:
        for_months = ''
        return for_months


def clean_color(color):
    if color is not None:
        return color
    else:
        return 'No Color'


class BestbuyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    per_month = scrapy.Field()
    offer_percent = scrapy.Field()
    regular_price = scrapy.Field()
    color = scrapy.Field()
    model_number = scrapy.Field()
    sku = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    rating = scrapy.Field()


# class SteamgamesItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
