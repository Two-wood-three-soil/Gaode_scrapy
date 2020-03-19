# -*- encoding: utf-8 -*-
from time import sleep

from scrapy.cmdline import execute
# sleep(60*60*6)
execute(['scrapy','crawl','gaode_spider'])

