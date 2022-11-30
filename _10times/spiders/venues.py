'''
    10times.com spider and images downloader. 
    Author: Oussama.M <oussamamechri@protonmail.com>
    Description: This spider was created for scraping venues section specifically, using scrapy, 
                 the process is done by going though each country separately and scraping all venues there, 
                 "10times_venues.csv" contains countries urls and venue count in each one, it is loaded to
                 grab a clean urls list, note that for unknown reason sometimes the scraper get stuck in a
                 loop (line: 28) for certain countries so it is hardcoded to stop at max venues pages count
    Date: 30/11/2022
'''


import scrapy
import pandas as pd
from ..items import _10TimesItem, ImageItem
import json
import re


class VenuesSpider(scrapy.Spider):
    name = 'venues'
    allowed_domains = ['10times.com']
    # Load coutries links from csv file. NB: you can specify where to start by indexing the values
    start_urls = pd.read_csv("./10times_venues.csv")['url'].values
    doit = True

    def start_requests(self):
        for url in self.start_urls:
            i = 1
            # loop through venues lists pages using 'page' param
            while self.doit:
                yield scrapy.Request(
                    url=url+f"?&ajax=1&page={i}&popular=1",
                    headers={"X-Requested-With": "XMLHttpRequest"})
                i += 1
                if i >= 242:
                    break
            self.doit = True

    def parse(self, response):
        if "No more venue found!" in response.text:
            self.doit = False
            return
        # Grab 30 venues per page and yield it to 'venue_parse' method
        venues = response.xpath("//h2/a[@class='text-decoration-none']/@href"
                                ).extract()
        if len(venues) == 0:
            self.doit = False
            return
        for v in venues:
            yield scrapy.Request(url=v,
                                 headers={
                                     "X-Requested-With": "XMLHttpRequest"},
                                 cb_kwargs={
                                     "country": response.url.split(
                                         "/")[-1].split("?")[0]},
                                 callback=self.venue_parse)

    def venue_parse(self, response, country):
        '''
            Main method for scraping data from page.
            Here the venue will be scraped for requested data stored in '_10TimesItem'
            and images in ImageItem, to be yielded later and saved according to pipelines 
        '''
        item = _10TimesItem()
        for field in item.fields:
            item.setdefault(field, "-")
        item['name'] = response.xpath(
            "//h1[@class='mb-2']/text()").extract_first()
        item['location'] = response.xpath(
            "//section[@id='address']/div/div[2]/*/text()").extract()[0]
        try:
            item['state'] = response.xpath(
                "//section[@id='address']/div/div[2]/*/text()"
            ).extract()[1].split(",")[0]
        except Exception:
            item['state'] = response.xpath(
                "//section[@id='address']/div/div[2]/*/text()"
            ).extract_first()
        item['country'] = country
        try:
            item['reviews'] = re.findall(r"[-+]?(?:\d*\.\d+|\d+)",
                                         response.xpath(
                                             "//div[@id='event-rating']/text()"
                                                        ).extract_first())
        except Exception:
            item['reviews'] = "-"
        try:
            item['rate'] = response.xpath(
                "//button[contains(@class, 'ratings')]/text()").extract_first()
        except Exception:
            item['rate'] = '-'
        space = response.xpath(
            "//section[@id='meeting-space']/div[@class='row mx-0']/div/*/text()"
        ).extract()
        for dd in space:
            if space[space.index(dd)-1] == "Total Space":
                item['total_space'] = dd
            if space[space.index(dd)-1] == "Indoor Space":
                item['indoor_space'] = dd
            if space[space.index(dd)-1] == "Outdoor Space":
                item['outdoor_space'] = dd
            if space[space.index(dd)-1] == "Number of Halls":
                item['n_halls'] = dd
            if space[space.index(dd)-1] == "Largest Hall":
                item['largest_hall'] = dd
            if space[space.index(dd)-1] == "Max Hall Capacity":
                item['max_hall_cap'] = dd
        item['url'] = response.url

        # Image itel will take venue url in addition to save image by venue name slug
        image = ImageItem()
        image['venue'] = response.url
        image['image_urls'] = json.loads(response.xpath(
            "//script[@type='application/ld+json']/text()"
            ).extract()[0])['image']
        yield image
        yield item
