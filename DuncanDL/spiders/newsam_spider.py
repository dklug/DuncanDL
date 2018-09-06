import scrapy
import os.path
import errno

class NewsamSpider(scrapy.Spider):
    name = "newsam"

    def start_requests(self):
        urls = [
            'http://faculty.ucmerced.edu/snewsam/CSE107/schedule.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-1]
        page = response.url.replace('http://faculty.ucmerced.edu/snewsam/',"")
        self.log("page %s" % page)

        filename = '%s' % page
        #Simple way of putting parentheses back in the filename
        filename = filename.replace('%28','(')
        filename = filename.replace('%29',')')

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if not os.path.isfile(filename):
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)

        if page.split(".")[-1]=="html":
            links = response.css('a::attr(href)').extract()
            for next_page in links:
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)