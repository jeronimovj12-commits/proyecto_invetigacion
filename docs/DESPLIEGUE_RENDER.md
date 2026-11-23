# Despliegue v3 en Render

El Blueprint está en [`render.yaml`](../render.yaml). Define una base PostgreSQL,
una API privada y el front Flask público. El front usa `PORT`, y conserva sus
sesiones SQLite bajo `/var/data` en un disco persistente de una sola instancia.
La API recibe `DATABASE_URL` desde Render como `DB_POSTGRES`; el repositorio
convierte el esquema estándar a `postgresql+asyncpg`.

## Preparación y creación

1. Subir `v3-desarrollo` actualizado al remoto y revisar el commit de la rama.
2. En Render, crear un Blueprint desde ese repositorio y elegir `v3-desarrollo`.
   Revisar los recursos y el costo que muestra el panel antes de confirmar.
3. Confirmar que DB, API y front queden en la misma región (`ohio`). El endpoint
   público es solo el front; la API es privada.
4. Render genera `JWT_SECRET` y `CLAVE_SESION`. No copiar `v3-local.env` ni poner
   contraseñas en este archivo. Las claves locales se quedan fuera del repo.

## Base de datos e inicialización

Al arrancar, `comandos/preparar_render.py` cuenta las tablas del esquema `public`.
Solo si no hay ninguna tabla corre `db/init.sql`. Si ya hay tablas, lo omite y
jamás permite que el script destructivo las recree. Después aplica la migración
v3, que valida el esquema antes de cambiarlo y conserva filas existentes. Si la
migración no es compatible, el servicio no inicia: investigar antes de reparar;
no borrar la base ni volver a ejecutar `init.sql` manualmente.

Esto automatiza el primer esquema de una base vacía. No copia los datos locales
ni crea el administrador inicial. Después del primer deploy, abrir una consola
interactiva del servicio API y ejecutar:

```sh
python -m comandos.crear_administrador
```

El comando solicita usuario, correo y contraseña de forma interactiva y no
imprime la contraseña. Elegir una clave nueva para la demo; no reutilizar claves
locales. Luego entrar en `/login` desde el URL del servicio front.

La base configurada usa un plan pagado de entrada para que no venza como una
instancia gratuita. El front también necesita plan pagado por su disco persistente;
Render requiere ese disco porque el almacén de sesiones actual es SQLite. El costo
final y los límites deben confirmarse en la pantalla del Blueprint antes de crear.

## Datos de demostración

`init.sql` incluye los catálogos base, no los registros de ejemplo de universidad,
docente, líneas, grupos y semilleros. Para una demo académica, usar las cargas
opcionales descritas en [quickstart v3](spec_kit/versiones/v3_autenticacion/7_quickstart.md)
solo sobre esta base recién creada y tras revisar su contenido. Las cargas pueden
rechazar conflictos; no forzarlas ni editar los datos existentes para hacerlas pasar.
Crear y probar la cuenta demo desde el front/API, nunca copiando el administrador
local. No publicar usuarios o contraseñas reales.

## Verificación posterior

- `/login` responde 200; abrir el formulario en un navegador real y completar CSRF,
  login de administrador, login de consulta, permisos, logout y expiración.
- La API privada responde al front; no abrir `/docs` públicamente.
- Reiniciar el front y confirmar que la sesión se invalida o continúa según el TTL
  guardado, y que el archivo permanece en `/var/data`.
- Conservar copia de respaldo antes de toda carga manual. Nunca aplicar `init.sql`
  sobre una base con tablas o datos.
