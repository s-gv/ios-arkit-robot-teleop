# Copyright (c) 2020 Sagar Gubbi. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import socket
import time
import math
import pybullet as p
import pybullet_data


p.connect(p.GUI)

#p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)
p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)
#p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=-89, cameraPitch=-75, cameraTargetPosition=[0.75, 0, 0])
p.resetDebugVisualizerCamera(cameraDistance=1.25, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[0.75, 0, 0])


p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)

plane_id = p.loadURDF("plane.urdf")
kuka_id = p.loadURDF("kuka_iiwa/model.urdf")

num_joints = p.getNumJoints(kuka_id)
kuka_end_effector_idx = 6

for t in range(100000):
    freq = 0.002
    target_pos = [0.45, 0.00 + 0.1*math.sin(2*3.14*freq*t), 0.35 + 0.1*math.cos(2*3.14*freq*t)]
    joint_poses = p.calculateInverseKinematics(kuka_id, kuka_end_effector_idx, target_pos)
    for j in range (num_joints):
        p.setJointMotorControl2(bodyIndex=kuka_id, jointIndex=j, controlMode=p.POSITION_CONTROL, targetPosition=joint_poses[j])
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()

