# -*- coding: utf-8 -*-

# Scrapy settings for fjjj project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'fjjj'

SPIDER_MODULES = ['fjjj.spiders']

NEWSPIDER_MODULE = 'fjjj.spiders'

ITEM_PIPELINES = {
    'fjjj.pipelines.FjjjPipeline' : 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent

#USER_AGENT = 'fjjj (+http://www.yourdomain.com)'
