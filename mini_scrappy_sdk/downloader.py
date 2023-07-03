import requests
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from typing import List
from .types import BaseRequest, BaseResponse


# 建立下載器 (Downloader)
class Downloader:
    def __init__(self, num_workers: int = 10):
        self.num_workers = num_workers
        self.queue: Queue[BaseRequest] = Queue()
        self.results: Queue[BaseResponse] = Queue()

    def download(self, request: BaseRequest):
        if request.method == "POST":
            r = requests.post(request.url, json=request.payload, headers=request.headers)
        else:
            r = requests.get(request.url, headers=request.headers)
        self.results.put(BaseResponse(request, r.text))

    def start(self) -> List[BaseResponse]:
        download_queue = []
        while not self.queue.empty():
            download_queue.append(self.queue.get())

        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            executor.map(self.download, download_queue)

        results = []
        while not self.results.empty():
            results.append(self.results.get())

        return results
