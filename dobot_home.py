from pydobot import Dobot

d = Dobot(port='/dev/ttyUSB0', verbose=False)

d.wait_for_cmd(d.home())

d.close()


