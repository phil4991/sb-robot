# Self Balancing Robot Project
This robot project came to my mind as an introduction to mobile robotics and 
control theory. The robot is fully designed by myself and will stabilze and orientate itself 
once it's finished.

## Status Quo
![text][robot_side] ![text][robot_front]


[robot_side]: https://github.com/phil4991/sb-robot/blob/doc-master/docs/images/robot_side.png "robot side with first two platforms"
[robot_front]: https://github.com/phil4991/sb-robot/blob/doc-master/docs/images/robot_front.png "robot front with first two platforms"

## Status overview
2020-05 updated code structure
- new configuration handling

2020-02 updated simulation model

2019-10 implemented `motion`, `daq` & `core` components.. 
- Basic structure for sensordata acquisition is set up. 

2019-08 implementing basic code for `motion` & `core` components..

2019-07 tested the controller code on the RPi

2019-02 first code for the controller implemented in robot.py

## Project directory
The project is structured in packages which will be implemented in different steps
```
sb-robot/
│
├── src/
│   ├── robot1.py
│   ├── config.yml
│   ├── core/
│   │   ├── configuration.py
│   │   ├── state.py
│   │   ├── events.py
│   │   └── helpers.py
│   │
│   ├── motion/
│   │   └── motion_suite.py
│   │
│   └── daq/
│       ├── daq_suite.py
│       └── sensors.py
│
├── data/
│   └── RTIMULib.ini
│
├── sim/
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
