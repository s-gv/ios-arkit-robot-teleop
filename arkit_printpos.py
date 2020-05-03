# Copyright (c) 2020 Sagar Gubbi. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import socket

CLIENT_UDP_IP = "0.0.0.0"
UDP_PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((CLIENT_UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    txt = data.decode('utf-8').strip()
    print(txt)

