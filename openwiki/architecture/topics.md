---
type: reference
title: Topics y servicios
description: Quién publica y quién escucha cada topic.
---

# Topics y servicios

| Topic / servicio | Tipo | Publica | Escucha |
|---|---|---|---|
| `/x/camera/image_raw` | `sensor_msgs/Image` | externo (`usb_cam` en real) | `detector` ([`detector.py:16`](../../src/x_vision/x_vision/detector.py#L16)) |
| `/x/vision/detections` | `x_interfaces/Detection` | `detector` ([`detector.py:17`](../../src/x_vision/x_vision/detector.py#L17)) | `mission_handler` ([`mission_handler.py:20`](../../src/x_mission/x_mission/mission_handler.py#L20)) |
| `/x/nav/waypoint` | `x_interfaces/Waypoint` | `mission_handler` ([`mission_handler.py:19`](../../src/x_mission/x_mission/mission_handler.py#L19)) | `waypoint_follower` ([`waypoint_follower.py:19`](../../src/x_navigation/x_navigation/waypoint_follower.py#L19)) |
| `/x/odom` | `nav_msgs/Odometry` | externo | `waypoint_follower` ([`waypoint_follower.py:20`](../../src/x_navigation/x_navigation/waypoint_follower.py#L20)), `pid_controller` ([`pid_controller.cpp:16-17`](../../src/x_control/src/pid_controller.cpp#L16-L17)) |
| `/x/control/setpoint` | `geometry_msgs/PoseStamped` | `waypoint_follower` ([`waypoint_follower.py:21`](../../src/x_navigation/x_navigation/waypoint_follower.py#L21)) | `pid_controller` ([`pid_controller.cpp:14-15`](../../src/x_control/src/pid_controller.cpp#L14-L15)) |
| `/x/thrusters/cmd` | `std_msgs/Float64MultiArray` | `pid_controller` ([`pid_controller.cpp:18`](../../src/x_control/src/pid_controller.cpp#L18)) | externo |
| `/x/mission/set` (servicio) | `x_interfaces/SetMission` | — | `mission_handler` ([`mission_handler.py:21`](../../src/x_mission/x_mission/mission_handler.py#L21)) |
| `/planner/goal` | `geometry_msgs/PoseStamped` | `old_planner` (obsoleto) ([`old_planner.py:13`](../../src/x_navigation/x_navigation/old_planner.py#L13)) | nadie |

En real, `usb_cam` se remapea a `/x/camera/image_raw` ([`real.launch.py:9`](../../src/x_bringup/launch/real.launch.py#L9)).
