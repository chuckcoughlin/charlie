# Administration

This document describes installation and configuration of the tools used to develop and deploy customizations for our Booster K1 robot, `Charlie`.
The standard setup, configuration and operational parameters are fully documented by Booster Robotics in several manuals. See [Documentation Center](https://docs.booster.tech).

![Charlie](/images/CharlieStanding.jpeg)
```
Charlie Standing
```

***
## Table of Contents <a id="table-of-contents"></a>

  * [Development Tools](#tools)
    * [Booster Studio](#studio)
    * [Docker](#docker_desktop)
    * [Python](#python_ide)
  * [Accessing the Robot](#commandline)
  * [Logs](#logs)
  * [Updates](#updates)
  * [Deployment](#deployment)
***

## Development Tools <a id="tools"></a>
Code development is on a MacBookPro or iMac version Tahoe 26.6.1.
`git` is the source code control system. We've defined the robot IP
address and the root of the source tree as environment variables
to be used in several of our utility scripts.
```  
     BOOSTER      = booster@10.0.0.245
     CHARLIE_HOME = ~/robotics/charlie
```
### Booster Studio <a id="studio"></a>
Booster Studio is the preferred development environment for robot custom agents.
It is available from [Booster Studio](https://studio.booster.tech/#contact).
See
 [Quick Start](https://docs.booster.tech/docs/product-manual/booster-studio/quick-start/download-install) for an initial description. Under the `View` menu, the *Command Palette* lists all actions available with the studio.

 ### Docker <a id="docker_desktop"></a>
   Docker is used to create a testing container for a virtual image of the robot. The installation guide is [here](https://booster.feishu.cn/wiki/FlUUw1b7IiNxrFkBlnacGhvKnU). You will also be directed here if you attempt to connect to the virtual robot with `Docker` not installed.
   To install click on the "Virtual Robot" to trigger installation of the required resources into the container.

   Ubuntu and the Booster core is pre-configured inside the Docker container. Python is also bundled there including the *boosteros* and
   *booster_sdk_python* packages. The Python version is 3.10.

   execute
   ```
    docker ps
   ```
   Place the resulting id in *~/.zshrc*. Export as `DOCKER_ID`. This will be referenced in various utility
   scripts that access the virtual robot.

   To execute utilities within the Docker container, for example:
   ```
     docker exec -it ${DOCKER_ID} /bin/bash
   ```

## Accessing the Robot <a id="commandline"></a>
  Neither of the MacOSX machines used for development have ethernet ports. Consequently the first contact must be made through the Android app using a Bluetooth connection. Using the app a wifi network connection can be configured for subsequent communication with the development system. The robot IP address is visible from the tablet application.
  The default password is: 123456

  ```
    ssh booster@10.0.0.245
  ```
  To setup password-free access, on the development machine:
  ```
    ssh-keygen -t ed25519
    ssh-copy-id booster@10.0.0.245
  ```

## Logs <a id="logs"></a>
Operational logs are available. `ssh` onto the robot and execute:
```
   booster-cli log -st YYYYMMDD-hhMMSS -et YYYYMMDD-hhMMSS \
                       -o /home/booster/Documents/logs.zip
```
Alternatively use the script `view_logs.sh` to list log entries generated within the last hour.

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
