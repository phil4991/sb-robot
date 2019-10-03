# Selfbalancing Robot Project 2019-02-23

This robot project came to my mind as an introduction to mobile robotics and 
control theory. The robot is fully designed by myself and will stabilze itself 
once it's finished.

## Status overview
2019-08 implementing `drivecontroller/` module..

2019-07 tested the first controller code with the new hardware on the RPi

2019-02 first code for the controller implemented in robot.py

## Project directory
The project is structured in packages which will be impleneted in different steps.
```
sb-robot/
│
│
├── sb-robot/
│   ├── robot.py
│   ├── drivecontroller/
│   │   ├── drivecontroller.py
│   │   └── helpers.py
│   │
│   └── sensorsystem/
│       ├── sensors.py
│       └── helpers.py
│
├── data/
│   └── config.json
│
├── tests/
│   ├── drivecontroller
│   │   ├── helpers_tests.py
│   │   └── drivecontroller_tests.py
│   │
│   └── sensorsystem/
│       ├── helpers_tests.py
│       └── sensors_tests.py
│
├── .gitignore
├── LICENSE
└── README.md
```
