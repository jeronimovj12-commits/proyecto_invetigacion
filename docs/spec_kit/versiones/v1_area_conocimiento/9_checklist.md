# Lista de Chequeo — Versión 1 (Compuerta 3)

- [x] **Claridad:** Todos los RF tienen códigos HTTP y valores concretos; sin `[NECESITA ACLARACIÓN]`.
- [x] **Completitud:** Cubre las 6 tablas sin FK (`area_conocimiento`, `objetivo_desarrollo_sostenible`, `area_aplicacion`, `termino_clave`, `universidad`, `linea_investigacion`).
- [x] **Coherencia:** Los tipos en `5_data_model.md` coinciden exactamente con `db/init.sql`.
- [x] **Alcance:** No se nombra ninguna tabla de v2 (FK) ni de v3 (seguridad/JWT).
- [x] **Secretos y Marca:** `.env` fuera de git con `.env.example` presente; paleta UMV en `marca.css` sin CDN externos.
- [x] **Separación Front/API:** `front_flask/requirements.txt` solo contiene `flask` y `requests`.

**Veredicto:** 🟢 En verde — Autorizado para generar código de Versión 1.