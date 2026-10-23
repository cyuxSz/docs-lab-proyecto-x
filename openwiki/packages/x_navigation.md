---
type: component
title: x_navigation
owner: "@cyuxSz"
description: Convierte waypoints en setpoints suavizados.
---

# x_navigation

## `waypoint_follower` (en uso)
- Hasta tener waypoint y odometría no publica nada ([`waypoint_follower.py:31-32`](../../src/x_navigation/x_navigation/waypoint_follower.py#L31-L32)).
- El setpoint es un punto sobre la recta hacia el waypoint, a `lookahead` metros como máximo de la posición actual ([`waypoint_follower.py:35-42`](../../src/x_navigation/x_navigation/waypoint_follower.py#L35-L42)).
- Declara `max_speed` pero no lo usa en ningún cálculo ([`waypoint_follower.py:15`](../../src/x_navigation/x_navigation/waypoint_follower.py#L15)).
- No pasa orientación: el `PoseStamped` solo lleva posición, en el frame `odom` ([`waypoint_follower.py:39-42`](../../src/x_navigation/x_navigation/waypoint_follower.py#L39-L42)).

## `old_planner` (obsoleto)
- Su propio comentario dice que nadie lo lanza ([`old_planner.py:1-2`](../../src/x_navigation/x_navigation/old_planner.py#L1-L2)), y ningún launch lo incluye ([`sim.launch.py:11-14`](../../src/x_bringup/launch/sim.launch.py#L11-L14), [`real.launch.py:9-13`](../../src/x_bringup/launch/real.launch.py#L9-L13)).
- Publica metas aleatorias en `/planner/goal`, un topic que ningún nodo escucha ([`old_planner.py:13`](../../src/x_navigation/x_navigation/old_planner.py#L13), [`old_planner.py:18-20`](../../src/x_navigation/x_navigation/old_planner.py#L18-L20)).
- Sigue registrado como ejecutable ([`setup.py:20`](../../src/x_navigation/setup.py#L20)). Se puede borrar junto con esa línea.
