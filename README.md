# Selfbalancing Robot Project 2019-02-23

The robot projects came to my mind as an introduction to mobile robotics and 
control theory. The robot is fully designed by my own and will stabilze it self 
once its finished.

## Status overview
2019-08 implementing `drivecontroller/` & `core/` modules..

2019-07 tested the controller code on the RPi

2019-02 first code for the controller implemented in robot.py

## Project directory
The projects is structured in modules which will be impleneted in diffrent steps.
```
sb-robot/
│
│
├── sb-robot/
│   ├── robot.py
│   ├── core/
│   │   ├── events.py
│   │   └── state.py
│   │
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
└── README.md
```
