from scrapy.spider import BaseSpider
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.shell import inspect_response
from superpages.items import *
import re
from urlparse import urljoin
from time import sleep


class Superpgs(BaseSpider):

	name='superpgs'
	start_urls = ['http://www.superpages.com/yellowpages/C-Pharmacies/',]

	XPATH_CATEGORY_BUSINESS_ALL='//div[@class="leftcontent"]//div/a/@href'

	def parse(self,response):
		sel=Selector(response)
		pharmasises_list=[urljoin(response.url,x) for x in sel.xpath(self.XPATH_CATEGORY_BUSINESS_ALL).extract()]
		for links in pharmasises_list[:5]:
			yield Request(url=links,callback=self.parse1)
			
	XPATH_SUB1_CATEGORY_BUSINESS_ALL='//div[@class="leftcontent"]//div/a/@href'

	def parse1(self,response):
		sel=Selector(response)
		pharmasies_list2=[ urljoin(response.url,x) for x in sel.xpath(self.XPATH_SUB1_CATEGORY_BUSINESS_ALL).extract()]
		for links2 in pharmasies_list2[:5]:
			yield Request(url=links2,callback=self.parse2)

	XPATH_SUB2_CATEGORY_BUSINESS_ALL = """
			//div[contains(@id,lstg)]/
				.//h3
					/a[contains(@href,"http://www.superpages.com")]
						/@href
		"""

	def parse2(self,response):
		sel=Selector(response)
		pharmasies_all=sel.xpath(self.XPATH_SUB2_CATEGORY_BUSINESS_ALL).extract()
		for pharmasies in pharmasies_all:
			yield Request(url=pharmasies,callback=self.parse_item)

	XPATH_BUSINESS_NAME='//*[@id="coreBizName_nonad"]/h1/text()'
	XPATH_BUSINESS_ADDRESS='//*[@id="coreBizAddress"]/text()'
	XPATH_BUSINESS_PHONENO='//*[@id="phNos"]/span[1]/text()'
	XPATH_BUSINESS_DESCRIPTION='//*[@id="coreAboutBiz_nonad"]/div/text()'

	def parse_item(self,response):
		sel=Selector(response)
		url=response.url
		namee=sel.xpath(self.XPATH_BUSINESS_NAME).extract()
		addresss=sel.xpath(self.XPATH_BUSINESS_ADDRESS).extract()
		phonenoo=sel.xpath(self.XPATH_BUSINESS_PHONENO).extract()
		descriptionn=sel.xpath(self.XPATH_BUSINESS_DESCRIPTION).extract()

		name=namee[0] if namee else None
		address=addresss[0] if addresss else None
		phone_no=phonenoo[0].replace('\n','') if phonenoo else None
		description=descriptionn[0].strip() if descriptionn else None

		item=SuperpagesItem(url=url,
			name=name,
			address=address,
			phone_no=phone_no,
			description=description
			)
		yield item