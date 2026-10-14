# Instalar y verificar el borrador v2

1. En su clon existente y sin cambios pendientes: `git switch -c v2-desarrollo`.
2. Copiar las carpetas del paquete de cambios sobre la raíz del clon.
   La raíz contiene docker-compose.yml, api_investigacion, front_flask y db.
3. Ejecutar `docker compose up -d --build`. No borrar el volumen PostgreSQL.
4. Abrir http://localhost:8025/ (version v2), http://localhost:8025/docs
   y http://localhost:8078/ (las diez pantallas nuevas).
5. Pruebas sin base:
   `docker compose exec api-investigacion python pruebas/prueba_capas.py`
   `docker compose exec api-investigacion python pruebas/prueba_v2.py`
6. Prueba real de las diez tablas:
   `docker compose exec api-investigacion python pruebas/humo_v2.py`
   Utiliza fichas marcadas como pruebas y las deja inactivas. En caso de
   fallo, imprime el caso y se detiene; no modifica registros oficiales.
7. Revisar manualmente las opciones, errores y los dos botones de guardar.

No se debe declarar terminada la v2 solo porque estas pruebas de capas pasan.
También se deben ejecutar la prueba integrada y la revisión visual en Docker.
