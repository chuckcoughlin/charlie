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
***
## First Contact <a id="initialization"></a>
Neither of the MacOSX machines used for development have ethernet ports. Consequently the first contact must be made through the Android app and a Bluetooth connection. Using the app a wifi network connection can be configured. This, in turn, becomes the communication mode for the development system.

To check the firmware version:
``   cat /opt/booster/version.txt`

## System Setup <a id="system"></a>

This section describes the use of remote shell to login to the robot directly and to transfer code to the robot.

## Development System <a id="software"></a>
### Booster Studio <a id="studio"></a>

Booster Studio is the preferred development environment for robot custom agents. It is available at [Booster Studio](https://studio.booster.tech/#contact).
 [Booster Studio Quick Start](https://docs.booster.tech/docs/product-manual/booster-studio/quick-start/download-install)
