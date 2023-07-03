Mini-scrappy：一個簡單的網路爬蟲框架
======================================

Mini-scrappy是一個類似於scrapy輕量且易於使用的Python網路爬蟲框架。它提供了一個簡單直觀的架構，讓您可以撰寫網路爬蟲，從網站中提取資料。無論您是初學者還是有經驗的開發者，Mini-scrappy都能幫助您快速建立並運行網路爬蟲專案。

如何使用？
---------------

使用Mini-scrappy非常簡單。按照以下步驟開始使用：

1. 安裝Mini-scrappy：您可以使用git clone來獲取框架。
```zsh
$ git clone https://github.com/tungwu1230/mini-scrappy.git
```

3. 建立一個爬蟲：在`spider`資料夾中，創建一個名為`example_spider.py`的Python檔案，用於定義您的爬蟲。
```commandline
mini_scrappy_sdk/
├── __init__.py
├── downloader.py
├── engine.py
├── logger.py
├── scheduler.py
├── spider
│   ├── __init__.py
│   ├── base_spider.py
│   └── example_spider.py (*)
└── types.py
```

4. 在檔案中，撰寫名為`parse()`的函式，用於定義從網頁中爬取資訊的邏輯。此外，撰寫名為`save_file()`的函式，用於定義儲存爬取資料的檔案。

```python3
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
```
