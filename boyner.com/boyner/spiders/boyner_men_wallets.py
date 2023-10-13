import scrapy
import re


class BOYNERSpider(scrapy.Spider):
    name = "boyner"
    allowed_domains = ["www.boyner.com.tr"]
    start_urls = ["https://www.boyner.com.tr/erkek-canta-c-2005"]
    pages_count = 28


    def extract_color(self, s):
        size_pattern = re.compile(r'\d+(x\d+)*', re.I)
        parts = s.split(' ')
        for part in parts:
            if not size_pattern.match(part):
                return part
        return None

    def start_requests(self):
        for page in range(1, self.pages_count + 1):
            url = f'https://www.boyner.com.tr/erkek-canta-c-2005?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('div.product-item_content__9CfBp a::attr(href)').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        title = response.css('span.title_subtitle__9USXk::text').get()
        color = self.extract_color(title) if title is not None else None
        images = [url for url in response.css('div.grid_productDetailGallery__AvuaZ  img::attr(src)').getall() if url.startswith('http') and '520' in url]
        item = {
            'ID(SKU)': response.css('span.product-information-card_value__jGcTJ::text')[-1].get(),
            'Product name': title,
            'Product link': response.request.url,
            'Category_1': response.css('li.breadcrumb_itemLists__O62id a::text')[-3].get(),
            'Category_2': response.css('li.breadcrumb_itemLists__O62id a::text')[-2].get(),
            'Category_3': response.css('li.breadcrumb_itemLists__O62id a::text')[-1].get(),
            'Color': color,
            'Brand': response.css('span.title_title__laaYP::text').get(),
            'Gender': response.css('li.breadcrumb_itemLists__O62id a::text')[-3].get().split(' ')[0],
            'Description': ' '.join(response.xpath(
                '//div[@class="product-information-card_infoText__tuXRX"]//span/text() | //div[@class="product-information-card_infoText__tuXRX"]//strong/text()').getall()),
            'image_urls': images,
        }
        yield item