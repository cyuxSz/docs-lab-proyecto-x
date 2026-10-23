---
type: guide
title: Correrlo y configurarlo
description: Compilar, lanzar y parámetros.
---

# Correrlo y configurarlo

```bash
colcon build
source install/setup.bash
ros2 launch x_bringup sim.launch.py mission_file:=mission_1.yaml
ros2 service call /x/mission/set x_interfaces/srv/SetMission "{mission_file: mission_test.yaml}"
```

## Archivos de configuración: hoy no se cargan
Los YAML de `config/` se instalan (por ejemplo en navegación, [`setup.py:13`](../../src/x_navigation/setup.py#L13)), pero `sim.launch.py` no se los pasa a los nodos ([`sim.launch.py:11-14`](../../src/x_bringup/launch/sim.launch.py#L11-L14)). Cada nodo corre con los valores por defecto del código:

| Archivo | Valor en YAML | ¿Tiene efecto? |
|---|---|---|
| `x_navigation/config/nav.yaml` | `log_dir: /home/alberto/x_logs` ([`nav.yaml:6`](../../src/x_navigation/config/nav.yaml#L6)) | No. Además, `waypoint_follower` ni siquiera declara `log_dir` ([`waypoint_follower.py:15-16`](../../src/x_navigation/x_navigation/waypoint_follower.py#L15-L16)) |
| `x_vision/config/vision.yaml` | `model_path: /home/alberto/...` ([`vision.yaml:3`](../../src/x_vision/config/vision.yaml#L3)) | No, y el modelo tampoco se usa |
| `x_control/config/pid.yaml` | ganancias ([`pid.yaml:3-8`](../../src/x_control/config/pid.yaml#L3-L8)) | No, pero coinciden con los valores por defecto |

El README actual pide cambiar `/home/alberto` en `nav.yaml`. Con el launch actual ese cambio no tiene ningún efecto.
