import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request

from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):
    name = 'baidu.com'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com']

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(), callback='parse_item'),
    )
    #
    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                meta={'cookiejar': 1},
                # callback=self.after_login,
            )

    def parse_item(self, response):
        print("当前网址: {url}".format(url=response.url))
        a = response.xpath('//a/@href').extract_first()
        print(a)
        return a

if __name__ == "__main__":
    print("jkjlgjl")
    from scrapy.cmdline import execute

    execute("scrapy crawl baidu.com".split())
    print("")