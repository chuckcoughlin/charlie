# README
`Charlie` is a Booster K1 "kid-size" robot manufactured by Booster Robotics.

This repository contains personal modifications to the default robot configuration.
These customizations are documented in a set of guides where
the checked-in state of the guides roughly match the current state of the project.

See the [Admin](http://github.com/chuckcoughlin/charlie/tree/master/docs/admin.md) guide for a description of the
MacOSX development environment. Code is written against the *Booster Robotics* Python SDK within the
`BoosterStudio` tool.
Communication with the physical robot takes place over either wifi or *Bluetooth* connections.
Both a game controller and an *Android* tablet application are provided for operational control.

 A second guide, [Agent](http://github.com/chuckcoughlin/charlie/tree/master/docs/agents.md) describes a custom agent, `Irish`, that is made up of the following robot actions:
 * Countin - robot delays, then counts a 1,2,3 ... cadence as a precursor to a dance
 * Jig - this is an additional dance, an Irish jig
 * Stand - straighten the robot to attention
 * Bow - take a stage-appropriate bow
 * Wave - perform a celebratory gesture in the air
 * Chain - combine the preceding actions into a sequence for an integrated preformance

 Offline simulation and training procedures are described in [Training](http://github.com/chuckcoughlin/charlie/tree/master/docs/training.md).  Simulation via `Booster Studio` is used to test
 customizations before installation on the physical robot.
 Some features are developed using machine learning
 techniques. A second agent is trained in navigation and obstacle
 avoidance in a indoor setting using these techniques.

 ![Charlie](/images/CharlieSitting3.jpeg)
 ```                  Charlie in Study     ```
