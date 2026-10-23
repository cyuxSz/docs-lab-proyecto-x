---
type: component
title: x_mission
description: Máquina de estados que recorre las misiones en YAML.
---

# x_mission · `mission_handler`

## Qué hace
- Al arrancar carga el archivo del parámetro `mission_file`, `mission_1.yaml` por defecto en el nodo ([`mission_handler.py:22`](../../src/x_mission/x_mission/mission_handler.py#L22)). El launch de simulación lo sobrescribe con `mission_test.yaml` ([`sim.launch.py:10-11`](../../src/x_bringup/launch/sim.launch.py#L10-L11)).
- Busca el archivo en `share/x_mission/missions/` del paquete instalado ([`mission_handler.py:26`](../../src/x_mission/x_mission/mission_handler.py#L26)), así que tras agregar una misión hay que volver a correr `colcon build`.
- El servicio `/x/mission/set` carga otra misión ([`mission_handler.py:32-38`](../../src/x_mission/x_mission/mission_handler.py#L32-L38)), y al cargarla el índice vuelve a 0 ([`mission_handler.py:29`](../../src/x_mission/x_mission/mission_handler.py#L29)).

## Tipos de paso
| `type` | Efecto | Cita |
|---|---|---|
| `dive` | Publica un waypoint solo con `z = depth` | [`mission_handler.py:48-49`](../../src/x_mission/x_mission/mission_handler.py#L48-L49) |
| `goto` | Publica un waypoint en `x, y, z` | [`mission_handler.py:50-51`](../../src/x_mission/x_mission/mission_handler.py#L50-L51) |
| `search` | No publica nada; avanza cuando la última detección tiene ese `label` | [`mission_handler.py:52-55`](../../src/x_mission/x_mission/mission_handler.py#L52-L55) |
| `surface` | Publica un waypoint con `z = 0` | [`mission_handler.py:56-57`](../../src/x_mission/x_mission/mission_handler.py#L56-L57) |

## Ojo
- `dive`, `goto` y `surface` avanzan al siguiente paso en el mismo tick en que publican, sin esperar a que el sub llegue ([`mission_handler.py:58-60`](../../src/x_mission/x_mission/mission_handler.py#L58-L60)). Con un tick cada 0.5 s, una misión de 5 pasos sin `search` se "termina" en unos 2.5 s.
- El `timeout` de los pasos `search` en el YAML ([`mission_1.yaml:4`](../../src/x_mission/missions/mission_1.yaml#L4)) no se lee en ningún lado: si la detección no llega, la misión se queda en ese paso para siempre ([`mission_handler.py:52-55`](../../src/x_mission/x_mission/mission_handler.py#L52-L55)).

## Misiones disponibles
- `mission_1.yaml`: compuerta y boya ([`mission_1.yaml:1-7`](../../src/x_mission/missions/mission_1.yaml#L1-L7)). Hoy se queda atorada en el paso `search: buoy` ([`mission_1.yaml:6`](../../src/x_mission/missions/mission_1.yaml#L6)), porque `detector` solo publica `gate` (ver [x_vision](x_vision.md)).
- `mission_test.yaml`: cuadrado de 2 m a 0.5 m de profundidad, sin pasos `search` ([`mission_test.yaml:1-7`](../../src/x_mission/missions/mission_test.yaml#L1-L7)).
