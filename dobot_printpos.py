# Copyright (c) 2020 Sagar Gubbi. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from pydobot import Dobot
import time

d = Dobot(port='/dev/ttyUSB0', verbose=False)

for _ in range(100):
    x, y, z, r = d.pose()[:4]
    print(f'x: {x}, y: {y}, z: {z}, r: {r}')
    time.sleep(0.1)

d.close()

