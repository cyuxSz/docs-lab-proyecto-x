---
type: component
title: x_vision
owner: "@cyuxSz"
description: Detección con la cámara frontal.
---

# x_vision

## `detector` (en uso, incompleto)
- Declara `model_path` pero no carga ningún modelo ([`detector.py:14`](../../src/x_vision/x_vision/detector.py#L14), [`detector.py:21`](../../src/x_vision/x_vision/detector.py#L21)).
- Con cada imagen publica una detección fija: `label='gate'`, confianza 0.7 y la caja centrada en la mitad de la imagen ([`detector.py:22-25`](../../src/x_vision/x_vision/detector.py#L22-L25)).
- Como 0.7 ≥ 0.6 (umbral por defecto), publica en **cada** frame ([`detector.py:13`](../../src/x_vision/x_vision/detector.py#L13), [`detector.py:24`](../../src/x_vision/x_vision/detector.py#L24)). Por eso los pasos `search: gate` pasan siempre y los de `search: buoy` nunca.

## `camara_vieja` (obsoleto)
- Su comentario dice que ya no se usa, porque el driver publica directo en `/x/camera/image_raw` ([`camara_vieja.py:1-2`](../../src/x_vision/x_vision/camara_vieja.py#L1-L2)).
- Abre la cámara 0 con OpenCV y muestra una ventana; no es un nodo ROS ([`camara_vieja.py:6-14`](../../src/x_vision/x_vision/camara_vieja.py#L6-L14)).
- Sigue registrado como ejecutable ([`setup.py:20`](../../src/x_vision/setup.py#L20)). Si se borra el archivo, hay que borrar también esa línea.
