# MIT License

# Copyright (c) 2021 Mobot

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

class HzAndLatencyEstimator:
    # n: Number of samples used to estimate hz
    def __init__(self, n):
        self.n = n
        self.hz = 0.0
        self.latency = 0.0
        self.pings = []

    def ping(self, time_now, timestamp_this_clock):
        ################# Estimate Hz ###################
        if len(self.pings) == self.n:
            self.pings.pop(0)
        self.pings.append(time.time())
        if len(self.pings) > 1:
            self.hz = (len(self.pings) - 1) / (self.pings[-1] - self.pings[0])
        #################################################

        ############### Estimate latency ################
        self.latency = time_now - timestamp_this_clock
        #################################################

    def reset(self):
        self.hz = 0.0
        self.latency = 0.0
        self.pings = []

class PerfStat:
    def __init__(self):
        self.time_offset = 0

        self.chassis = HzAndLatencyEstimator(20)
        self.accelerometer = HzAndLatencyEstimator(20)
        self.gyroscope = HzAndLatencyEstimator(20)
        self.magnetometer = HzAndLatencyEstimator(20)
        self.camera = HzAndLatencyEstimator(20)

    def reset(self):
        self.time_offset = 0
        self.chassis.reset()
        self.accelerometer.reset()
        self.gyroscope.reset()
        self.magnetometer.reset()
        self.camera.reset()

    def estimate_timestamp_this_clock(self, time_now, timestamp):
        timestamp_this_clock = timestamp - self.time_offset
        if (time_now - timestamp_this_clock) <= 0:
            timestamp_this_clock = time_now
        return timestamp_this_clock

    def chassis_new_data_arrived(self, timestamp):
        time_now = int(time.time() * 1000)
        timestamp_this_clock = self.estimate_timestamp_this_clock(time_now, timestamp)
        self.chassis.ping(time_now, timestamp_this_clock)
        return timestamp_this_clock

    def accelerometer_new_data_arrived(self, timestamp):
        time_now = int(time.time() * 1000)
        timestamp_this_clock = self.estimate_timestamp_this_clock(time_now, timestamp)
        self.accelerometer.ping(time_now, timestamp_this_clock)
        return timestamp_this_clock

    def gyroscope_new_data_arrived(self, timestamp):
        time_now = int(time.time() * 1000)
        timestamp_this_clock = self.estimate_timestamp_this_clock(time_now, timestamp)
        self.gyroscope.ping(time_now, timestamp_this_clock)
        return timestamp_this_clock

    def magnetometer_new_data_arrived(self, timestamp):
        time_now = int(time.time() * 1000)
        timestamp_this_clock = self.estimate_timestamp_this_clock(time_now, timestamp)
        self.magnetometer.ping(time_now, timestamp_this_clock)
        return timestamp_this_clock

    def camera_new_data_arrived(self, timestamp):
        time_now = int(time.time() * 1000)
        timestamp_this_clock = self.estimate_timestamp_this_clock(time_now, timestamp)
        self.camera.ping(time_now, timestamp_this_clock)
        return timestamp_this_clock
