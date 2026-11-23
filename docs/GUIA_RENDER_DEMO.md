# Demostración temporal de v3 en Render

Esta guía prepara una instancia independiente para mostrar v3 con una dirección
pública `onrender.com`. Render no abre el `localhost` del equipo: construye el código
desde una rama de Git y asigna URL a sus servicios web.

## Estado

La configuración está declarada en [`render.yaml`](../render.yaml), con imagen de API,
front y una base PostgreSQL separados. Render aún no ha desplegado esta configuración
desde este equipo, por lo que **todavía no existe una URL pública que compartir**.
Los cambios locales deben estar en GitHub en la rama `v3-desarrollo` antes de que
Render pueda leerlos. Esta guía no publica cambios ni crea recursos externos.

## Archivos que controlan el arranque

| Archivo | Para qué sirve |
|---|---|
| [`render.yaml`](../render.yaml) | Pide a Render dos servicios web gratuitos y una base PostgreSQL gratuita en Virginia. Genera secretos en Render; no contiene valores secretos. |
| [`api_investigacion/Dockerfile.render`](../api_investigacion/Dockerfile.render) | Construye la API para Render e incluye `psql` y los scripts de inicialización/migración. |
| [`front_flask/Dockerfile.render`](../front_flask/Dockerfile.render) | Construye el front v3 con Gunicorn como servidor WSGI, escucha en el puerto Render y mantiene separado el arranque v2. |
| [`front_flask/requirements-v3.lock`](../front_flask/requirements-v3.lock) | Fija Gunicorn junto con las dependencias de Flask para construir de forma repetible. |
| [`scripts/iniciar_api_render.sh`](../scripts/iniciar_api_render.sh) | Inicializa una base vacía de forma protegida, aplica migración v3 y escucha en el puerto asignado por Render. |
| [`scripts/preparar_db_render.sql`](../scripts/preparar_db_render.sql) | Inicializa `db/init.sql` solo si no hay tablas; si hay tablas parciales o inesperadas, se detiene sin reinicializar. Después aplica la migración v3. |
| [`api_investigacion/servicios/ensamblador.py`](../api_investigacion/servicios/ensamblador.py), [`servicios/ensamblador_seguridad.py`](../api_investigacion/servicios/ensamblador_seguridad.py) y [`servicios/ensamblador_autenticacion.py`](../api_investigacion/servicios/ensamblador_autenticacion.py) | Aceptan `DATABASE_URL` como alternativa a la variable local `DB_POSTGRES`. |
| [`api_investigacion/repositorios/conexion_postgresql.py`](../api_investigacion/repositorios/conexion_postgresql.py) | Adapta la URL administrada al controlador asyncpg y traduce `sslmode` a la opción TLS que entiende asyncpg. |
| [`scripts/crear_admin_render.ps1`](../scripts/crear_admin_render.ps1) | Desde Windows, construye una imagen local y crea el primer administrador con entrada oculta, conectándose a la URL externa de la base. Borra su archivo temporal al terminar. |

La API tiene URL pública en esta configuración gratuita porque los servicios web
gratuitos no pueden recibir solicitudes por la red privada de Render. La API mantiene
sus validaciones de sesión y permisos; el front la llama por HTTPS. PostgreSQL entrega
una dirección interna a los servicios. No se comparte la base local de v2.

## Publicar el proyecto

1. Abre la carpeta raíz del proyecto en Visual Studio Code. `render.yaml` está en esa
   carpeta; no abras solo `front_flask` o `api_investigacion`.
2. Conserva los cambios que ya tengas. Render necesita que los cambios de este trabajo
   estén confirmados en Git y publicados en GitHub en la rama `v3-desarrollo`. No subas
   `v3-local.env`, archivos `.env`, respaldos ni credenciales.
3. Inicia sesión en Render, selecciona **New → Blueprint**, conecta GitHub y escoge el
   repositorio y la rama `v3-desarrollo`.
4. Render lee `render.yaml`. Revisa los tres recursos y confirma que los planes mostrados
   sean gratuitos antes de aplicar el Blueprint. Si los nombres ya están ocupados en tu
   cuenta, cambia los nombres `investigacion-...-v3-demo` en ese archivo antes de subirlo.
5. Espera a que terminen la base y los dos despliegues. En el servicio `investigacion-api-v3-demo`,
   los registros deben mostrar la inicialización/migración y luego el servidor HTTP activo.
   La base gratuita debe estar lista antes de que la API pueda iniciar.
6. Abre la base PostgreSQL de Render y copia su **External Database URL** desde **Connect**.
   En una terminal PowerShell de Visual Studio Code, situada en la raíz del proyecto,
   ejecuta:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/crear_admin_render.ps1
   ```

   La URL se pega cuando el script la solicita con entrada oculta; no la escribas en un
   comando ni en un archivo versionado. Luego el comando pide nombre, correo y contraseña
   dos veces. Solo se puede crear el primer administrador si la base aún no tiene cuentas
   o roles iniciales. No es recuperación de acceso.
7. Después de crear la cuenta, abre la configuración de acceso de la base y retira cualquier
   regla amplia como `0.0.0.0/0`. La API y el front siguen usando la conexión interna de Render;
   el acceso externo solo hace falta para el alta inicial.
8. En el servicio `investigacion-front-v3-demo`, copia la URL pública que muestra Render y
   añade `/login`. Esa es la dirección para el profesor. No uses una URL supuesta: Render
   asigna el dominio real al crear el servicio.
9. Antes de compartirla, abre también la URL pública de `investigacion-api-v3-demo` desde
   Render y espera a que la raíz responda con el diagnóstico v3. Los servicios gratuitos
   pueden estar dormidos; la primera llamada del formulario al API tiene un tiempo límite
   de 75 segundos para permitir que la API gratuita despierte. Conviene abrir el
   front y la API antes de que el profesor inicie sesión.

El comando de administrador necesita Docker Desktop en el equipo local. La URL externa de
la base contiene credenciales, por eso el script la solicita oculta y la guarda solo de
forma temporal en la carpeta temporal de Windows. No publiques capturas de esa URL.

## Qué cambia en el entorno gratuito

- Los servicios web gratuitos se duermen tras 15 minutos sin tráfico y pueden tardar
  alrededor de un minuto en despertar. Conviene abrir el enlace antes de la sustentación.
- La base PostgreSQL gratuita tiene 1 GB y vence a los 30 días; Render da un periodo de
  gracia para actualizarla antes de eliminarla. No la uses como almacenamiento permanente.
- El front guarda sesiones en SQLite local. El entorno gratuito no ofrece disco persistente;
  si Render reinicia el front, el usuario tendrá que iniciar sesión otra vez.
- Render no ofrece Shell para servicios web gratuitos. El primer administrador se crea
  desde el equipo local con el script anterior, no mediante una ruta pública nueva.
- Los valores `JWT_SECRET` y `CLAVE_SESION` los genera Render. No los copies al repositorio.
- El servicio API es accesible desde Internet, pero no acepta operaciones protegidas sin
  una sesión válida y permisos asignados. La pantalla es el enlace que se comparte.

Estos límites corresponden a la modalidad gratuita actual y pueden cambiar. Revisa el
[detalle de los planes gratuitos de Render](https://render.com/docs/free) antes de crear
recursos. La guía no acredita un despliegue, una sesión de prueba ni una verificación
manual en Render.
