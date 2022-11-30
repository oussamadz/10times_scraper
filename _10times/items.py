# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class _10TimesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    location = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    reviews = scrapy.Field()
    rate = scrapy.Field()
    total_space = scrapy.Field()
    indoor_space = scrapy.Field()
    outdoor_space = scrapy.Field()
    n_halls = scrapy.Field()
    largest_hall = scrapy.Field()
    max_hall_cap = scrapy.Field()
    url = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    venue = scrapy.Field()
    pass
