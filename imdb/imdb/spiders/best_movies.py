import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.utils.response import open_in_browser


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    # start_urls = ['https://www.imdb.com/chart/top'] #we don't need this because of start_request method

# this is the other method for setting up user agent
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top', headers={
            'User-Agent': self.user_agent
        })

# other method for setting up user agent
    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),  # add process_request in this method for changing user agent
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        # open_in_browser(response) opens response in browser
        yield {
            'Name': response.xpath("//div[@class='ipc-page-content-container ipc-page-content-container--center']/section/section/div[2]/div/h1/text()").get(),
            'Year': response.xpath("//div[@class='ipc-page-content-container ipc-page-content-container--center']/section/section/div[2]/div/div/ul/li[1]/span/text()").get(),
            'Duration': response.xpath("normalize-space(//div[@class='ipc-page-content-container ipc-page-content-container--center']/section/section/div[2]/div/div/ul/li[3]/text())").get(),
            'Genre': response.xpath("//div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/a/span/text()").get(),
            'Rating': response.xpath("//div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()").get(),
            'Movie_Url': response.url,
            'user-agent': response.request.headers['User-Agent']
        }
