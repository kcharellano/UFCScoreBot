import scrapy
from scores.items import ScoresItem


class ScoreSpider(scrapy.Spider):
    name = "charlotte"

    def start_requests(self):
        queryUrl = "http://www.ufcstats.com/statistics/fighters/search?query=" + self.last.strip().lower()
        urls = [queryUrl]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
            Find fighter
            TODO: What if queryUrl leads to empty fighter table?
        '''
        xpathStr = '//tbody/tr/td/a[contains(translate(text(), "ABCEDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnoqrstuvwxyz"), "{firstName}")]/@href'
        nextPage = response.xpath(xpathStr.format(firstName=self.first.strip().lower())).extract()[0]
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.afterParse)

    def afterParse(self, response):
        '''
            Extract record
        '''
        item = ScoresItem()
        xpathStr = '//*[@class="b-content__title-record"]/text()'
        item['record'] = response.xpath(xpathStr).extract()
        return item        
