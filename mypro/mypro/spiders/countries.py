import scrapy
import logging
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f'https://www.worldometers.info{link}'
            # absolute_url = response.urljoin(link)

            # yield scrapy.Request(url=absolute_url)

            # yield {
            #     'country_name': name,
            #     'country_link': link,
            # }
            # after scrapy sends request to each country link response will be sent to parse_country method
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        # open_in_browser(response) #for viewving response in browser while debugging
        # inspect_response(response, self) #for debugging scrapy spider in terminal
        # logging the info for each response we get
        # logging.info(response.status) #for debugging by logging and get status of requests
        name = response.meta['country_name']
        rows = response.xpath(
            '//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'Country_name': name,
                'year': year,
                'population': population
            }
