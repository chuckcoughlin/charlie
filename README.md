# README
`Charlie` is a Booster K1 "kid-size" robot manufactured by Booster Robotics.


This repository contains personal customizations to the delivered robot software and configuration.
These customizations are described in a series of guides.

See [Admin](http://github.com/chuckcoughlin/charlie/tree/master/docs/admin.md) for a description of initial setup and configuration steps. It also describes the development environment on MacOSX, as well as build and deployment procedures. Communication between the development system and robot is accomplished though a wifi connection.

 A second guide, [Agents](http://github.com/chuckcoughlin/charlie/tree/master/docs/agents.md) describes a custom agent, `Irish`, that adds the following capabilities
 to the robot.
 * Bow - perform a stage-appropriate bow action.
 * Intro - robot delays, then counts a 1,2,3 ... cadence as a precursor to a dance
 * Jig - this is an additional dance, an Irish jig
 * Chain - combine a series of actions into a named list to be executed sequentially


 The [Acoustics](http://github.com/chuckcoughlin/charlie/tree/master/docs/acoustics.md) guide describes how to speak to the robot. It also describes methods for extension of the robot's vocabulary and speech patterns. Aside from some straightforward
 control commands, speech communication is forwarded to `ChatGPT` (with a configurable preamble).

 [Training](http://github.com/chuckcoughlin/charlie/tree/master/docs/training.md) describes training procedures for both direct and simulation training regimes. In
 particular, the inside of a house is simulated to be used as an environment for
 autonomous navigation by the robot in an indoor setting.

 ![Charlie](/images/CharlieSitting3.jpeg)
 ```                  Charlie in Study     ```
