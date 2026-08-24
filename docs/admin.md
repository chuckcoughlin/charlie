# Administration

This document describes installation and configuration of the tools used to develop and deploy customizations for our Booster K1 robot, `Charlie`.
The standard setup, configuration and operational parameters are fully documented by Booster Robotics in several manuals. See [Documentation Center](https://docs.booster.tech).

![Charlie](/images/CharlieStanding.jpeg)
```
Chsrlie Standing
```

***
## Table of Contents <a id="table-of-contents"></a>

  * [Development Tools](#tools)
    * [Booster Studio](#studio)
    * [Docker](#docker_desktop)
    * [Python](#python_ide)
  * [Accessing the Robot](#commandline)
  * [Updates](#updates)
  * [Deployment](#deployment)
***

## Development Tools <a id="tools"></a>
Code development is on a MacBookPro or iMac version Tahoe 26.6.1.
`git` is the source code control system. We've defined
the root of the source tree in our environment as
```CHARLIE_HOME``` (*~/robotics/charlie*)

### Booster Studio <a id="studio"></a>
Booster Studio is the preferred development environment for robot custom agents.
It is available from [Booster Studio](https://studio.booster.tech/#contact).
See
 [Quick Start](https://docs.booster.tech/docs/product-manual/booster-studio/quick-start/download-install) for an initial description. Under the `View` menu, the *Command Palette* lists all actions available with the studio.

 ### Docker <a id="docker_desktop"></a>
   Docker is used to create a test container for a virtual image of the robot. The installation guide is [here](https://booster.feishu.cn/wiki/FlUUw1b7IiNxrFkBlnacGhvKnU). You will also be directed here if you attempt to connect to the virtual robot with `Docker` not installed.
   To install click on the "Virtual Robot" to trigger installation of the required resources into the container.

   Python is bundled inside the Docker container, including the *boosteros* and
   *booster_sdk_python* packages. The Python version is 3.10.

## Accessing the Robot <a id="commandline"></a>
  Neither of the MacOSX machines used for development have ethernet ports. Consequently the first contact must be made through the Android app using a Bluetooth connection. Using the app a wifi network connection can be configured for subsequent communication with the development system.

  ```
    # The host address is visible from the tablet pplication
    # The default password is: 123456
    ssh booster@10.0.0.245
  ```

## Updates <a id="updates"></a>
Software updates for the development system and internal robot are not necessarily released at the same time.

#### Booster Studio
When an update is available for `Booster Studio` a blue notice will appear in the top menu bar. Otherwise to check explicitly, see
`Help->Booster Studio - Check for Updates`.

#### Booster K1
The currently installed version is v1.7.2.0-release.00331-2026-07-28-global.

Instructions for firmare updates are available [here](https://docs.booster.tech/docs/product-manual/k1/firmware-version/check-version/). There are several ways to install an update. Perhaps the easiest is through `Firmware Upgrade` link on the `Settings` page in the Android app. Make sure both the tablet and robot are fully charged
before proceeding.

#### After Update
Connect to the robot using *ssh*.
```
  # Check the new firmware version
  cat /opt/booster/version.txt`

  # In firmware version v1.7, the `boosteros` package is not included.
  # Install it now. The python version must be >= 3.10.
  python3 --version
  python3 -m pip install --upgrade pip
  python3 -m pip install --upgrade --no-cache-dir \
                            boosteros==1.1.1 --user

  # Retrieve sample code
  boosteros-examples
  exit

  # On development system
  cd ${CHARLIE_HOME}
  rsync -r booster@10.0.0.245:/home/booster/boosteros_examples .

  ```

## Software Deployment <a id="deployment"></a>
  This section describes the process of installing our custom
  code to the robot.
