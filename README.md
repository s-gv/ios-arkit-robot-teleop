ios-arkit-robot-teleop 
======================

Teleoperate a robot arm using the iPhone. This uses the Augmented Reality (ARKit) toolkit in iOS to track the 3D position of an iOS device in the room and moves the robot arm in lockstep. The iOS device sends out its position via UDP which is received on a PC / Mac to control the robot. This repo includes sample code to control the Kuka robot in the PyBullet simulation enivronment and the Dobot Magician robot arm.

How to use
----------

- Install the app on iPhone 6S or above.
- Swipe Left on the screen to set host IP.
- Tap to toggle the gripper.
- Swipe Right to send a command (does nothing right now).
- Run `pybullet_ios_teleop.py` on PC to teleoperate the Kuka robot in PyBullet.
- Run `dobot_ios_teleop.py` on PC connected to Dobot to teleoperate the Dobot.

Requirements
------------

- Python 2.7 or 3.6
- pybullet 2.2.2
- iOS >= 13
- Xcode 11.4
- pydobot 1.1.0
- Ubuntu 16.04 (might work on Mac too)

