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
import threading
import grpc

import mobot.proto.mobot_pb2 as pb2
import mobot.proto.mobot_pb2_grpc as pb2_grpc

from .body_state import BodyState
from .utils import PerfStat

class Servicer(pb2_grpc.MobotServicer):
    def __init__(self):
        self.body_state = BodyState()
        self.perf_stat = PerfStat()

#################################################
    def AttachBody(self, _, context):
        if self.body_state.connected:
            if self.body_state.connection_details == context.peer():
                print(f"Body at \"{self.body_state.connection_details}\" Already attached!")
                return pb2.Success(success=True)
            else:
                print(f"AttachBody request from \"{context.peer()}\" rejected as body at \"{self.body_state.connection_details}\" is attached!")
                return pb2.Success(success=False)
        else:
            self.body_state.SetConnected(context.peer())
            print(f"Body at \"{self.body_state.connection_details}\" Attached!")
            return pb2.Success(success=True)

    def DetachBody(self, _, context):
        if self.body_state.connected:
            if self.body_state.connection_details == context.peer():
                print(f"Body at \"{self.body_state.connection_details}\" Detached!")
                self.body_state.SetDisconnected()
                return pb2.Success(success=True)
            else:
                print(f"DetachBody request from \"{context.peer()}\" rejected as body at \"{self.body_state.connection_details}\" is attached!")
                return pb2.Success(success=False)
        else:
            print(f"DetachBody request from \"{context.peer()}\" rejected as no body is attached!")
            return pb2.Success(success=False)

    def SynchronizeClock(self, time_offset, context):
        milliseconds_since_epoch = int(time.time() * 1000)
        if self.body_state.connected:
            if self.body_state.connection_details == context.peer():
                self.perf_stat.time_offset = time_offset.milliseconds
        return pb2.TimeStamp(milliseconds_since_epoch=milliseconds_since_epoch)
#################################################

############### Chassis RPCs ####################
    def SetChassisMetaData(self, chassis_metadata, context):
        return self.SetMetaData(chassis_metadata, context.peer(), self.body_state.chassis)

    def NewOdometryData(self, odometry_stamped, context):
        odometry_stamped.timestamp.milliseconds_since_epoch =\
        self.perf_stat.chassis_new_data_arrived(odometry_stamped.timestamp.milliseconds_since_epoch)
        return self.NewData(odometry_stamped, context.peer(), self.body_state.chassis)

    def OdometryDataCallback(self, register, context):
        return self.DataCallback(register.register, context.peer(), self.body_state.chassis, "NewOdometryData", "SetChassisMetaData")

    def GetCmdVel(self, _, context):
        return self.body_state.chassis.cmdvel

    def SetCmdVel(self, cmdvel, context):
        if self.body_state.connected:
            self.body_state.chassis.cmdvel = cmdvel
            return pb2.Success(success=True)
        else:
            return pb2.Success(success=False)
#################################################

############### Accelerometer RPCs ##############
    def SetAccelerometerMetaData(self, accelerometer_metadata, context):
        return self.SetMetaData(accelerometer_metadata, context.peer(), self.body_state.accelerometer)

    def NewAccelerometerData(self, linear_acceleration_stamped, context):
        linear_acceleration_stamped.timestamp.milliseconds_since_epoch =\
        self.perf_stat.accelerometer_new_data_arrived(linear_acceleration_stamped.timestamp.milliseconds_since_epoch)
        return self.NewData(linear_acceleration_stamped, context.peer(), self.body_state.accelerometer, debug=False)

    def AccelerometerDataCallback(self, register, context):
        return self.DataCallback(register.register, context.peer(), self.body_state.accelerometer, "NewAccelerometerData" , "SetAccelerometerMetaData")
#################################################

############### Gyroscope RPCs ##################
    def SetGyroscopeMetaData(self, gyroscope_metadata, context):
        return self.SetMetaData(gyroscope_metadata, context.peer(), self.body_state.gyroscope)

    def NewGyroscopeData(self, angular_velocity_stamped, context):
        angular_velocity_stamped.timestamp.milliseconds_since_epoch =\
        self.perf_stat.gyroscope_new_data_arrived(angular_velocity_stamped.timestamp.milliseconds_since_epoch)
        return self.NewData(angular_velocity_stamped, context.peer(), self.body_state.gyroscope, debug=False)

    def GyroscopeDataCallback(self, register, context):
        return self.DataCallback(register.register, context.peer(), self.body_state.gyroscope, "NewGyroscopeData", "SetGyroscopeMetaData")
