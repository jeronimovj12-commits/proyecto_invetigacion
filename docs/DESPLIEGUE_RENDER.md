# Despliegue v3 en Render

El Blueprint está en [`render.yaml`](../render.yaml). La opción de costo cero usa
una base PostgreSQL gratuita y dos servicios web gratuitos. Para permitir que el
front gratuito llegue a la API, la API tiene URL pública; sus rutas de datos exigen
Bearer y la documentación OpenAPI se desactiva en Render. Ambos servicios usan
`PORT` y el front obtiene la URL pública de la API desde Render.

Es una instancia de demostración temporal. El API puede tardar cerca de un minuto
en despertar tras 15 minutos sin tráfico; el front espera hasta 75 segundos para
la llamada. Render borra los archivos del front al dormir o reiniciar, así que las
sesiones del navegador se invalidarán y habrá que iniciar sesión de nuevo. La base
PostgreSQL gratuita vence a los 30 días y no incluye backups; exportar datos antes
de esa fecha si se quieren conservar. Render documenta estas limitaciones en sus
[planes gratuitos](https://render.com/docs/free) y su [red privada](https://render.com/docs/private-network).

## Preparación y creación

1. Subir `v3-desarrollo` actualizado al remoto y revisar el commit de la rama.
2. En Render, crear un Blueprint desde ese repositorio y elegir `v3-desarrollo`.
   Elegir plan Free para API, front y PostgreSQL.
3. Confirmar que DB, API y front queden en la misma región (`ohio`). La API es
   pública en el nivel gratuito; no compartir su URL como interfaz de usuario.
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
ni crea el administrador inicial. El plan gratuito no ofrece Shell en el servicio.
Para crear el administrador, ejecutar el comando desde una copia local del repo,
con Python 3 y las dependencias v3 instaladas, usando el URL externo de PostgreSQL
copiado del panel de Render:

```powershell
$secureUrl = Read-Host 'URL externo temporal de PostgreSQL en Render' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureUrl)
try {
  $env:DB_POSTGRES = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
  Set-Location api_investigacion
  python -m comandos.crear_administrador
} finally {
  Remove-Item Env:\DB_POSTGRES -ErrorAction SilentlyContinue
  [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
}
```

El comando solicita usuario, correo y contraseña de forma interactiva y no
imprime la contraseña. Elegir una clave nueva para la demo; no reutilizar claves
locales. Luego entrar en `/login` desde el URL del servicio front.

El URL externo contiene credenciales: no guardarlo en archivos, historial de shell,
capturas o repositorio. El bloque anterior pide el URL oculto y lo retira del entorno
al terminar. Usar una contraseña demo nueva.

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
- La API pública responde al front; `/docs` y `/openapi.json` deben estar desactivados.
- Tras el reposo o reinicio del plan gratuito, iniciar sesión otra vez: las sesiones
  del front viven en almacenamiento temporal.
- Conservar copia de respaldo antes de toda carga manual. Nunca aplicar `init.sql`
  sobre una base con tablas o datos.
