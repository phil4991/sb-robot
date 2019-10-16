# Selfbalancing Robot Project 2019-02-23

This robot project came to my mind as an introduction to mobile robotics and 
control theory. The robot is fully designed by myself and will stabilze and orientate itself 
once it's finished.

## Status overview
2019-10 implemented `motion/`, `daq/` & `core/` packages.. 
- Basic structure for sensordata acquisition is set up. 
- First control code will be added to the ´motion_suite.py´ module next

2019-08 implementing basic code for `motion/` & `core/` packages..

2019-08 implementing basic code for `motion/` & `core/` packages..

2019-07 tested the controller code on the RPi

2019-02 first code for the controller implemented in robot.py

## Project directory
The project is structured in packages which will be implemented in different steps
```
sb-robot/
│
├── src/
│   ├── robot1.py
│   ├── core/
│   │   ├── state.py
│   │   ├── events.py
│   │   └── helpers.py
│   │
│   ├── motion/
│   │   └── motion_suite.py
│   │
│   └── daq/
│       └── daq_suite.py
│
├── data/
│   ├── RTIMULib.ini
│   └── config.json
│
├── tests/
│   ├── fig/
│   ├── RTEllipsoidFit/
│   ├── daq_analysis.m
│   └── daq_IMU_test.py
│
├── .gitignore
└── README.md
```