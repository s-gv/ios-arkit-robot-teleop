# Copyright (c) 2020 Sagar Gubbi. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from pydobot import Dobot

d = Dobot(port='/dev/ttyUSB0', verbose=False)

d.wait_for_cmd(d.home())

d.close()


