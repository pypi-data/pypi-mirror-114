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
import mobot.proto.mobot_pb2 as pb2
import mobot.proto.mobot_pb2_grpc as pb2_grpc

class Callback():
    def __init__(self):
        self.enabled = False
        self.ip = None
        self.port = None
        self.channel = None
        self.stub = None
        self.PublishDataFunc = None
        self.PublishMetaDataFunc = None

    def RegisterCallback(self, ip, port, publish_data_func_name, publish_metadata_func_name):
        self.ip = ip
        self.port = port
        self.channel = grpc.insecure_channel(ip + ":" + port)
        self.stub = pb2_grpc.MobotStub(self.channel)
        self.PublishDataFunc = getattr(self.stub, publish_data_func_name)
        self.PublishMetaDataFunc = getattr(self.stub, publish_metadata_func_name)
        self.enabled = True

    def Reset(self):
        self.enabled = False

class Sensor():
    def __init__(self, name, data_class, metadata_class):
        self.name = name
        self.data_class = data_class
        self.metadata_class = metadata_class

        self.metadata = None
        self.data_stamped = None
        self.callback = Callback()

        self.Reset()

    def Reset(self):
        self.metadata = self.metadata_class(available=False)

        self.data_stamped = self.data_class()

class Chassis(Sensor):
    def __init__(self, name, data_class, metadata_class):
        Sensor.__init__(self, name, data_class, metadata_class)
        self.cmdvel = None
        self.Reset()

    def Reset(self):
        Sensor.Reset()
        self.metadata = self.metadata_class(available=False,\
                bounding_radius=0.0,\
                bounding_height=0.0,\
                noload_max_linear_speed=0.0,\
                noload_max_angular_speed=0.0)
        self.cmdvel = pb2.DiffDriveVelocity(v=0.0, w=0.0)

class BodyState():
    def __init__(self):
        self.connected = False
        self.connection_details = None

        self.chassis = Sensor("Chassis", pb2.OdometryStamped, pb2.ChassisMetadata)
        self.accelerometer = Sensor("Accelerometer", pb2.LinearAccelerationStamped, pb2.SensorMetadata)
        self.gyroscope = Sensor("Gyroscope", pb2.AngularVelocityStamped, pb2.SensorMetadata)
        self.magnetometer = Sensor("Magnetometer", pb2.OrientationStamped, pb2.SensorMetadata)
        self.camera = Sensor("Camera", pb2.CompressedImageStamped, pb2.CameraMetadata)

    def SetConnected(self, connection_details):
        self.connected = True
        self.connection_details = connection_details

    def SetDisconnected(self):
        self.connected = False
        self.connection_details = None

        self.chassis.Reset()
        self.accelerometer.Reset()
        self.gyroscope.Reset()
        self.magnetometer.Reset()
        self.camera.Reset()
