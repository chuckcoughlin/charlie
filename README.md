# README
`Charlie` is a Booster K1 "kid-size" robot manufactured by Booster Robotics.

This repository contains personal modifications to the default robot software and configuration.
These customizations are described in a series of guides.

See [Admin](http://github.com/chuckcoughlin/charlie/tree/master/docs/admin.md) for a description of the development environment. Python code is developed in a Docker environment
running on MacOSX. Communication with the physical robot
 takes place over a wifi connection.

 A second guide, [Agents](http://github.com/chuckcoughlin/charlie/tree/master/docs/agents.md) describes a custom agent, `Irish`, that adds the following actions
 to the robot.
 * Countin - robot delays, then counts a 1,2,3 ... cadence as a precursor to a dance
 * Jig - this is an additional dance, an Irish jig
 * Bow - perform a stage-appropriate bow action.
 * Chain - combine a series of actions into a named list to be executed sequentially


 The [Acoustics](http://github.com/chuckcoughlin/charlie/tree/master/docs/acoustics.md) guide describes how to speak to the robot. It also describes methods for extension of the robot's vocabulary and speech patterns.

 [Training](http://github.com/chuckcoughlin/charlie/tree/master/docs/training.md) describes simulation and training procedures. Simulation via `Booster Studio` is used to test
 customizations before installation on the physical robot.
 Some features are developed using machine learning
 techniques. In particular, navigation and obstacle
 avoidance in a indoor setting are developed using
 off-line training techniques.

 ![Charlie](/images/CharlieSitting3.jpeg)
 ```                  Charlie in Study     ```
