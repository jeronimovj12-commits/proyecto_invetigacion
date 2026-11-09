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

