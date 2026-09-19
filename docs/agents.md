# Agents

The Application Programming Interface (API) defines commands that can be executed on the robot from a client device. Supported devices are the robot controller delivered with the Booster K1 or an Android tablet running the Booster Android application.
The devices communicate with the robot over a Bluetooth connection. The API is comprehensize and allows the user to set gait speed and direction and to execute stored moves. It provides accesss to high-speed edge processes, stereo depth visual data, microphone arrays, and real-time inference loop routines.
See [Developer Guide](https://docs.booster.tech/developer-guide). The robot version
must be at least v1.7.

This guide describes the custom agent, `Irish` which contains the following custom actions:
  * Countin - pause the robot and then issue a verbal cadence, "1,2,3 ..."
  * Jig - dance an Irish jig for 16 measures
  * Bow - execute a stage bow
  * Stand - bring the robot to attention
  * Wave - raise an arm in celebration
  * Chain - link the actions above into a single sequence


***************************************************************
## Table of Contents <a id="table-of-contents"></a>
 * [Controls](#controls)
 * [Countin](#countin)
 * [Jig](#jig)
 * [Bow, Stand, Wave](#bow)
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
```

#### Android App
The Android application is customizable.

## Bow, Stand, Wave <a id="bow"></a>
#### Easy Teach

Each of the `Bow`, `Stand` and `Wave` actions were created using the `Easy Teach`
feature of the live robot. This is available on the *Android* app under the
`Irish` agent, `Custom` tab and the "+" option.

For each of the three actions the developer positions limbs into an appropriate
series of timed poses that are recorded for later playback.

Once recordings were complete, the resulting
*.json* files was found in a subdirectory of
```
/opt/booster/booster_agent_data/data agent_storage
        /chuckcoughlin.charlie/orchestrations
```
and copied back onto the development machine. The recording
and custom action were then deleted from the live robot.

After this, the `BoosterStudio` *AI Assistant* was asked to generate Python code to
use the file in an agent that executed the recorded action.
Starting with a stub version of the `Stand.py` class with an empty *execute* method, then ...

```
   "Modify Stand.py to use data/stand.json to drive
    the robot motion. stand.json is the result of an
    Easy Teach session on the robot"
```
