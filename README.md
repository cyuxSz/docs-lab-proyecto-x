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

## Arquitectura (Archify)

Diagrama interactivo de nodos y topics: [`docs/arch/arquitectura-proyecto-x.html`](docs/arch/arquitectura-proyecto-x.html).
GitHub muestra el HTML como código: descárgalo (botón *Download raw file*) y ábrelo en el navegador.
Fuente editable: [`docs/arch/arquitectura-proyecto-x.archify.json`](docs/arch/arquitectura-proyecto-x.archify.json).
