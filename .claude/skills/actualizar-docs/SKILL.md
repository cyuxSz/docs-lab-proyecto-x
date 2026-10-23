---
name: actualizar-docs
description: Valida y actualiza la wiki openwiki/ del repo contra el código actual. Úsala cuando pidan "actualizar la documentación", "validar la wiki", "revisar si los docs siguen siendo ciertos" o después de cambios grandes en src/.
argument-hint: "[validar | actualizar | desde <commit>]"
---

# Actualizar la wiki (openwiki/)

La wiki imita el formato de OpenWiki, pero la mantiene Claude Code sin API externa. El `README.md` raíz es el portal de la wiki: lleva citas como ella, las valida el mismo script y se actualiza con las mismas reglas (que siga siendo corto: estado, diagrama, tabla de paquetes y cómo correrlo). Antes de editar, lee `openwiki/INSTRUCTIONS.md`: ahí están el alcance y las reglas de citas.

Argumento: `validar` solo reporta, sin editar. `actualizar` (el valor por defecto) valida y corrige. `desde <commit>` usa ese commit como base en lugar del de `.last-update.json`.

## 1. Punto de partida
- Lee `openwiki/.last-update.json` → `commit`. Si no existe, toma como base el primer commit que tocó `openwiki/`.
- Lista lo que cambió desde ahí: `git diff --stat <commit>..HEAD -- src/` y `git log --oneline <commit>..HEAD`.

## 2. Validación mecánica
```bash
python tools/wiki_claims.py check
```
Cada línea que reporta es una cita que hay que revisar:
- `MOVIDA`: el código es idéntico pero cambió de lugar. Corre `python tools/wiki_claims.py check --fix-moved`; no hay que releer nada.
- `CAMBIADA`: las líneas citadas cambiaron. Abre el código y decide si la afirmación sigue siendo cierta.
- `FALTA` / `FUERA`: el archivo o las líneas ya no existen. Busca a dónde se movió la lógica (con `git log --follow` o grep).
- `NUEVA`: es una cita que aún no está registrada.

## 3. Validación semántica (lo que el script no ve)
El script solo detecta que el código citado cambió. Además revisa:
- **Diff sin citas:** en los archivos de `src/` del diff que ninguna página cita, busca nodos, topics, servicios, parámetros o launch nuevos o borrados y documéntalos en la página que corresponda.
- **Afirmaciones negativas:** frases como "nadie escucha X", "ningún launch lo carga" o "no se usa" se pueden volver falsas sin que cambien sus líneas citadas. Verifícalas con grep sobre todo `src/`.
- **Topics:** confirma que la tabla de `architecture/topics.md` coincide con todos los `create_publisher`, `create_subscription` y `create_service` de `src/`.
- **Diagramas:** confirma que el Mermaid de `architecture/overview.md` coincide con esa tabla. Si la topología cambió y existe `docs/arch/*.archify.json`, avisa que hay que regenerar el diagrama de Archify (skill `archify`).

En modo `validar`, detente aquí y entrega un reporte agrupado por página: qué afirmaciones siguen siendo ciertas, cuáles son falsas (con la cita que lo demuestra) y qué falta documentar.

## 4. Corregir
- Edita solo las páginas afectadas. Toda afirmación nueva lleva cita `[`archivo:línea`](ruta/relativa#Lx-Ly)`.
- Lo que no puedas verificar va como **Pregunta abierta**, no como hecho.
- Mueve a `operations/estado.md` lo que se vuelva obsoleto, y quita de ahí lo que ya se arregló.
- No reescribas páginas enteras si solo cambió un dato: el PR debe ser fácil de revisar.

## 5. Registrar
```bash
python tools/wiki_claims.py check       # debe terminar sin problemas, salvo las NUEVA que acabas de revisar
python tools/wiki_claims.py stamp       # se niega si quedan CAMBIADA, FALTA o FUERA
```
Si una CAMBIADA sigue siendo cierta sin editar su texto (por ejemplo, el código solo cambió de formato), usa `stamp --revisado`. Nunca uses `--revisado` sin haber leído el código citado: es la única forma de aprobar una afirmación falsa.
Escribe `openwiki/.last-update.json` así: `{"commit": "<git rev-parse HEAD>", "date": "<YYYY-MM-DD>", "by": "claude-code /actualizar-docs"}`.

## 6. Entregar
- Crea una rama `docs/wiki-<fecha>` y haz commit de `openwiki/`. No hagas push ni abras PR sin que el usuario lo pida.
- Resume en 3 a 6 líneas: cuántas afirmaciones se revisaron, cuáles cambiaron de verdadero a falso y qué páginas se tocaron.
