## charlie
"Charlie" is a Booster K1 "kid-size" robot manufactured by Booster Robotics.


This repository contains personal customizations to the delivered robot software and configuration.
These customizations are described in a series of guides. See [Admin](http://github.com/chuckcoughlin/charlie/tree/master/docs/admin.md) for a description of network settings and other configuration tasks. These are accomplished though a wifi connection to the robot.

 A second guide, [API](http://github.com/chuckcoughlin/charlie/tree/master/docs/api.md) describes actions that are available via Python over Bluetooth connections. Currently there are two devices supports: a game console or Android phone or tablet. The API allows the user to set gait speed and direction and to execute stored moves.

 The [Acoustic](http://github.com/chuckcoughlin/charlie/tree/master/docs/acoustic.md) guide describes how to speak to the robot. It also describes methods for extension of the robot's vocabulary and  speech patterns.

 [Auto](http://github.com/chuckcoughlin/charlie/tree/master/docs/uauto.md) is the custom programming SDK in Python using the embedded NVIDIA Jetson Orin NX module. It manages high-speed edge processes, stereo depth visual data, microphone arrays, and real-time inference loop routines completely detached from external hardware. [Training](http://github.com/chuckcoughlin/charlie/tree/master/docs/user-guide.md) describes the off-line training environment.


 ![Charlie](/images/CharlieSitting3.png)
 ```                  Charlie in Lawn Chair     ```
