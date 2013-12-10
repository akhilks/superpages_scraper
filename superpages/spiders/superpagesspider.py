from scrapy.spider import BaseSpider
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from superpages.items import *
import re
from time import sleep
class Superpgs(BaseSpider):
	name='superpgs'
	start_urls = ['http://www.superpages.com/yellowpages/C-Pharmacies/',]

	def parse(self,response):
		sel=Selector(response)
		pharmasises_list=['http://www.superpages.com'+x for x in sel.xpath('//div[@class="leftcontent"]//div/a/@href').extract()]
		for links in pharmasises_list[:5]:

			yield Request(url=links,callback=self.parse1)

	def parse1(self,response):
		sel=Selector(response)
		pharmasies_list2=['http://www.superpages.com'+x for x in sel.xpath('//div[@class="leftcontent"]//div/a/@href').extract()]
		for links2 in pharmasies_list2[:5]:
			yield Request(url=links2,callback=self.parse2)
	def parse2(self,response):
		sel=Selector(response)
		pharmasies_all_xpath=sel.xpath('//div[contains(@id,lstg)]/.//h3/a[contains(@href,"http://www.superpages.com")]/@href').extract()
		for pharmasies in pharmasies_all_xpath:
			yield Request(url=pharmasies,callback=self.parse_item)

	def parse_item(self,response):
		sel=Selector(response)
		url=response.url
		name_xpath=sel.xpath('//*[@id="coreBizName_nonad"]/h1/text()').extract()
		address_xpath=sel.xpath('//*[@id="coreBizAddress"]/text()').extract()
		phoneno_xpath=sel.xpath('//*[@id="phNos"]/span[1]/text()').extract()
		description_xpath=sel.xpath('//*[@id="BPcoreAboutBiz_nonad"]/div/text()').extract()

		name=name_xpath[0] if name_xpath else None
		address=address_xpath[0] if address_xpath else None
		phone_no=phoneno_xpath[0].replace('\n','') if phoneno_xpath else None
		description=description_xpath[0].strip() if description_xpath else None

		item=SuperpagesItem(url=url,
			name=name,
			address=address,
			phone_no=phone_no,
			description=description
			)
		yield item