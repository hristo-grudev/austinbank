import scrapy

from scrapy.loader import ItemLoader

from ..items import AustinbankItem
from itemloaders.processors import TakeFirst


class AustinbankSpider(scrapy.Spider):
	name = 'austinbank'
	start_urls = ['https://www.austinbank.com/blog']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "MainContentContainer")]//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-6", " " ))]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-md-12"]/p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="blogPostDateStyle"]/text()').get()

		item = ItemLoader(item=AustinbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
