# Copyright (c) 2020 Sagar Gubbi. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import socket
from pydobot import Dobot

CLIENT_UDP_IP = "0.0.0.0"
UDP_PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((CLIENT_UDP_IP, UDP_PORT))

d = Dobot(port='/dev/ttyUSB0', verbose=False)
d.wait_for_cmd(d.suck(True))
d.wait_for_cmd(d.grip(False))

g_state = False

d_origin_x = 225.
d_origin_y = 0.
d_origin_z = 15.
dr = -20

d_scale = 300.

dx_min, dx_max = 180, 270
dy_min, dy_max = -110, 110
dz_min, dz_max = -30, 70

try:
    while True:
        data, addr = sock.recvfrom(1024)
        txt = data.decode('utf-8').strip()
        if txt.startswith(':'):
            continue
        vals = txt.split(',')
        ix, iy, iz, ig = float(vals[0]), float(vals[1]), float(vals[2]), 'r' in vals[3]
        print(ix, iy, iz, ig)

        dx = d_origin_x + d_scale * -iz
        dy = d_origin_y + d_scale * -ix
        dz = d_origin_z + d_scale * iy
       
        dx = dx_min if dx < dx_min else (dx_max if dx > dx_max else dx)
        dy = dy_min if dy < dy_min else (dy_max if dy > dy_max else dy)
        dz = dz_min if dz < dz_min else (dz_max if dz > dz_max else dz)
        
        d.wait_for_cmd(d.move_to(dx, dy, dz, dr))
        if ig != g_state:
            d.wait_for_cmd(d.grip(g_state))
            g_state = ig

        # Read and discard any buffered samples
        sock.setblocking(0)
        while True:
            try:
                _, _ = sock.recvfrom(1024)
            except BlockingIOError:
                break
        sock.setblocking(1)
except KeyboardInterrupt:
    print('Interrupted...')


d.wait_for_cmd(d.grip(False))
d.wait_for_cmd(d.suck(False))
d.close()

