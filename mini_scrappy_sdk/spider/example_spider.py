import pandas as pd
from mini_scrappy_sdk.spider.base_spider import BaseSpider


class MySpider(BaseSpider):
    name = "example_spider"

    def __init__(self):
        super().__init__()
        self.start_urls = ["https://example.com"]

    def parse(self, response):
        items = response.xpath("//body/div")

        for item in items:
            h1 = item.xpath("./h1/text()")[0]
            p1 = item.xpath("./p[1]/text()")[0]
            p2 = item.xpath("./p[2]/a/text()")[0]
            yield {"title": h1, "p1": p1, "p2": p2}

    def save_file(self):
        df = pd.DataFrame(self.engine.data)
        df.to_csv(f"{self.name}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.csv", index=False)
