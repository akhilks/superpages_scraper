# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SuperpagesPipeline(object):

    def open_spider(self,spider):
        c = MongoClient('192.168.1.4')
        self.db = c.superpgs
    def process_item(self, item, spider):
        self.db[spider.name].insert(dict(item))
        return item
