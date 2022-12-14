import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            # yield {
            #     'country_name':name,
            #     'country_link':link
            # }
            # absolute_url = f'https://www.worldometers.info{link}'      # create absolute url
            # absolute_url = response.urljoin(link)                      # create absolute url
            # yield scrapy.Request(url=absolute_url)                     # needs absolute url
            yield response.follow(                                       # needs relative url
                url=link,
                callback=self.parse_country,
                meta = {'country_name':name})  
            
    def parse_country(self,response):
        # logging.info(response.url)
        country_name = response.request.meta['country_name']
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]/tbody/tr)')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'country':country_name,
                'year':year,
                'population':population
            }