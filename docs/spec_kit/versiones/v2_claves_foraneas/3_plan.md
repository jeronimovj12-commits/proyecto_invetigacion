# Plan de implementación de la v2

## Objetivo

Ampliar el módulo de investigación para consultar, crear, editar y desactivar registros de diez tablas desde la interfaz web. La API debe validar las relaciones entre registros antes de guardar los cambios en PostgreSQL.

## Etapas de trabajo

1. **Modelo de datos.** Identificar la clave de cada tabla y las referencias que necesita. Documentar qué registros deben existir antes de crear uno relacionado.
2. **API.** Implementar las operaciones de las diez tablas. Validar los campos obligatorios y rechazar referencias inexistentes o inactivas. Impedir que se desactive un registro del que dependan otros registros activos.
3. **Interfaz en Flask.** Conectar los listados y formularios con la API. Cargar desde la API las opciones de los desplegables y mostrar un aviso cuando el servicio esté fuera de línea.
4. **Pruebas.** Comprobar las reglas de integridad en memoria. Después, iniciar PostgreSQL, la API y la interfaz con Docker Compose y ejecutar la prueba integrada con fichas de prueba.
5. **Revisión y entrega.** Recorrer las diez pantallas en el navegador, comprobar sus formularios y desplegables, registrar los hallazgos y completar la documentación de la v2.

## Avance al 4 de noviembre de 2026

Las 12 pruebas en memoria pasaron. La prueba integrada con Docker y PostgreSQL también terminó correctamente. El resultado y el identificador de las fichas están en `VERIFICACION_V2.md`.

Quedan pendientes la revisión manual de las diez pantallas, los documentos faltantes y el cierre de la lista de verificación.