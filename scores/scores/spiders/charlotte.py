import scrapy


class ScoreSpider(scrapy.Spider):
    name = "charlotte"

    def start_requests(self):
        queryUrl = 'http://www.ufcstats.com/statistics/fighters/search?query=' + self.last 
        urls = [queryUrl]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('++++++++Saved file %s' % filename)