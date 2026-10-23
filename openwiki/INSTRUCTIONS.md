# Instrucciones de la wiki

Esta carpeta imita el formato de [OpenWiki](https://github.com/langchain-ai/openwiki), pero la escribe y la actualiza Claude Code desde una sesión (skill `/actualizar-docs`), sin una API de pago.

## Alcance y prioridades
1. Qué nodos corren, qué topics y servicios intercambian y quién lanza cada cosa.
2. Qué está en uso, qué está obsoleto y qué está a medias: la información que hoy solo vive en la cabeza de alguien.
3. Cómo correrlo y qué hay que cambiar en la máquina de cada quien.

## Reglas
- Cada afirmación sobre el código lleva al menos una cita `archivo:línea` enlazada con ancla `#Lx` o `#Lx-Ly`.
- Lo que no se pueda citar se escribe como **pregunta abierta**, no como hecho.
- `tools/wiki_claims.py` guarda el hash de cada cita en `.claims/claims.json`. El workflow `wiki-claims` falla si el código citado cambió y la wiki no se actualizó.
- No se documentan cosas obvias del framework (cómo funciona ROS 2); solo cómo lo usa este repo.
