---
type: guide
title: Quickstart
description: Orientación para quien llega nuevo al proyecto X.
---

# Quickstart

El proyecto X es un workspace ROS 2 para un vehículo submarino. Una misión escrita en YAML decide a dónde ir, navegación suaviza el camino y un PID mueve los thrusters. Visión aporta detecciones que hacen avanzar las misiones.

## Lo mínimo para correrlo
```bash
colcon build
source install/setup.bash
ros2 launch x_bringup sim.launch.py mission_file:=mission_test.yaml
```
- El launch de simulación arranca 4 nodos: `mission_handler`, `waypoint_follower`, `pid_controller` y `detector` ([`sim.launch.py:11-14`](../src/x_bringup/launch/sim.launch.py#L11-L14)).
- Si no se indica misión, usa `mission_test.yaml` ([`sim.launch.py:10`](../src/x_bringup/launch/sim.launch.py#L10)).
- No arranca simulador, cámara ni odometría: alguien más tiene que publicar `/x/camera/image_raw` y `/x/odom`. **Pregunta abierta:** ¿qué simulador se usa? No hay nada en el repo que lo lance.

## Qué leer según la tarea
| Si vas a… | Lee |
|---|---|
| Entender el flujo completo | [architecture/overview.md](architecture/overview.md) |
| Cambiar o agregar una misión | [packages/x_mission.md](packages/x_mission.md) |
| Tocar el control | [packages/x_control.md](packages/x_control.md) |
| Saber qué está roto u obsoleto | [operations/estado.md](operations/estado.md) |
| Configurar tu máquina | [operations/running.md](operations/running.md) |
