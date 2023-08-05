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

import grpc
import time, datetime

import mobot_pb2

from sensor import Sensor

class Camera(Sensor):
    def __init__(self, metadata, stub, stream=True):
        super().__init__(metadata, stub, stream)

    def SetMetaData(self):
        camera_metadata = mobot_pb2.CameraMetadata()
        camera_metadata.available = True
        try:
            success = self.stub.SetCameraMetaData(camera_metadata)
            if not success.success:
                print("WARN: SetCameraMetaData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("SetCameraMetaData: Unable to Connect to server!")

    def GetCompressedImageStamped(self):
        compressed_image_stamped = mobot_pb2.CompressedImageStamped()
        while self.connection_error:
            time.sleep(1/self.hz)
            self.seq_id += 1

            with open(self.metadata["image"], "rb") as img_fd:
                img_bytes = bytes(img_fd.read()) 
            compressed_image_stamped.header.seq_id = self.seq_id
            timestamp = datetime.datetime.now()
            compressed_image_stamped.header.timestamp.year = timestamp.year
            compressed_image_stamped.header.timestamp.month = timestamp.month
            compressed_image_stamped.header.timestamp.day = timestamp.day
            compressed_image_stamped.header.timestamp.hour = timestamp.hour
            compressed_image_stamped.header.timestamp.minute = timestamp.minute
            compressed_image_stamped.header.timestamp.second = timestamp.second
            compressed_image_stamped.header.timestamp.microsecond = timestamp.microsecond

            compressed_image_stamped.compressed_image.data = img_bytes
            yield compressed_image_stamped

    def PublishDataStream(self):
        compressed_image_stamped_iterator = self.GetCompressedImageStamped() 
        try:
            success = self.stub.NewCameraDataStream(compressed_image_stamped_iterator)
            if not success.success:
                print("WARN: NewCameraDataStream rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewCameraDataStream: Unable to Connect to server!")

    def PublishData(self):
        self.seq_id += 1

        with open(self.metadata["image"], "rb") as img_fd:
            img_bytes = bytes(img_fd.read()) 
        compressed_image_stamped = mobot_pb2.CompressedImageStamped()
        compressed_image_stamped.header.seq_id = self.seq_id
        timestamp = datetime.datetime.now()
        compressed_image_stamped.header.timestamp.year = timestamp.year
        compressed_image_stamped.header.timestamp.month = timestamp.month
        compressed_image_stamped.header.timestamp.day = timestamp.day
        compressed_image_stamped.header.timestamp.hour = timestamp.hour
        compressed_image_stamped.header.timestamp.minute = timestamp.minute
        compressed_image_stamped.header.timestamp.second = timestamp.second
        compressed_image_stamped.header.timestamp.microsecond = timestamp.microsecond

        compressed_image_stamped.compressed_image.data = img_bytes
        try:
            accepted = self.stub.NewCameraData(compressed_image_stamped)
            if not accepted.success:
                print("WARN: NewCameraData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewCameraData: Unable to Connect to server!")
