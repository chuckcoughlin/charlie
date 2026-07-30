# Autonomous Operation

This document describes the process of implementing autonomous behavior in the robot. It describes both "hands-on" training and training via simulation.

One of Webots, Mujoco, or Isaac Sim is used as the simulation environment to guarantee proper walking dynamics before live mechanical engagement. This guide provides installation instruction for the simulation tool.

***************************************************************
## Table of Contents <a id="table-of-contents"></a>
 * [Robot](#robot)
    * [Setup](#setup_robot)
    * [Training](#speech)
    * [Installation](#speech)
 * [Simulation](#tablet)
   * [Setup](#speech_simulation)
   * [Training](#speech)
   * [Installation](#speech)

*********************************************************
## Robot <a id="robot"></a>
This section describes how to train the robot by repeated executions of a set of actions.
### a - Setup <a id="setup_robot"></a>

* ![green](/images/ball_green.png) ``System Scripts``  - Launch the robot code autonomously on system boot or standalone from the command-line.
- [x] bert-server start/stop: Start/stop the "headless" version of the robot code.
- [x] bert-standalone: Run the robot code from the command line. (Cannot be run simultaneously with daemon).
* ![green](/images/ball_green.png) ``Utility Applications``  - Exercise features independent of the robot
application. These are *python3* scripts.
- [x] dxl_scan: Show ids of all connected Dynamixel controllers. Verify that the discovery operation shows the correct motor ids within each serial device (*ttyACM0* and *ttyACM1*).
- [x] dxl_read: Read parameters of a servo motor. Access each individual motor. Verify that parameter settings match values in *bert.xml*.
- [x] dxl_write: Set volatile values for a given motor.
- [x] test-client: Connect via sockets to a running version of the robot. Type commands, receive responses.
interface for interactive testing.
- [x] test-server: Allow the tablet client to connect via sockets to a mock version of the robot. Accept commands, send responses.
interface for interactive testing. Note: when testing with the Android emulator connect the server to *localhost*, but configure
the emulator client as 10.0.2.2.


## Simulation <a id="simulation"></a>
Describe tests specifically for the Android tablet application called "BertSpeak"

[toc](#table-of-contents)<br/>
### a - Tablet Application <a id="bertspeak"></a>

The <b>Cover</b> page of the `BertSpeak` application shows a reclining picture of the robot and an audio visualizer. It also contains status buttons which show the
status of the connection to the robot, the states of speech
to text and of text to speech processing. The right-side slider adjusts the speaking volume.
The red button in the lower right corner kills the tablet application.

![Cover](/images/bertspeak_cover.png)


* ![yellow](/images/ball_yellow.png) ```Ignoring``` -
It can be annoying when the robot
attempts to interpret  background speech not directed  towards it.
(And usually fails).
The commands below place the tablet application into a state where it ignores ambient speech until specifically directed to be attentive. Note: The `cover` tab has a "Hearing" button that performs the same function.
  ```
      Bert, ignore me
      Bert, pay attention
  ```

The <b>Facial Recognition</b> page shows a view from the
forward-facing camera. A button press allows the user to
analyze the image for a human face.

![Facial Recognition](/images/bertspeak_facerec.png)

* ![green](/images/ball_green.png) ```Detecting``` - if a
face is detected, but is not known from a previous analysis,
the robot will query for a name and expect a response.
```
    What is your name
    my name is Chuck
```
* ![green](/images/ball_green.png) ```Greeting``` - if a
face is detected and matches a face previously analyzed,
the robot will send a greeting.
```
    Hi Chuck
```

This is the facial recognition page that
allows the robot to recognize whoever is handling the tablet.

![Animation](/images/bertspeak_animation.png)

* ![yellow](/images/ball_yellow.png) ```Animation```

This panel is planned to show the robot position
in real-time .

![Logging](/images/bertspeak_logs.png)

* ![yellow](/images/ball_yellow.png) ```Logging```

Validate that notifications and internal
application errors are logged to this panel.

![Settings](/images/bertspeak_settings.png)

* ![green](/images/ball_green.png) ```Settings```

There are a small number of configurable parameters
that are settable on this page.


![Transcript](/images/bertspeak_transcript.png)
* ![yellow](/images/ball_yellow.png) ```Transcript```

Validate that the tablet keeps a record of spoken commands and corresponding responses from the robot.
