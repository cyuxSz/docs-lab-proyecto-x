---
type: reference
title: x_interfaces
description: Mensajes y servicio propios.
---

# x_interfaces

Genera dos mensajes y un servicio ([`CMakeLists.txt:6-11`](../../src/x_interfaces/CMakeLists.txt#L6-L11)).

- **`Waypoint`**: posición `geometry_msgs/Point`, `yaw` y `tolerance` ([`Waypoint.msg:1-3`](../../src/x_interfaces/msg/Waypoint.msg#L1-L3)). Ningún nodo lee `yaw` ni `tolerance`: `waypoint_follower` solo usa `position` ([`waypoint_follower.py:34`](../../src/x_navigation/x_navigation/waypoint_follower.py#L34)).
- **`Detection`**: `label`, `confidence` y una caja en píxeles ([`Detection.msg:1-7`](../../src/x_interfaces/msg/Detection.msg#L1-L7)).
- **`SetMission`** (servicio): recibe `mission_file` y responde `success` y `message` ([`SetMission.srv:1-4`](../../src/x_interfaces/srv/SetMission.srv#L1-L4)).
