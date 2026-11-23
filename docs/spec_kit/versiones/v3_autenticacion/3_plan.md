# Plan y resultado — v3

Actualizado: 9 de noviembre de 2026. V2 permanece abierta.

1. Auditar Git y documentación antes de editar: realizado; rama limpia v3-desarrollo con tres commits locales de autenticación conservados.
2. Conservar autenticación y bootstrap existentes: realizado; ampliar pruebas sin reemplazar bibliotecas ni políticas.
3. Proteger todas las rutas por identidad y permiso en API: realizado mediante middleware en main_v3; excepciones públicas explícitas.
4. Añadir administración por controlador, interfaz de servicio, servicio, interfaz de repositorio y SQL manual: realizado. Las bajas se serializan con lock antes de leer el estado, bajo READ COMMITTED; transacción revierte si se pierde el último administrador efectivo.
5. Integrar Flask por HTTP: realizado en arranque separado app_v3; sesión en servidor SQLite, cookie opaca firmada, CSRF, permisos de menú y URL, manejo de errores sin conservar datos de investigación ante caída.
6. Arranque reproducible: compose aislado, migración como dependencia obligatoria, secretos externos conservados y dependencias fijadas para v3. El Dockerfile conserva requirements.txt como opción predeterminada de v2.
7. Verificación: suites de autenticación, permisos sobre OpenAPI completo, CRUD, concurrencia, migración, Flask, recorrido integrado real y regresión de capas; evidencia en VERIFICACION_V3.md.
8. Publicar commits funcionales en origin/v3-desarrollo sin force, merge ni tags. La aceptación humana y cierre no forman parte de esta ejecución.

## Decisiones de integración

PUT/PATCH de rol_usuario cambia un par activo mediante retiro lógico y alta de
otro par en la misma transacción. La fila original conserva su clave e historial;
no se reactivan pares retirados. Un par sin cambios responde 200 sin mutaciones. No se expone activo
en peticiones administrativas; DELETE siempre es lógico. Los roles arbitrarios
pueden administrarse, pero solo administrador/consulta conceden permisos v3.
Los nombres de esos dos roles se conservan para evitar cambiar permisos al renombrar.

El front solo necesita Flask y requests. SQLite pertenece a la biblioteca estándar
y guarda sesiones locales; no datos del módulo. No se comparten variables globales
con JWT entre usuarios; cada solicitud recupera su token por identificador de sesión.
El volumen del front admite reinicios y múltiples procesos del mismo contenedor;
no se propone distribución de sesiones entre servidores para v4.

## Pendientes humanos

Revisión visual en navegador, prompt interactivo getpass, integración de aportes,
ratificación de enmiendas y firmas. Ninguna suite sustituye la aceptación del equipo.
