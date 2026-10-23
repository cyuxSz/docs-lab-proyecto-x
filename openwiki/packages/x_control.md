---
type: component
title: x_control
description: PID de profundidad y yaw hacia los 6 thrusters.
---

# x_control · `pid_controller` (C++)

- Tiene dos PID, uno de profundidad y otro de yaw, con ganancias tomadas de parámetros ([`pid_controller.cpp:12-13`](../../src/x_control/src/pid_controller.cpp#L12-L13)). La clase `Pid` es un PID clásico; la integral se acumula sin límite, es decir, **no tiene anti-windup** ([`pid.hpp:9-14`](../../src/x_control/include/x_control/pid.hpp#L9-L14)).
- Error de profundidad = `setpoint.z − odom.z` ([`pid_controller.cpp:25-26`](../../src/x_control/src/pid_controller.cpp#L25-L26)).
- **El yaw siempre recibe error 0**, así que su salida es 0 ([`pid_controller.cpp:27-28`](../../src/x_control/src/pid_controller.cpp#L27-L28)).
- La salida son 6 valores: los 4 primeros son yaw con signos alternados y los 2 últimos son *heave* ([`pid_controller.cpp:30`](../../src/x_control/src/pid_controller.cpp#L30)). **Pregunta abierta:** ¿qué thruster físico corresponde a cada índice?
- **Consecuencia:** el `x` y la `y` del setpoint no entran en ningún cálculo, así que hoy el sub solo sube y baja ([`pid_controller.cpp:25-30`](../../src/x_control/src/pid_controller.cpp#L25-L30)). Los pasos `goto` de las misiones no lo desplazan en horizontal.
- `config/pid.yaml` tiene las mismas ganancias que los valores por defecto ([`pid.yaml:3-8`](../../src/x_control/config/pid.yaml#L3-L8)), pero ningún launch lo carga (ver [running](../operations/running.md)).
