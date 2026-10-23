---
type: component
title: x_bringup
description: Launch files.
---

# x_bringup

| Launch | Qué lanza | Estado |
|---|---|---|
| `sim.launch.py` | Los 4 nodos, con el argumento `mission_file` ([`sim.launch.py:10-14`](../../src/x_bringup/launch/sim.launch.py#L10-L14)) | En uso |
| `real.launch.py` | `usb_cam` más los mismos 4 nodos, con `mission_1.yaml` fija ([`real.launch.py:9-13`](../../src/x_bringup/launch/real.launch.py#L9-L13)) | Sin probar, según su comentario ([`real.launch.py:1-2`](../../src/x_bringup/launch/real.launch.py#L1-L2)) |

Ninguno de los dos pasa archivos de parámetros a los nodos; solo pasan `mission_file` ([`sim.launch.py:11`](../../src/x_bringup/launch/sim.launch.py#L11), [`real.launch.py:10`](../../src/x_bringup/launch/real.launch.py#L10)).
