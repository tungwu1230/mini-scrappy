import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

TEST_OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../output')

from mini_scrappy_sdk import PttSpider

ptt_spider = PttSpider("https://www.ptt.cc/bbs/Education/index.html", 10)
ptt_spider.start_crawl()
ptt_spider.save_file(f"{TEST_OUTPUT_FOLDER}/ptt.csv")
