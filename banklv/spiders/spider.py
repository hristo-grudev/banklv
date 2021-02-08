import re

import scrapy
from scrapy.exceptions import CloseSpider

from scrapy.loader import ItemLoader
from ..items import BanklvItem
from itemloaders.processors import TakeFirst


class BanklvSpider(scrapy.Spider):
	name = 'banklv'
	start_urls = ['https://www.bank.lv/par-mums/jaunumi']
	page = 0

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-articles"]/div/a/@href')
		yield from response.follow_all(post_links, self.parse_post)

		self.page += 8
		next_page = f'https://www.bank.lv/par-mums/jaunumi?page={self.page}'

		if not post_links:
			raise CloseSpider('no more pages')

		yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="page-header"]/h1//text()').get()
		description = response.xpath('//div[@itemprop="articleBody"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description)
		date = response.xpath('//span[@class="publish-date"]//text()').get()

		item = ItemLoader(item=BanklvItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		if date:
			item.add_value('date', re.findall(r"(\d+.\d+.\d{4})", str(date))[0])
		else:
			item.add_value('date', '')

		return item.load_item()
