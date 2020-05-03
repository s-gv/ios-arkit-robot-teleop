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

d_origin_x = -170.
d_origin_y = 122.
d_origin_z = 60.
dr = -20

d_scale = 10.

try:
    while True:
        data, addr = sock.recvfrom(1024)
        txt = data.decode('utf-8').strip()
        vals = txt.split(',')
        ix, iy, iz, ig = float(vals[0]), float(vals[1]), float(vals[2]), 'r' in vals[3]
        print(ix, iy, iz, ig)

        dx = d_origin_x + d_scale * ix
        dy = d_origin_y + d_scale * iz
        dz = d_origin_z + d_scale * iy
        '''
        if dx > -180 and dx < 180 and dy > -180 and dy < 180 and dz > -10 and dz < 60:
            d.wait_for_cmd(d.move_to(dx, dy, dz, dr))
        if ig != g_state:
            d.wait_for_cmd(d.grip(g_state))
            g_state = ig
        '''

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

