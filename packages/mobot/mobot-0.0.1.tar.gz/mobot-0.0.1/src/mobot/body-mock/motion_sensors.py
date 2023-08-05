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
import math

import mobot_pb2

from sensor import Sensor

class Accelerometer(Sensor):
    def __init__(self, metadata, stub, stream=True):
        super().__init__(metadata, stub, stream)

    def SetMetaData(self):
        accelerometer_metadata = mobot_pb2.SensorMetadata()
        accelerometer_metadata.available = True
        accelerometer_metadata.vendor = self.metadata["vendor"]
        accelerometer_metadata.version = self.metadata["version"]
        accelerometer_metadata.resolution = self.metadata["resolution"]
        accelerometer_metadata.max_range = self.metadata["max_range"]
        try:
            success = self.stub.SetAccelerometerMetaData(accelerometer_metadata)
            if not success.success:
                print("WARN: SetAccelerometerMetaData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("SetAccelerometerMetaData: Unable to Connect to server!")
    
    def GetLinearAccelerationStamped(self):
        while self.connection_error:
            time.sleep(1/self.hz)
            self.seq_id += 1

            linear_acceleration_stamped = mobot_pb2.LinearAccelerationStamped()
            linear_acceleration_stamped.header.seq_id = self.seq_id
            timestamp = datetime.datetime.now()
            linear_acceleration_stamped.header.timestamp.year = timestamp.year
            linear_acceleration_stamped.header.timestamp.month = timestamp.month
            linear_acceleration_stamped.header.timestamp.day = timestamp.day
            linear_acceleration_stamped.header.timestamp.hour = timestamp.hour
            linear_acceleration_stamped.header.timestamp.minute = timestamp.minute
            linear_acceleration_stamped.header.timestamp.second = timestamp.second
            linear_acceleration_stamped.header.timestamp.microsecond = timestamp.microsecond

            linear_acceleration_stamped.linear_acceleration.x = 0
            linear_acceleration_stamped.linear_acceleration.y = 0
            linear_acceleration_stamped.linear_acceleration.z = 0
            yield linear_acceleration_stamped

    def PublishDataStream(self):
        linear_acceleration_stamped_iterator = self.GetLinearAccelerationStamped() 
        try:
            success = self.stub.NewAccelerometerDataStream(linear_acceleration_stamped_iterator)
            if not success.success:
                print("WARN: NewAccelerometerDataStream rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewAccelerometerDataStream: Unable to Connect to server!")

    def PublishData(self):
        self.seq_id += 1
        linear_acceleration_stamped = mobot_pb2.LinearAccelerationStamped()
        linear_acceleration_stamped.header.seq_id = self.seq_id
        timestamp = datetime.datetime.now()
        linear_acceleration_stamped.header.timestamp.year = timestamp.year
        linear_acceleration_stamped.header.timestamp.month = timestamp.month
        linear_acceleration_stamped.header.timestamp.day = timestamp.day
        linear_acceleration_stamped.header.timestamp.hour = timestamp.hour
        linear_acceleration_stamped.header.timestamp.minute = timestamp.minute
        linear_acceleration_stamped.header.timestamp.second = timestamp.second
        linear_acceleration_stamped.header.timestamp.microsecond = timestamp.microsecond

        linear_acceleration_stamped.linear_acceleration.x = 0
        linear_acceleration_stamped.linear_acceleration.y = 0
        linear_acceleration_stamped.linear_acceleration.z = 0
        try:
            accepted = self.stub.NewAccelerometerData(linear_acceleration_stamped)
            if not accepted.success:
                print("WARN: NewAccelerometerData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewAccelerometerData: Unable to Connect to server!")

class Gyroscope(Sensor):
    def __init__(self, metadata, bodystate, stub, stream=True):
        super().__init__(metadata, stub, stream)
        self.bodystate = bodystate
    
    def SetMetaData(self):
        gyroscope_metadata = mobot_pb2.SensorMetadata()
        gyroscope_metadata.available = True
        gyroscope_metadata.vendor = self.metadata["vendor"]
        gyroscope_metadata.version = self.metadata["version"]
        gyroscope_metadata.resolution = self.metadata["resolution"]
        gyroscope_metadata.max_range = self.metadata["max_range"]
        try:
            success = self.stub.SetGyroscopeMetaData(gyroscope_metadata)
            if not success.success:
                print("WARN: SetGyroscopeMetaData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("SetGyroscopeMetaData: Unable to Connect to server!")

    def GetAngularVelocityStamped(self):
        while self.connection_error:
            time.sleep(1/self.hz)
            self.seq_id += 1

            angular_velocity_stamped = mobot_pb2.AngularVelocityStamped()
            angular_velocity_stamped.header.seq_id = self.seq_id
            timestamp = datetime.datetime.now()
            angular_velocity_stamped.header.timestamp.year = timestamp.year
            angular_velocity_stamped.header.timestamp.month = timestamp.month
            angular_velocity_stamped.header.timestamp.day = timestamp.day
            angular_velocity_stamped.header.timestamp.hour = timestamp.hour
            angular_velocity_stamped.header.timestamp.minute = timestamp.minute
            angular_velocity_stamped.header.timestamp.second = timestamp.second
            angular_velocity_stamped.header.timestamp.microsecond = timestamp.microsecond

            angular_velocity_stamped.angular_velocity.x = 0.0
            angular_velocity_stamped.angular_velocity.y = 0.0
            angular_velocity_stamped.angular_velocity.z = self.bodystate.w
            yield angular_velocity_stamped

    def PublishDataStream(self):
        angular_velocity_stamped_iterator = self.GetAngularVelocityStamped() 
        try:
            success = self.stub.NewGyroscopeDataStream(angular_velocity_stamped_iterator)
            if not success.success:
                print("WARN: NewGyroscopeDataStream rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewGyroscopeDataStream: Unable to Connect to server!")

    def PublishData(self):
        self.seq_id += 1
        angular_velocity_stamped = mobot_pb2.AngularVelocityStamped()
        angular_velocity_stamped.header.seq_id = self.seq_id
        timestamp = datetime.datetime.now()
        angular_velocity_stamped.header.timestamp.year = timestamp.year
        angular_velocity_stamped.header.timestamp.month = timestamp.month
        angular_velocity_stamped.header.timestamp.day = timestamp.day
        angular_velocity_stamped.header.timestamp.hour = timestamp.hour
        angular_velocity_stamped.header.timestamp.minute = timestamp.minute
        angular_velocity_stamped.header.timestamp.second = timestamp.second
        angular_velocity_stamped.header.timestamp.microsecond = timestamp.microsecond

        angular_velocity_stamped.angular_velocity.x = 0.0
        angular_velocity_stamped.angular_velocity.y = 0.0
        angular_velocity_stamped.angular_velocity.z = self.bodystate.w
        try:
            accepted = self.stub.NewGyroscopeData(angular_velocity_stamped)
            if not accepted.success:
                print("WARN: NewGyroscopeDataStream rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewGyroscopeDataStream: Unable to Connect to server!")

class Magnetometer(Sensor):
    def __init__(self, metadata, bodystate, stub, stream=True):
        super().__init__(metadata, stub, stream)
        self.bodystate = bodystate
    
    def SetMetaData(self):
        magnetometer_metadata = mobot_pb2.SensorMetadata()
        magnetometer_metadata.available = True
        magnetometer_metadata.vendor = self.metadata["vendor"]
        magnetometer_metadata.version = self.metadata["version"]
        magnetometer_metadata.resolution = self.metadata["resolution"]
        magnetometer_metadata.max_range = self.metadata["max_range"]
        try:
            success = self.stub.SetMagnetometerMetaData(magnetometer_metadata)
            if not success.success:
                print("WARN: SetMagnetometerMetaData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("SetMagnetometerMetaData: Unable to Connect to server!")

    def GetOrientationStamped(self):
        while self.connection_error:
            time.sleep(1/self.hz)
            self.seq_id += 1

            orientation_stamped = mobot_pb2.OrientationStamped()
            orientation_stamped.header.seq_id = self.seq_id
            timestamp = datetime.datetime.now()
            orientation_stamped.header.timestamp.year = timestamp.year
            orientation_stamped.header.timestamp.month = timestamp.month
            orientation_stamped.header.timestamp.day = timestamp.day
            orientation_stamped.header.timestamp.hour = timestamp.hour
            orientation_stamped.header.timestamp.minute = timestamp.minute
            orientation_stamped.header.timestamp.second = timestamp.second
            orientation_stamped.header.timestamp.microsecond = timestamp.microsecond

            orientation_stamped.orientation.x = 0.0
            orientation_stamped.orientation.y = 0.0
            orientation_stamped.orientation.z = math.sin(self.bodystate.yaw/2)
            orientation_stamped.orientation.w = math.cos(self.bodystate.yaw/2)
            yield orientation_stamped

    def PublishDataStream(self):
        orientation_stamped_iterator = self.GetOrientationStamped() 
        try:
            success = self.stub.NewMagnetometerDataStream(orientation_stamped_iterator)
            if not success.success:
                print("WARN: NewMagnetometerDataStream rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewMagnetometerDataStream: Unable to Connect to server!")

    def PublishData(self):
        self.seq_id += 1
        orientation_stamped = mobot_pb2.OrientationStamped()
        orientation_stamped.header.seq_id = self.seq_id
        timestamp = datetime.datetime.now()
        orientation_stamped.header.timestamp.year = timestamp.year
        orientation_stamped.header.timestamp.month = timestamp.month
        orientation_stamped.header.timestamp.day = timestamp.day
        orientation_stamped.header.timestamp.hour = timestamp.hour
        orientation_stamped.header.timestamp.minute = timestamp.minute
        orientation_stamped.header.timestamp.second = timestamp.second
        orientation_stamped.header.timestamp.microsecond = timestamp.microsecond

        orientation_stamped.orientation.x = 0.0
        orientation_stamped.orientation.y = 0.0
        orientation_stamped.orientation.z = math.sin(self.bodystate.yaw/2)
        orientation_stamped.orientation.w = math.cos(self.bodystate.yaw/2)
        try:
            accepted = self.stub.NewMagnetometerData(orientation_stamped)
            if not accepted.success:
                print("WARN: NewMagnetometerData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewMagnetometerData: Unable to Connect to server!")
