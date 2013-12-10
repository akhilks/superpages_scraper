# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SuperpagesItem(Item):
    url=Field()
    name=Field()
    address=Field()
    phone_no=Field()
    description=Field()
