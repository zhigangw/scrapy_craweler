import scrapy


class ProQuestAdvanceSpider(scrapy.Spider):
    name = "ProQuestAdvance"
    start_urls = [
        'http://www.pqdtcn.com'
        ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'searchText': 'Biomedical and Circuit AND Implant 68'},
            callback=self.after_post
            )

    def after_post(self, response):
        page = response.url.split("/")[-2]
        filename = 'ProQuestAdvanceResult-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)