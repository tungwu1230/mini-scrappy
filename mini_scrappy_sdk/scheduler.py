from queue import Queue


# 建立調度器（Scheduler）
class Scheduler:
    def __init__(self):
        self.queue = Queue()

    def add_request(self, url):
        self.queue.put(url)

    def get_next_request(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None
