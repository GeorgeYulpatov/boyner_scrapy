import scrapy


class BOYNERSpider(scrapy.Spider):
    # name = "boyner"
    allowed_domains = ["www.boyner.com.tr"]
    start_urls = ["https://www.boyner.com.tr/erkek-canta-c-2005"]
    pages_count = 28

    def start_requests(self):
        for page in range(2, 1 + self.pages_count):
            url = f'https://www.boyner.com.tr/erkek-canta-c-2005?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('div.product-item_content__9CfBp a::attr(href)').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        item = {
            'ID(SKU)': response.css('span.product-information-card_value__jGcTJ::text')[-1].get(),
            'Product name': response.css('span.title_subtitle__9USXk::text').get(),
            'Product link': response.request.url,
            'Category_1': response.css('li.breadcrumb_itemLists__O62id a::text')[-3].get(),
            'Category_2': response.css('li.breadcrumb_itemLists__O62id a::text')[-2].get(),
            'Category_3': response.css('li.breadcrumb_itemLists__O62id a::text')[-1].get(),
            'Color': response.css('span.title_subtitle__9USXk::text').get().split(' ')[0]
            if response.css('span.title_subtitle__9USXk::text').get() is not None else None,
            'Brand': response.css('span.title_title__laaYP::text').get(),
            'Gender': response.css('li.breadcrumb_itemLists__O62id a::text')[-3].get().split(' ')[0],
            'Description': ' '.join(response.xpath('//div[@class="product-information-card_infoText__tuXRX"]'
                                                   '//span/text() | //div[@class="product-information-card_'
                                                   'infoText__tuXRX"]//strong/text()').getall()),
            # 'Image name':
        }
        yield item