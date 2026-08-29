# Agents

The Application Programming Interface (API) defines commands that can be executed on the robot from a client device. Supported devices are the robot controller delivered with the Booster K1 or an Android tablet running the Booster Android application.
The devices communicate with the robot over a Bluetooth connection. The API is comprehensize and allows the user to set gait speed and direction and to execute stored moves. It provides accesss to high-speed edge processes, stereo depth visual data, microphone arrays, and real-time inference loop routines.
See [Developer Guide](https://docs.booster.tech/developer-guide). The robot version
must be at least v1.7.

This guide describes the custom agent, `Irish` which contains the following custom actions:
  * Countin - pause the robot and then issue a verbal cadence, "1,2,3 ..."
  * Jig - dance an Irish jig for 16 measures
  * Bow - execute a stage bow
  * Chain - link the 3 actions above into a single sequence


***************************************************************
## Table of Contents <a id="table-of-contents"></a>
 * [Controls](#controls)
 * [Countin](#countin)
 * [Jig](#jig)
 * [Bow](#bow)
 * [Chain](#chain)


*********************************************************
## Controls <a id="controls"></a>
#### Robot
The `F1` button on the robot's shoulder is re-programmed so that it's press triggers the Irish agent's fixed sequence of
actions: `Countin`,`Jig` and `Bow`. The robot mode must be `WALKING`, otherwise nothing will happen.


#### Controller
The joystick control is powered (on or off) by pressing the "home" button. "Led 4" is illuminated when contact with the robot is live.

![Charlie](/images/controller.jpeg)
```                  Joystick Control  ```

With the robot in `WALKING` mode press `L2 + R2 + DOWN` to enter the `Irish` agent.

| Agent | <center>Actions</center> |<center>Buttons</center>
| :------: | :---------------------- | :----------: |
| Irish | Countin | A |
| | Jig | B |
| | Bow | X |
| | Chain | Y |


#### Android App
The Android application is customizable.
