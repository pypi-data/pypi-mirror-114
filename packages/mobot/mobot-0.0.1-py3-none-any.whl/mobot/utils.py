import time

class Rate:
    def __init__(self, hz):
        self.hz = hz
        self.time = time.time()

    def sleep(self):
        sleep_duration = max(0, (1/self.hz) - (time.time() - self.time))
        time.sleep(sleep_duration)
        self.time = time.time()
