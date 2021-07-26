# ROS helpers

This package contains some of my ROS helpers, it contains two nodes:

## Scan merger

Some Laser Scanners deliver multiple `LaserScan` messages per revolution,
this can be useful in some cases, but in others, we would like to have
the full scan in the same message. This node targets this.

## Gyro/Accelero merger

In RealSense D435i, the Gyroscope and Acceleration messages are published
separately, the RealSense node contains an option to unite these mesurements,
but in some cases, you might record a bag file without setting the unification
option. In such a case, this node can help.

-- Abdelhak BOUGOUFFA
