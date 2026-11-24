# Guía de Construcción con IA — Versión 2 (`GUIA_IA2.md`)

> **Versión 2** ([mapa](../0_mapa_versiones.md)) · Rige la [constitución](../../1_constitution.md).

## 1. Estrategia de Generación en Dos Bloques
Debido a que la v2 incorpora **10 tablas completas** (60 endpoints nuevos y 10 pantallas con carga múltiple de catálogos para `<select>`), la generación con GitHub Copilot en modo Agent se divide en dos bloques secuenciales:
- **Bloque A:** `docente`, `grupo_investigacion`, `semillero`, `participa_grupo` y `participa_semillero`.
- **Bloque B:** `grupo_linea`, `semillero_linea`, `ac_linea`, `ods_linea` y `aa_linea`, más actualización de menús en `base.html` e `inicio.html`.

## 2. Puntos de Control Auditados
| Punto Auditado | Riesgo Detectado | Regla Aplicada en el Prompt |
| :--- | :--- | :--- |
| **Nombres con errata en el SQL dado** | Que Copilot escriba `universidad` o `nacionalidad` en el SQL `text()` causando error de columna inexistente. | Se instruyó usar `universidsad` y `nacionalidaad` en la consulta SQL y traducirlos a `universidad`/`nacionalidad` solo en el alias JSON de Pydantic. |
| **Inputs numéricos en lugar de `<select>`** | Que los formularios de Flask pidan digitar IDs manuales para las llaves foráneas. | Se exigió que `app.py` consulte los catálogos `GET` correspondientes antes de renderizar cada formulario y pinte etiquetas `<select>`. |
| **Llaves compuestas en tablas puente** | Ambigüedad al actualizar o eliminar registros en tablas de relación muchos-a-muchos. | Se estandarizó la ruta `/api/{tabla}/{fk1}/{fk2}` tanto en FastAPI como en `cliente_api.py`. |