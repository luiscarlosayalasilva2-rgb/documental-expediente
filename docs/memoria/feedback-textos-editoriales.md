---
name: feedback-textos-editoriales
description: "Video descriptions must have NO questions and NO AI/ficción disclosure line — overrides the master prompt's Bloque 5 rule."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 88e8cb85-2109-40fa-9c83-8d73ae67da87
  modified: 2026-10-16T01:11:25.501Z
---

In Bloque 5 descriptions (and TEXTOS_EDITORIALES) never include a question to the viewer and never include the line "Historia ficticia dramatizada · Ilustraciones generadas por IA · Narración con voz sintética" or any AI label. Keep exactly 3 emojis, keyword first.

**Why:** Luis said so on 2026-10-15 ("no pongas preguntas en la descripción y no pongas eso de IA"); it overrides §14 Bloque 5 / §27 of his master prompt.
**How to apply:** applies to every series. `testamento\src\editorial.py` already omits the declaration and flags any "?"/"¿". See [[sistema-produccion]], [[master-prompt-reflexion]].
