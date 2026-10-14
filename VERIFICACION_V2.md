# Verificación del borrador v2

Verificado en este entorno:
- Prueba de capas de v1: pasa.
- 12 pruebas de integridad y contratos con repositorio en memoria: pasan.
- Rutas HTTP de las diez tablas con servicios en memoria: pasan.
- Plantillas, formularios y selectores de las diez pantallas con HTTP simulado: pasan.
- Listados del front ante API no disponible: muestran aviso y lista vacía.

Pendiente: ejecución de SQL contra PostgreSQL real, prueba integrada con
Docker y revisión visual manual. El script pruebas/humo_v2.py está incluido
para realizar esta verificación en su equipo. No hay tag ni publicación remota.

Referencia: el init.sql no se modifica. Universidades y líneas están vacías
hasta cargar datos reales; la prueba integrada crea únicamente sus fichas de
prueba y las desactiva al terminar.
