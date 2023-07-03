from datetime import datetime
from typing import Generator, List, Optional, Union

from mini_scrappy_sdk.engine import Engine
from mini_scrappy_sdk.logger import logger
from ..types import BaseRequest


class BaseSpider:
    name: Optional[str] = None
    start_urls: Union[str, List[str], None] = None

    def __init__(self):
        self.start_time = datetime.now()
        self.engine = Engine()

    def start_request(self) -> Generator[BaseRequest, None, None]:
        if self.start_urls is not None:
            if isinstance(self.start_urls, list):
                for url in self.start_urls:
                    yield BaseRequest(url, callback=self.parse)
            else:
                yield BaseRequest(self.start_urls, callback=self.parse)
        else:
            raise ValueError("No start URLs provided.")

    def parse(self, response) -> Generator[Union['BaseRequest', dict, None], None, None]:
        """
        Writing your own logic to extract information from a response.
        """
        pass

    def save_file(self) -> None:
        """
        Writing your own logic to save data into a file or save data into database.
        """
        pass

    def close_spider(self) -> None:
        end_time = datetime.now()
        logger.info(f"Spider ended at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Takes {self.spider_take_time(self.start_time, end_time)}.")
        logger.info(f"Spider is closed (Finished)")

    def start_crawl(self) -> None:
        logger.info(f"{self.name} started")
        logger.info(f"Spider is running at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        request_queue = self.start_request()
        self.engine.start(request_queue)
        self.close_spider()

    @staticmethod
    def spider_take_time(start_time: datetime, end_time: datetime) -> str:
        delta = end_time - start_time
        # 提取出日、小時、分鐘和秒數
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days} days {hours} hours {minutes} minutes {seconds} seconds"
