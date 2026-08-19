# Administration

This document describes installation and configuration of the tools used to develop and deploy customizations for our Booster K1 robot, `Charlie`.
The standard setup, configuration and operational parameters are fully documented by Booster Robotics in several manuals. See [Documentation Center](https://docs.booster.tech).

![Charlie](/images/CharlieStanding.jpeg)
```                        ``Stand` Mode ```

***
## Table of Contents <a id="table-of-contents"></a>

  * [Development Tools](#tools)
    * [Booster Studio](#studio)
    * [Python](#python_ide)
    * [Docker](#docker_desktop)
  * [Direct Access](#commandline)
  * [Updates](#updates)
  * [Deployment](#deployment)
***

## Development Tools <a id="tools"></a>
Code development is on a MacBookPro or iMac version Tahoe 26.6.1.
The development scripts require that the root
of the `git` source tree be defined in `~/.zshrc` as, for example,
```   export CHARLIE_HOME=~/robotics/charlie ```

### Booster Studio <a id="studio"></a>
Booster Studio is the preferred development environment for robot custom agents.
It is available at [Booster Studio](https://studio.booster.tech/#contact).
There is a
 [Quick Start](https://docs.booster.tech/docs/product-manual/booster-studio/quick-start/download-install) document available. Under the `View` menu, open the `Command Palette` to list available actions with the studio.

### Python <a id="python_ide"></a>
Check for the latest version of Python at [python.org](https://www.python.org/downloads). The installed version must be 3.14.6 or greater. Install certificates as directed. Add `/Library/Frameworks/Python.framework/Versions/3.14.6/bin` to the `PATH` variable.

Then install the following packages:
```
    python3 -m pip install --upgrade pip
    python3 -m pip install boosteros
    python3 -m pip install boosteros[brain]
    python3 -m pip install booster_sdk_python --user   
```

We have chosen `PyCharm` as our Python editor. It can be downloaded from [here](https://https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=macM1) Configure the python interpreter as `/Library/Frameworks/Python.framework/Versions/3.14`. For additional assistance, see [PyCharm Help](https://www.jetbrains.com/help/pycharm/).

### Docker <a id="docker_desktop"></a>
  Docker is used to create a test container for a virtual image of the robot. The install link is [here](https://www.docker.com/products/docker-desktop)

## Direct Access <a id="commandline"></a>
  Neither of the MacOSX machines used for development have ethernet ports. Consequently the first contact must be made through the Android app using a Bluetooth connection. Using This app a wifi network connection can be configured. This, in turn, becomes the communication mode for the development system.

  ```
    ssh booster@10.0.0.245   (address visible on tablet application, password is initially 123456)
  ```

  To check the firmware version:
  ``   cat /opt/booster/version.txt`

  The current version is v1.6.2.2-release.global-02145-2026-06-03

## Updates <a id="updates"></a>
### Booster Studio
Help->Booster Studio - Check for Updates

## Software Deployment <a id="deployment"></a>
  This section describes the use of remote shell to login to the robot directly and to transfer code to the robot.
