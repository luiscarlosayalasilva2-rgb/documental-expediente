---
name: velocidad-pipeline
description: Mediciones de velocidad del pipeline de series en la PC del usuario (i3-1215U, 7.7 GB RAM) y qué sí/no ayuda
metadata:
  type: project
---

PC: Intel i3-1215U (6 núcleos), 7.7 GB RAM (≈1 GB libre durante render), sin GPU dedicada (solo Intel UHD con Quick Sync).

- Montaje con libx264 `preset medium` ≈ 25 min/capítulo; con `veryfast` ≈ 14 min. Usar veryfast (ya está en restaurante\src).
- Quick Sync (h264_qsv): en una transcodificación pura de 60 s fue 2x más rápida (13 s vs 26 s) con SSIM igual (0.989 vs 0.990) pero archivos ~1.5x más grandes. En pasos con filtros (zoompan, subtítulos ass, overlay del banner) NO ayuda: son CPU-bound (zoompan 2.9 s vs 3.1 s; banner 96 s x264 vs 111 s qsv). Por eso queda apagado; se activa con env QSV=1 vía src\enc.py.
- Si la PC se duerme, el montaje se congela: pedir request_keep_awake al iniciar.
- Lo que más frenó el lote 2 fue la cuota de imágenes (ver [[series-cumple-regreso-restaurante]]), no la CPU. RAM 16 GB sería la mejora de hardware más útil.
- Solapar clips y montaje: restaurante\src\montar_al_vuelo.ps1 (no probado de punta a punta todavía; probar con la próxima serie).
