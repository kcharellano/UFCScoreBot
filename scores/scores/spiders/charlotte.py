import scrapy


class ScoreSpider(scrapy.Spider):
    name = "charlotte"

    def start_requests(self):
        queryUrl = 'http://www.ufcstats.com/statistics/fighters/search?query=' + self.last 
        urls = [queryUrl]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        nextPage = response.xpath('//tbody/tr/td/a[text()="Chael"]/@href').extract()[0]
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.afterParse)

    def afterParse(self, response):
        #self.log("++++++++++++" + "AFTER PARSE!!");
        with open('example.html', 'wb') as f:
            f.write(response.body);
