# README
`Charlie` is a Booster K1 "kid-size" robot manufactured by Booster Robotics.


This repository contains personal customizations to the delivered robot software and configuration.
These customizations are described in a series of guides. See [Admin](http://github.com/chuckcoughlin/charlie/tree/master/docs/admin.md) for a description of network settings and other configuration tasks. It also describes the development environment on MacOSX. Communication with the development system is accomplished though a wifi connection to the robot.

 A second guide, [API](http://github.com/chuckcoughlin/charlie/tree/master/docs/api.md) describes actions that are available over Bluetooth connections. Currently there are two devices that are supported: a robot controller that is delivered with the Booster K1 and an Android phone or tablet. The extensive API allows the user to set gait speed and direction and to execute stored moves. It provides accesss to high-speed edge processes, stereo depth visual data, microphone arrays, and real-time inference loop routines.

 The [Acoustics](http://github.com/chuckcoughlin/charlie/tree/master/docs/acoustics.md) guide describes how to speak to the robot. It also describes methods for extension of the robot's vocabulary and speech patterns. Aside from some straightforward
 control commands, speech communication is forwarded to `ChatGPT` (with a configurable preamble).

 [Auto](http://github.com/chuckcoughlin/charlie/tree/master/docs/auto.md) describes training procedures for both direct and simulation training regimes.


 ![Charlie](/images/CharlieSitting3.jpeg)
 ```                  Charlie in Study     ```
