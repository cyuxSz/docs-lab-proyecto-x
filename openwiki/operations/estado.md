---
type: reference
title: Estado real del código
description: Qué está en uso, qué está obsoleto y qué está a medias, con evidencia.
---

# Estado real del código

## Obsoleto (se puede borrar)
- `old_planner`: ningún launch lo ejecuta y publica en un topic sin suscriptores ([`old_planner.py:1-2`](../../src/x_navigation/x_navigation/old_planner.py#L1-L2), [`old_planner.py:13`](../../src/x_navigation/x_navigation/old_planner.py#L13)).
- `camara_vieja`: la reemplaza el driver de cámara ([`camara_vieja.py:1-2`](../../src/x_vision/x_vision/camara_vieja.py#L1-L2)).

## A medias (bloquea misiones reales)
| Problema | Efecto | Evidencia |
|---|---|---|
| El yaw recibe error 0 y x/y no se controlan | El sub solo cambia de profundidad | [`pid_controller.cpp:25-30`](../../src/x_control/src/pid_controller.cpp#L25-L30) |
| La misión avanza sin esperar a llegar | Los pasos `goto` se saltan en 0.5 s | [`mission_handler.py:58-60`](../../src/x_mission/x_mission/mission_handler.py#L58-L60) |
| El detector siempre devuelve `gate` | `search: buoy` nunca termina | [`detector.py:23`](../../src/x_vision/x_vision/detector.py#L23) |
| El `timeout` de `search` se ignora | La misión puede quedarse atorada | [`mission_handler.py:52-55`](../../src/x_mission/x_mission/mission_handler.py#L52-L55) |
| Los YAML de parámetros no se cargan | Cambiarlos no tiene efecto | [`sim.launch.py:11-14`](../../src/x_bringup/launch/sim.launch.py#L11-L14) |

## Campos o parámetros sin uso
- `Waypoint.yaw` y `Waypoint.tolerance` ([`Waypoint.msg:2-3`](../../src/x_interfaces/msg/Waypoint.msg#L2-L3)).
- `max_speed` en `waypoint_follower` ([`waypoint_follower.py:15`](../../src/x_navigation/x_navigation/waypoint_follower.py#L15)).
- `model_path` en `detector` ([`detector.py:14`](../../src/x_vision/x_vision/detector.py#L14)).
