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

d_orig_x = -170.
d_orig_y = 122.
d_orig_z = 60.
dr = -20

d_scale = 10.

try:
    while True:
        data, addr = sock.recvfrom(1024)
        txt = data.decode('utf-8').strip()
        vals = txt.split(',')
        ix, iy, iz, ig = float(vals[0]), float(vals[1]), float(vals[2]), 'r' in vals[3]
        print(ix, iy, iz, ig)

        dx = d_orig_x + d_scale * ix
        dy = d_orig_y + d_scale * iy
        dz = d_orig_z + d_scale * iz
        '''
        d.wait_for_cmd(d.move_to(dx, dy, dz, dr))
        if ig != g_state:
            d.wait_for_cmd(d.grip(g_state))
            g_state = ig
        '''
except KeyboardInterrupt:
    print('Interrupted...')


d.wait_for_cmd(d.grip(False))
d.wait_for_cmd(d.suck(False))
d.close()

