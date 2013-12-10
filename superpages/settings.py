# Scrapy settings for superpages project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'superpages'

SPIDER_MODULES = ['superpages.spiders']
NEWSPIDER_MODULE = 'superpages.spiders'
DOWNLOAD_DELAY = 1
"""ITEM_PIPELINES = {
   'superpages.pipelines.SuperpagesPipeline'
   }
"""
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'superpages (+http://www.yourdomain.com)'
