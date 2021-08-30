import scrapy
 
class User1337xSpider(scrapy.Spider):
    name = 'user-1337x'
    allowed_domains = ['1337x.to']
    base_url = 'https://1337x.to'

    def __init__(self, user='', start_page=1, end_page=1, rate=5.0, **kwargs):
        self.start_urls = [self.base_url + f'/{user}-torrents/{i}/' for i in range(int(start_page),int(end_page)+1)]
        self.user = user
        #download_delay is used for rate limiting to avoid unnecessary traffic, blocks or suspicions of DDoS attack
        self.download_delay = 1.0/float(rate)
        super().__init__(**kwargs)
 
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)
 
    def parse_list(self, response):
        for item in response.css('td.coll-1.name a:nth-child(2)'):
            torrent_url = self.base_url + item.css('a::attr(href)').get()
            yield scrapy.Request(torrent_url, callback=self.parse_torrent)

    def parse_torrent(self, response):
        category, typ, lang, size, _ = response.css('.no-top-radius > .clearfix > ul:nth-child(2) li span::text').getall()
        yield {
            'title' : response.css('#files > span.head::text').get(),
            'url': response.url,
            'magnet': response.css('.dropdown-menu li:nth-child(4) a::attr(href)').get(),
            'hash': response.css('.infohash-box p span::text').get(),
            'category': category,
            'type': typ,
            'lang': lang,
            'size': size,
            'uploadedBy': self.user
        }