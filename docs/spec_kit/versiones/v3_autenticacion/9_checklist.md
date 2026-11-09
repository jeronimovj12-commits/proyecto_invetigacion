# Checklist de revisión — v3

9 de noviembre de 2026. Evidencia: [VERIFICACION_V3.md](VERIFICACION_V3.md).
Las casillas técnicas acreditan automatización; las humanas siguen abiertas.

- [x] Login válido/inválido/inactivo y contraseñas Argon2id sin hash en respuestas.
- [x] Firma, algoritmo, claims y vencimiento verificados; sin renovación automática.
- [x] Logout global atómico, concurrente y persistente tras reinicio.
- [x] Primer administrador transaccional, sin predeterminados, conflicto seguro y rechazo de entrada sin terminal.
- [x] Usuarios, roles y asignaciones con retiro lógico; pares retirados no reactivables.
- [x] Último administrador conservado al retirar cuenta, rol o asignación; concurrencia cubierta.
- [x] Administrador escribe; consulta solo lee investigación; sin roles no accede.
- [x] 90 operaciones HTTP protegidas y documentadas con Bearer; solicitudes directas verificadas.
- [x] Flask conserva separación HTTP y permisos tanto en menú como en URL.
- [x] Cookie sin JWT, sesiones en servidor, CSRF en login/logout y formularios de cambio.
- [x] 401/vencimiento limpia sesión; 403 sin datos; API caída o fallo de sesión presenta aviso sin investigación.
- [x] Arranque con migración previa, volumen nuevo/existente, configuración externa y versiones de paquetes fijadas.
- [x] Regresión de capas y CRUD integrado de investigación con administrador.
- [x] Archivos de compañeros conservados; v2 abierta, sin main ni tag v3.
- [ ] Recorrido humano de bootstrap oculto y navegador, incluido botón atrás.
- [ ] Revisión de compañeros, aportes, enmiendas formales y firmas de aceptación.

Recuperación por correo, registro público, restitución de asignaciones y v4
no forman parte de esta entrega. No presentar esta lista como aceptación humana.
