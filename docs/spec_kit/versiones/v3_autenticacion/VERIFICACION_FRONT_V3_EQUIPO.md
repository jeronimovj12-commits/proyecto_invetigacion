# Verificación manual del front v3 — equipo

## Versión y entorno

- Rama: `verificacion-front-v3`, creada desde `origin/v3-desarrollo` actualizado.
- Commit de código probado: `90aaad8` (`Permite editar asignaciones sin borrar vínculos`).
- Arranque: `docker-compose.v3.yml`, con API en `127.0.0.1:8026`, front en `127.0.0.1:8079` y volumen PostgreSQL v3 separado de v2.
- Inicio observado: las imágenes se construyeron; `postgres-v3` quedó `Healthy`; `api-v3` y `front-v3` quedaron `Up`; `migrar-v3` terminó como proceso de una ejecución.
- Bootstrap: el usuario confirmó que terminó el asistente del primer administrador local. No se registran su nombre, correo ni contraseña.
- No se modificó código de producción ni se migraron los datos de v2.

## Resultado manual confirmado

| Recorrido | Resultado observado | Estado |
|---|---|---|
| Abrir `GET /login` en `http://127.0.0.1:8079/login` | `curl.exe` recibió HTTP 200. El log del front también registra `GET /login` con 200. | Confirmado |
| Login con la cuenta administradora recién creada | Al enviar el formulario, el navegador mostró `Bad Request` y «El formulario venció. Recarga la página e intenta de nuevo». El log registra `POST /login` con 400. La validación CSRF rechaza la solicitud antes de comprobar las credenciales; por tanto, este resultado no permite concluir si usuario y contraseña son correctos. | Bloqueado; repetir cuando se resuelva CSRF |

### Incidencia de preparación

Después de ejecutar `scripts/configurar_v3.ps1`, Compose indicó que faltaba `JWT_SECRET`. Se corrigieron localmente los saltos de línea de `v3-local.env` sin mostrar ni guardar sus secretos en Git; después las imágenes y contenedores iniciaron. La configuración local está ignorada por Git. Queda pendiente revisar el script de configuración para evitar que se repita este problema. No se editó el script durante esta verificación.

## Comprobaciones manuales pendientes

| Comprobación | Estado |
|---|---|
| Login correcto | Bloqueado por el 400 de CSRF descrito arriba; credenciales aún no validadas. |
| Login incorrecto y mensaje esperado | Pendiente. |
| Acceso directo sin sesión a inicio, investigación y administración | Pendiente. |
| Menú de administrador y operaciones administrativas | Pendiente. |
| Cuenta de consulta: lectura, ausencia de botones de escritura y rechazo de escrituras por URL directa | Pendiente. |
| Crear/editar/retirar usuarios, roles y asignaciones | Pendiente. |
| Logout, revocación y acceso posterior | Pendiente. |
| Vencimiento de sesión y presentación de mensajes de error | Pendiente. |

No se atribuyen capturas, resultados ni firmas que no se hayan observado o recibido. Las pruebas automáticas ya descritas en `VERIFICACION_V3.md` son evidencia técnica separada y no sustituyen este recorrido humano.

## Recorrido de demostración pendiente

Este guion explica qué se comprobará cuando el formulario de login funcione. Es una guía; los pasos todavía no se marcan como realizados.

1. **Administrador:** iniciar sesión y comprobar que aparecen los enlaces Usuarios, Roles y Asignaciones, además de las pantallas de investigación.
2. **Preparar consulta:** desde administración, crear un usuario de prueba, conservar el rol `consulta` creado por el bootstrap y asignarlo a ese usuario. No usar cuentas reales de compañeros.
3. **Permisos de consulta:** cerrar sesión, entrar con el usuario de prueba y comprobar que puede leer investigación, que no ve controles de escritura y que una visita directa a `/seguridad/usuarios` es denegada.
4. **Escrituras por URL:** con la cuenta consulta, intentar una operación de escritura desde una URL protegida; debe rechazarse y no modificar datos. Registrar el mensaje y el estado visible, sin capturar contraseñas ni tokens.
5. **Administración:** volver a entrar como administrador y comprobar crear, editar y retirar registros de usuarios, roles y asignaciones con datos de prueba. Verificar los mensajes y que las filas retiradas no se presenten como activas.
6. **Sesión:** cerrar sesión, volver a abrir una dirección protegida y comprobar que se solicita login. Para vencimiento, usar una duración local breve solo si se acuerda durante la prueba; anotar el tiempo configurado y el mensaje visible.
7. **Credenciales incorrectas y errores:** en el login, probar deliberadamente una contraseña incorrecta y observar el aviso. Probar mensajes de vencimiento y de servicio no disponible cuando corresponda, sin provocar cambios en datos oficiales.

La explicación sencilla para sustentar el recorrido es: primero se verifica quién entra; luego se compara lo que puede hacer una cuenta administradora con una cuenta de consulta; por último se cierra o deja vencer la sesión y se comprueba que las páginas protegidas vuelvan a exigir autenticación. Cada observación se añadirá aquí solo después de la confirmación del usuario.

