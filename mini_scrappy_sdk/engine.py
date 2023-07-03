from .downloader import Downloader
from .scheduler import Scheduler


# 建立引擎（Engine）
class Engine:
    def __init__(self):
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.data = []

    def start(self, request_queue):
        # 步驟 1：接收起始 URL 類，加入調度器
        for request in request_queue:
            self.scheduler.add_request(request)

        while True:
            # 步驟 2：從調度器獲取下一個待爬取的請求
            next_request = self.scheduler.get_next_request()

            # 調度器中沒有待爬取的請求，停止爬取
            if not next_request:
                # 步驟 4：運行下載器
                resp = self.downloader.start()

                # 步驟 5：在這裡可以進一步處理響應，例如解析數據或生成項目
                for res in resp:
                    # 步驟 6：處理 parse function 返回的內容
                    parse_return = res.request.callback(res)

                    for item in parse_return:
                        if isinstance(item, dict):
                            self.data.append(item)
                        else:
                            self.scheduler.queue.put(item)

                next_request = self.scheduler.get_next_request()
                if not next_request:
                    break

            # 步驟 3：將請求加入下載器
            self.downloader.queue.put(next_request)
