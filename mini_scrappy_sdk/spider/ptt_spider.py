import pandas as pd
from mini_scrappy_sdk.spider.base_spider import BaseSpider
from ..types import BaseResponse


class PttSpider(BaseSpider):
    name = "ptt_spider"

    def __init__(self, url: str, max_crawl_pages: int = 1):
        super().__init__()
        self.start_urls = url
        self.max_crawl_pages = max_crawl_pages

    def parse(self, response: BaseResponse):
        items = response.xpath("//div[@class='r-ent']")

        for item in items:
            title = item.xpath("./div[@class='title']/a/text()")[0]
            author = item.xpath("./div[@class='meta']/div[@class='author']/text()")[0]
            date = item.xpath("./div[@class='meta']/div[@class='date']/text()")[0]
            link = "https://www.ptt.cc" + item.xpath("./div[@class='title']/a/@href")[0]
            # ptt content
            yield response.follow(link, callback=self.parse_content,
                                  meta={"title": title, "author": author, "date": date, "link": link})

        if self.max_crawl_pages > 1:
            self.max_crawl_pages -= 1
            next_url = "https://www.ptt.cc" + response.xpath("//div[@class='btn-group btn-group-paging']/a[2]/@href")[0]
            # previous page
            yield response.follow(next_url, callback=self.parse)

    def save_file(self, path=None):
        df = pd.DataFrame(self.engine.data)
        if path is None:
            df.to_csv(f"{self.name}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.csv", index=False)
        else:
            df.to_csv(path, index=False)

    @staticmethod
    def parse_content(response: BaseResponse):
        title = response.meta["title"]
        author = response.meta["author"]
        date = response.meta["date"]
        link = response.meta["link"]

        bbs_content = response.xpath("//div[@class='bbs-screen bbs-content']/text()")
        bbs_content = [text.strip() for text in bbs_content if text.strip()]
        bbs_content = "\n".join(bbs_content)

        yield {"title": title, "author": author, "date": date, "link": link, "bbs_content": bbs_content}
