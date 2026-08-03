# Administration

This document describes installation and configuration of the software tools used to develop `Charlie`.
The standard setup, configuration and operational parameters are fully documented by Booster Robotics. See [K1 Product Manual](https://docs.booster.tech/docs/product-manual/k1/getting-started/overview/), [Booster Manual](https://booster.feishu.cn/wiki/E3q5wF5SnitXZgkY18Uc8odBnXb) and [Booster SDK](https://github.com/BoosterRobotics/booster_robotics_sdk). All software is provided under an open-source license.

![Charlie](/images/CharlieStanding.jpeg)
```                        ``Stand` Mode ```


***
## Table of Contents <a id="table-of-contents"></a>
  * [First Contact](#initialization)
  * [System Setup](#system)
  * [Software Development](#software)
    * [Booster Studio](#studio)
    * [Python](#python_ide)
    * [Docker](#docker_desktop)
***

## First Contact <a id="initialization"></a>
Neither of the MacOSX machines used for development have ethernet ports. Consequently the first contact must be made through the Android app and a Bluetooth connection. Using the app a wifi network connection can be configured. This, in turn, becomes the communication mode for the development system.

To check the firmware version:
``   cat /opt/booster/version.txt`

## System Setup <a id="system"></a>

This section describes the use of remote shell to login to the robot directly and to transfer code to the robot.

## Development System <a id="software"></a>
Code development is on a MacBookPro or iMac version Sequoia 15.7.4. The development scripts require that the root
of the `git` source tree be defined in `~/.bashrc` as, for example,
```   export CHARLIE_HOME=~/robotics/charlie ```

### Booster Studio <a id="studio"></a>
Booster Studio is the preferred development environment for robot custom agents. It is available at [Booster Studio](https://studio.booster.tech/#contact). There is a
 [Quick Start](https://docs.booster.tech/docs/product-manual/booster-studio/quick-start/download-install) document available.

### Python <a id="python_ide"></a>

Check for the latest version of Python at [python.org](https://www.python.org/downloads). The installed version must be 3.14.6 or greater.

Then install the following packages:
```
    python3 -m pip install boosteros
    python3 -m pip install boosteros[brain]    
```

We have chosen `PyCharm` as our Python editor. It can be downloaded from [here](https://https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=macM1) See [PyCharm Help](https://www.jetbrains.com/help/pycharm/).

### Docker <a id="docker_desktop"></a>
  Docker is used to create a test container for a virtual image of the robot. The install link is [here](https://www.docker.com/products/docker-desktop)
