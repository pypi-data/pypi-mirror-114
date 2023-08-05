#!/usr/bin/env python3
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

import signal, sys
import socket
import math
import argparse
import yaml
import grpc

import mobot_pb2
import mobot_pb2_grpc

from chassis import Chassis
from motion_sensors import Accelerometer, Gyroscope, Magnetometer
from camera import Camera

class MobotState():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.v = 0
        self.w = 0

    def Reset(self):
        self.x = 0
        self.y = 0
        self.yaw = 0
        self.v = 0
        self.w = 0

    def UpdateState(self, v, w, dt):
        self.x += self.v * dt * math.cos(self.yaw)
        self.y += self.v * dt * math.sin(self.yaw)
        self.yaw += self.w * dt
        self.v = v
        self.w = w

    def __str__(self):
        return f"x: {round(self.x,4)}, y: {round(self.y,4)}, yaw: {round(self.yaw,4)}, v: {round(self.v,4)}, w: {round(self.w,4)}"

class MobotBody():
    def __init__(self, metadata, ip, port):
        self.metadata = metadata
        self.ip = ip
        self.port = port
        self.channel = grpc.insecure_channel(self.ip + ':' + self.port)
        self.stub = mobot_pb2_grpc.MobotStub(self.channel)

        signal.signal(signal.SIGINT, self.SignalHandler)

        self.attached = False

        self.bodystate = MobotState()

        self.chassis = Chassis(self.metadata["Chassis"], self.bodystate, self.stub, odometry_stream=False)
        self.accelerometer = Accelerometer(self.metadata["Accelerometer"], self.stub, stream=False)
        self.gyroscope = Gyroscope(self.metadata["Gyroscope"], self.bodystate, self.stub, stream=False)
        self.magnetometer = Magnetometer(self.metadata["Magnetometer"], self.bodystate, self.stub, stream=False)
        self.camera = Camera(self.metadata["Camera"], self.stub, stream=False)

    def start(self):
        self.AttachBody()
        self.chassis.start()
        self.accelerometer.start()
        self.gyroscope.start()
        self.magnetometer.start()
        self.camera.start()

    def AttachBody(self):
        try:
            attached = self.stub.AttachBody(mobot_pb2.Empty())
            if attached.success:
                self.attached = True
                print("Body Attached!")
            else:
                sys.exit("AttachBody request rejected by server!")
        except grpc.RpcError:
            sys.exit("AttachBody: Unable to Connect to server!")

    def DetachBody(self):
        try:
            detached = self.stub.DetachBody(mobot_pb2.Empty())
            if detached.success:
                print("Body Detached!")
            else:
                print("Need to restart the server!")
                sys.exit("DetachBody request rejected by server!")
        except grpc.RpcError:
            print("Need to restart the server!")
            sys.exit("DetachBody: Unable to Connect to server!")

    def SignalHandler(self, signum, frame):
        if self.attached:
            self.chassis.stop()
            self.accelerometer.stop()
            self.gyroscope.stop()
            self.magnetometer.stop()
            self.camera.stop()
            self.DetachBody()
        else:
            sys.exit()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def main():

    # TODO: Parse the arguments and the bodyfile
    # metadate: parameters of the mobot-body as a dict
    # args.ip: ip address as string
    # args.port: port number as string
    ############## Block Starts Here ##############
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bodyfile", help="Path to body yaml file", default="mobot_body.yaml")
    parser.add_argument("--ip", help="Ip address", default=get_ip_address())
    parser.add_argument("--port", help="Port", default="50051")
    args = parser.parse_args()
    try:
        with open(args.bodyfile, 'r') as bodyfile_fd:
            metadata = yaml.load(bodyfile_fd.read())
    except FileNotFoundError:
        print(f"File {args.bodyfile} not found!")
        return -1
    ############## Block Ends Here ##############

    mobot_body = MobotBody(metadata, args.ip, args.port)
    mobot_body.start()

if __name__ == '__main__':
    main()