#################################################

############### Magnetometer RPCs ###############
    def SetMagnetometerMetaData(self, magnetometer_metadata, context):
        return self.SetMetaData(magnetometer_metadata, context.peer(), self.body_state.magnetometer)

    def NewMagnetometerData(self, orientation_stamped, context):
        orientation_stamped.timestamp.milliseconds_since_epoch =\
        self.perf_stat.magnetometer_new_data_arrived(orientation_stamped.timestamp.milliseconds_since_epoch)
        return self.NewData(orientation_stamped, context.peer(), self.body_state.magnetometer, debug=False)
        
    def MagnetometerDataCallback(self, register, context):
        return self.DataCallback(register.register, context.peer(), self.body_state.magnetometer, "NewMagnetometerData", "SetMagnetometerMetaData")
#################################################

############### Camera RPCs #####################
    def SetCameraMetaData(self, camera_metadata, context):
        return self.SetMetaData(camera_metadata, context.peer(), self.body_state.camera)

    def NewCameraData(self, compressed_image_stamped, context):
        compressed_image_stamped.timestamp.milliseconds_since_epoch =\
        self.perf_stat.camera_new_data_arrived(compressed_image_stamped.timestamp.milliseconds_since_epoch)
        return self.NewData(compressed_image_stamped, context.peer(), self.body_state.camera, debug=False)

    def CameraDataCallback(self, register, context):
        return self.DataCallback(register.register, context.peer(), self.body_state.camera, "NewCameraData", "SetCameraMetaData")
#################################################

############## Generic Functions #################
    def SetMetaData(self, metadata, peer, sensor):
        if self.body_state.connected:
            if self.body_state.connection_details == peer:
                print(f"Set{sensor.name}MetaData")
                sensor.metadata = metadata
                self.PublishMetaData(sensor)
                return pb2.Success(success=True)
            else:
                return pb2.Success(success=False)
        else:
            return pb2.Success(success=False)

    def PublishMetaData(self, sensor, debug=False):
        time.sleep(0.1)
        if sensor.callback.enabled:
            try:
                success = sensor.callback.PublishMetaDataFunc(sensor.metadata)
                if debug:
                    print(f"PublishMetaData[Debug]: {sensor.name} metadata published")
            except grpc.RpcError:
                print(f"Publish{sensor.name}MetaData[Warn]: Unable to publish metadata, so callback is unregistered!")
                sensor.callback.Reset()

    def PublishData(self, sensor, debug=False):
        if sensor.callback.enabled:
            try:
                success = sensor.callback.PublishDataFunc(sensor.data_stamped)
                if debug:
                    print(f"PublishData[Debug]: {sensor.name} data published")
            except grpc.RpcError:
                print(f"Publish{sensor.name}Data[Warn]: Unable to publish data, so callback is unregistered!")
                sensor.callback.Reset()

    def NewData(self, data_stamped, peer, sensor, debug=False):
        if self.body_state.connected:
            if self.body_state.connection_details == peer:
                if debug:
                    print(f"New{sensor.name}Data[Debug]")
                sensor.data_stamped = data_stamped
                thread_publish_data = threading.Thread(target = self.PublishData, args=[sensor, debug])
                thread_publish_data.start()
                thread_publish_data.join()
                return pb2.Success(success=True)
        return pb2.Success(success=False)

    def DataCallback(self, register, peer, sensor, publish_data_func_name, publish_metadata_func_name, debug=False):
        ip = peer.split(":")[1]
        port = "50052"
        if register:
            if sensor.callback.enabled:
                print(f"{sensor.name}DataCallback[Warn]: Only one client can register for callback at a time, so overwriting!")
            sensor.callback.RegisterCallback(ip, port, publish_data_func_name, publish_metadata_func_name)
            if debug:
                print(f"{sensor.name}DataCallback: Callback Registered")
            thread_publish_metadata = threading.Thread(target = self.PublishMetaData, args=[sensor])
            thread_publish_metadata.start()
            return pb2.Success(success=True)
        else:
            if sensor.callback.ip == ip:
                sensor.callback.Reset()
                if debug:
                    print(f"{sensor.name}DataCallback: Callback Unregistered")
                return pb2.Success(success=True)
            else:
                print(f"{sensor.name}DataCallback[Warn]: Client requesting to unregister is not registered!")
                return pb2.Success(success=False)
#################################################
