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

import threading

class Sensor():
    def __init__(self, metadata, stub, stream=True):
        self.stub = stub
        self.metadata = metadata
        self.hz = float(metadata["hz"])
        self.connection_error = False

        self.seq_id = 0
        self.stream = stream
        if self.stream:
            self.thread = threading.Thread(target = self.PublishDataStream)
        else:
            self.thread = None

    def start(self):
        self.SetMetaData()
        if self.stream:
            self.thread.start()
        else:
            self.PublishDataPriodic()

    def SetMetaData(self):
        pass

    def PublishDataStream(self):
        pass

    def PublishData(self):
        pass

    def PublishDataPriodic(self):
        self.PublishData()
        if not self.connection_error:
            self.thread = threading.Timer(1/self.hz, self.PublishDataPriodic)
            self.thread.start()

    def stop(self):
        self.connection_error = True
        self.thread.join()
