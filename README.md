# proyecto-x

Software del sub X.

## Como correrlo
Primero cambia la ruta en `src/x_navigation/config/nav.yaml` a la de tu compu (dice /home/alberto).

```bash
colcon build
source install/setup.bash
ros2 launch x_bringup sim.launch.py
```

Si falla instala lo que te pida la terminal.

## WiP
- el planner viejo ya no se usa creo
- falta vision bien
- muchas cosas mas

## Documentación
La wiki está en [`openwiki/`](openwiki/index.md). Empieza por el [quickstart](openwiki/quickstart.md) o por el [estado real del código](openwiki/operations/estado.md).
Cada afirmación cita `archivo:línea`. Para validarla y actualizarla, usa `/actualizar-docs` en Claude Code.
