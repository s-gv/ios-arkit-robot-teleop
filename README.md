dobot-arkit-teleop
==================

Teleoperate a Dobot Magician using the iPhone. This uses the Augmented Reality (ARKit) tools in iOS to track the 3D position of the iOS device in the room and moves the Dobot arm in lockstep.

How to use
----------

- Install the app on iPhone 6S or above.
- Swipe Left on the screen to set host IP.
- Tap to toggle the gripper
- Swipe Right to send a command (does nothing right now)
- Run `dobot_ios_teleop.py` on PC connected to dobot.

Requirements
------------

- Python 3.6
- iOS >= 13
- Xcode 11.4
- pydobot 1.1.0
- Ubuntu 16.04 (might work on Mac too)

