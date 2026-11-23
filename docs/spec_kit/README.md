# Índice explicativo de Spec Kit

Spec Kit organiza requisitos, decisiones, contratos y evidencia. La [guía de sustentación](../GUIA_EXPOSICION_PROYECTO.md) explica los archivos y un recorrido desde Flask hasta PostgreSQL.

## Orden de lectura

1. [Constitución](1_constitution.md): reglas comunes de capas, SQL, datos, secretos y trabajo por versiones.
2. [Mapa](versiones/0_mapa_versiones.md): alcance previsto; conserva estados históricos que deben contrastarse con evidencia reciente.
3. En cada versión, `2_spec` explica **qué**, `3_plan` **cómo**, `4_research` **por qué**, `5_data_model` **con qué datos** y `6_contracts` **qué intercambian front y API**.
4. `7_quickstart` indica **cómo arrancar/probar**, `8_tasks` **qué trabajo se sigue** y `9_checklist` **qué se revisa antes de aceptar**. En v1 el checklist revisa la especificación; los posteriores incluyen aceptación y pendientes.
5. `GUIA_IA*.md` registra ayuda y límites de IA. Verificación registra ejecuciones; no sustituirla por la existencia de código o casillas.

## Versiones

| Carpeta | Documentos para empezar | Cómo interpretar su estado |
|---|---|---|
| [v1_area_conocimiento/](versiones/v1_area_conocimiento/) | [Spec](versiones/v1_area_conocimiento/2_spec.md), [contratos](versiones/v1_area_conocimiento/6_contracts.md), [checklist](versiones/v1_area_conocimiento/9_checklist.md) | Ejemplo de un CRUD, no toda la v1 del módulo original. Sus archivos no certifican aceptación |
| [v2_claves_foraneas/](versiones/v2_claves_foraneas/) | [Spec](versiones/v2_claves_foraneas/2_spec.md), [contratos](versiones/v2_claves_foraneas/6_contracts.md), [checklist](versiones/v2_claves_foraneas/9_checklist.md) | Diez CRUD con FK; v2 sigue abierta. Evidencia: [VERIFICACION_V2.md](../../VERIFICACION_V2.md) |
| [v3_autenticacion/](versiones/v3_autenticacion/) | [Spec](versiones/v3_autenticacion/2_spec.md), [contratos](versiones/v3_autenticacion/6_contracts.md), [checklist](versiones/v3_autenticacion/9_checklist.md) | Autenticación, permisos y administración con pruebas registradas; no equivale a firmas/cierre |

## Arranque y evidencia actual

- [Quickstart v3](versiones/v3_autenticacion/7_quickstart.md): configuración, Docker aislado, bootstrap y migraciones nuevas/existentes. Compose predeterminado sigue siendo v2.
- [Verificación v3](versiones/v3_autenticacion/VERIFICACION_V3.md): resultados automáticos, entornos, limitaciones e historia diferenciada.
- [Tareas v3](versiones/v3_autenticacion/8_tasks.md): implementación y pendientes humanos.
- [Guía IA3](versiones/v3_autenticacion/GUIA_IA3.md): solicitudes y trabajo real, sin atribuir aceptación al profesor.

Los textos históricos pueden conservar comandos/estados superados. Para exponer, distinguir implementación, prueba automática, confirmación humana registrada y pendiente. Este índice no cambia requisitos ni da versiones por aceptadas.
