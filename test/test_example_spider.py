import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

TEST_OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../output')

from mini_scrappy_sdk.spider.example_spider import MySpider

my_spider = MySpider()
my_spider.start_crawl()
my_spider.save_file()
