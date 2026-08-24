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
 * [General](#controllers)
 * [Countin](#countin)
 * [Jig](#jig)
 * [Bow](#bow)
 * [Chain](#chain)


*********************************************************
## General <a id="controllers"></a>
### Robot Controller
The controller is powered (on or off) by pressing the "home" button. "Led 4" is illuminated when contact with the robot is live.

![Charlie](/images/controller.jpeg)
```                  Controller     ```

The controller that is supplied with the robot is customizable.

### Android App
The Android application is customizable.
