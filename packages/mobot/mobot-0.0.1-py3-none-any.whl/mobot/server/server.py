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

from concurrent import futures
import socket

import grpc

import mobot.proto.mobot_pb2_grpc as pb2_grpc
from .servicer import Servicer

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=30))
    
    pb2_grpc.add_MobotServicer_to_server(Servicer(), server)

    try:
        ip = get_ip_address()
    except:
        print("Not Connected to any network!")
        return
    port = "50051"
    server.add_insecure_port(f"{ip}:{port}")

    server.start()
    print(f"Mobot Server started at {ip}:{port}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
