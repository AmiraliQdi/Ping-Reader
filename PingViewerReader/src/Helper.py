import threading
import psutil
import time


class MemoryMonitor(threading.Thread):
    def __init__(self, interval=1):
        super().__init__()
        self.interval = interval
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        max_mem_usage = 2000
        while not self.stopped():
            memory_usage = self.get_memory_usage()
            if memory_usage > max_mem_usage:
                print(f"\033[91mMemory usage: {memory_usage} MB\033[0m")
            time.sleep(self.interval)

    def get_memory_usage(self):
        process = psutil.Process()
        return process.memory_info().rss / (1024 ** 2)  # Memory usage in megabytes
