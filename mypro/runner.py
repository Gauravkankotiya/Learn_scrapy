'''for debugging spiders in programe create this file'''

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mypro.spiders.countries import CountriesSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl((CountriesSpider))
process.start(())
