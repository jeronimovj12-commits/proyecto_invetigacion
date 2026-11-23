# Decisiones técnicas de la v2

## Referencias entre tablas

Los formularios cargan desde la API las opciones de los desplegables. Así, el usuario puede elegir un registro relacionado sin memorizar su código. Al guardar, la API comprueba que la referencia exista y esté activa. Si la referencia es inválida, rechaza la operación y conserva los datos anteriores.

## Actualizaciones completas y parciales

La API exige todos los campos requeridos en una petición PUT. Para cambiar un solo campo, como el nombre, admite una petición PATCH. Así se puede corregir un dato sin volver a enviar los demás. Si el cambio solicitado es inválido, el registro conserva sus valores.

## Borrado lógico

Al desactivar un registro, la fila permanece en PostgreSQL y queda marcada como inactiva. Si otros registros activos dependen de ella, la API impide la desactivación para conservar la relación.

## Verificación en dos etapas

Las pruebas en memoria permiten comprobar por separado reglas como el rechazo de referencias inactivas y la conservación de valores tras una actualización inválida. La prueba integrada utiliza Docker y PostgreSQL para comprobar las operaciones con datos almacenados. El script crea sus propias fichas y las desactiva al terminar.

El 4 de noviembre de 2026 pasaron las 12 pruebas en memoria y terminó correctamente la prueba integrada. El resultado quedó registrado en `VERIFICACION_V2.md`. La revisión visual de las diez pantallas sigue pendiente.