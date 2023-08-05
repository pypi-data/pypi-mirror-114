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
import threading
import time, datetime

import mobot_pb2

class Chassis():
    def __init__(self, metadata, bodystate, stub, cmd_vel_stream=True, odometry_stream=True):
        self.stub = stub
        self.metadata = metadata
        self.bodystate = bodystate
        self.publish_odometry_hz = float(metadata["publish_odometry_hz"])
        self.execute_cmdvel_hz = float(metadata["execute_cmdvel_hz"])
        self.connection_error = False

        self.odometry_stream = odometry_stream
        self.odometry_seq_id = 0
        if self.odometry_stream:
            self.thread_publish_odometry = threading.Thread(target = self.PublishOdometryDataStream)
        else:
            self.thread_publish_odometry = None

        self.thread_update_state = None

        self.cmd_vel_stream = cmd_vel_stream
        if self.cmd_vel_stream:
            self.thread_get_cmdvel = threading.Thread(target = self.GetCmdVelStream)
        else:
            self.thread_get_cmdvel = None

    def UpdateState(self):
        dt = 1/self.execute_cmdvel_hz
        v = self.bodystate.v
        w = self.bodystate.w
        self.bodystate.UpdateState(v, w, dt)
        if not self.connection_error:
            self.thread_update_state = threading.Timer(dt, self.UpdateState)
            self.thread_update_state.start()

    def start(self):
        self.SetChassisMetaData()

        self.UpdateState()

        if self.odometry_stream:
            self.thread_publish_odometry.start()
        else:
            self.PublishOdometryData()

        if self.cmd_vel_stream:
            self.thread_get_cmdvel.start()
        else:
            self.GetCmdVel()

    def SetChassisMetaData(self):
        chassis_metadate = mobot_pb2.ChassisMetadata()
        chassis_metadate.available = True
        chassis_metadate.bounding_radius = self.metadata["bounding_radius"]
        chassis_metadate.bounding_height = self.metadata["bounding_height"]
        chassis_metadate.noload_max_linear_speed = self.metadata["noload_max_linear_speed"]
        chassis_metadate.noload_max_angular_speed = self.metadata["noload_max_angular_speed"]
        try:
            success = self.stub.SetChassisMetaData(chassis_metadate)
            if not success.success:
                print("WARN: SetChassisMetaData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("SetChassisMetaData: Unable to Connect to server!")

    def GetOdometryStamped(self):
        while not self.connection_error:
            time.sleep(1/self.publish_odometry_hz)
            self.odometry_seq_id += 1

            odometry_stamped = mobot_pb2.OdometryStamped()
            odometry_stamped.header.seq_id = self.odometry_seq_id
            timestamp = datetime.datetime.now()
            odometry_stamped.header.timestamp.year = timestamp.year
            odometry_stamped.header.timestamp.month = timestamp.month
            odometry_stamped.header.timestamp.day = timestamp.day
            odometry_stamped.header.timestamp.hour = timestamp.hour
            odometry_stamped.header.timestamp.minute = timestamp.minute
            odometry_stamped.header.timestamp.second = timestamp.second
            odometry_stamped.header.timestamp.microsecond = timestamp.microsecond
            
            odometry_stamped.odometry.pose.position.x = self.bodystate.x
            odometry_stamped.odometry.pose.position.y = self.bodystate.y
            odometry_stamped.odometry.pose.yaw = self.bodystate.yaw
            odometry_stamped.odometry.velocity.v = self.bodystate.v
            odometry_stamped.odometry.velocity.w = self.bodystate.w
            yield odometry_stamped

    def PublishOdometryDataStream(self):
        odometry_stamped_iterator = self.GetOdometryStamped() 
        try:
            success = self.stub.NewOdometryDataStream(odometry_stamped_iterator)
            if not success.success:
                print("WARN: NewOdometryDataStream rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewOdometryDataStream: Unable to Connect to server!")

    def PublishOdometryData(self):
        # TODO: Publish the odometry data
        ############## Block Starts Here ##############
        self.odometry_seq_id += 1

        odometry_stamped = mobot_pb2.OdometryStamped()
        odometry_stamped.header.seq_id = self.odometry_seq_id
        timestamp = datetime.datetime.now()
        odometry_stamped.header.timestamp.year = timestamp.year
        odometry_stamped.header.timestamp.month = timestamp.month
        odometry_stamped.header.timestamp.day = timestamp.day
        odometry_stamped.header.timestamp.hour = timestamp.hour
        odometry_stamped.header.timestamp.minute = timestamp.minute
        odometry_stamped.header.timestamp.second = timestamp.second
        odometry_stamped.header.timestamp.microsecond = timestamp.microsecond
        
        odometry_stamped.odometry.pose.position.x = self.bodystate.x
        odometry_stamped.odometry.pose.position.y = self.bodystate.y
        odometry_stamped.odometry.pose.yaw = self.bodystate.yaw
        odometry_stamped.odometry.velocity.v = self.bodystate.v
        odometry_stamped.odometry.velocity.w = self.bodystate.w
        try:
            accepted = self.stub.NewOdometryData(odometry_stamped)
            if not accepted.success:
                print("WARN: NewOdometryData request rejected by server!")
        except grpc.RpcError:
            self.connection_error = True
            print("NewOdometryData: Unable to Connect to server!")
        ############## Block Ends Here ##############

        if not self.connection_error:
            self.thread_publish_odometry = threading.Timer(1/self.publish_odometry_hz, self.PublishOdometryData)
            self.thread_publish_odometry.start()

    def GetCmdVel(self):
        try:
            cmdvel = self.stub.GetCmdVel(mobot_pb2.Empty())
            self.bodystate.v = cmdvel.v
            self.bodystate.w = cmdvel.w
            if cmdvel.reset_state:
                self.bodystate.Reset()
        except grpc.RpcError:
            self.connection_error = True
            print("GetCmdVel: Unable to Connect to server!")
        if not self.connection_error:
            self.thread_get_cmdvel = threading.Timer(1/self.execute_cmdvel_hz, self.GetCmdVel)
            self.thread_get_cmdvel.start()

    def GetCmdVelStream(self):
        try:
            for cmdvel in self.stub.GetCmdVelStream(mobot_pb2.Empty()):
                # print("GetCmdVelStream")
                self.bodystate.v = cmdvel.v
                self.bodystate.w = cmdvel.w
                if cmdvel.reset_state:
                    self.bodystate.Reset()
                if self.connection_error:
                    break
        except grpc.RpcError:
            self.connection_error = True
            print("GetCmdVelStream: Unable to Connect to server!")

    def stop(self):
        self.connection_error = True
        self.thread_publish_odometry.join()
        self.thread_get_cmdvel.join()
        self.thread_update_state.join()
