import socket
import time
import math
import pybullet as p
import pybullet_data

CLIENT_UDP_IP = "0.0.0.0"
UDP_PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((CLIENT_UDP_IP, UDP_PORT))

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

scale = 0.5
tx_min, tx_max = 0.45, 0.55
ty_min, ty_max = -0.2, 0.2
tz_min, tz_max = 0.35, 0.55

while True:
    data, addr = sock.recvfrom(1024)
    txt = data.decode('utf-8').strip()
    if txt.startswith(':'):
        continue
    vals = txt.split(',')
    ix, iy, iz, ig = float(vals[0]), float(vals[1]), float(vals[2]), 'r' in vals[3]
    print(ix, iy, iz, ig)
    
    tx = 0.5 + scale * iz
    ty = 0.0 + scale * ix
    tz = 0.45 + scale * iy
   
    tx = tx_min if tx < tx_min else (tx_max if tx > tx_max else tx)
    ty = ty_min if ty < ty_min else (ty_max if ty > ty_max else ty)
    tz = tz_min if tz < tz_min else (tz_max if tz > tz_max else tz)

    target_pos = [tx, ty, tz]

    joint_poses = p.calculateInverseKinematics(kuka_id, kuka_end_effector_idx, target_pos)
    for j in range (num_joints):
        p.setJointMotorControl2(bodyIndex=kuka_id, jointIndex=j, controlMode=p.POSITION_CONTROL, targetPosition=joint_poses[j])
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()

