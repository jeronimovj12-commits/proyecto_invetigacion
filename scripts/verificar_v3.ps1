# Ejecutar desde la raíz del repositorio. Se detiene al primer fallo.
# Guarda en $ErrorActionPreference el resultado de la expresion asignada.
$ErrorActionPreference = 'Stop'
# Guarda en $v3 el resultado de la expresion asignada.
$v3 = @('-p','investigacion-v3','--env-file','v3-local.env','-f','docker-compose.v3.yml','-f','docker-compose.v3.pruebas.yml')
# Declara la funcion PowerShell indicada.
function Ejecutar-Docker {
    # Ejecuta la instruccion PowerShell indicada.
    param([string[]] $ArgumentosDocker)
    # Ejecuta la instruccion PowerShell indicada.
    & docker @ArgumentosDocker
    # Ejecuta el bloque segun el resultado de la condicion.
    if ($LASTEXITCODE -ne 0) { throw 'Falló una verificación; revise la salida anterior.' }
# Ejecuta la instruccion PowerShell indicada.
}
# Ejecuta la instruccion PowerShell indicada.
Ejecutar-Docker (@('compose') + $v3 + @('build'))
# Repite el bloque para cada elemento de la coleccion indicada.
foreach ($prueba in @('prueba_migracion_v3.py','prueba_autenticacion_v3.py','prueba_administracion_v3.py')) {
    # Ejecuta la instruccion PowerShell indicada.
    Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','-e','PRUEBAS_V3=1','api-v3','python',"pruebas/$prueba"))
# Ejecuta la instruccion PowerShell indicada.
}
# Repite el bloque para cada elemento de la coleccion indicada.
foreach ($prueba in @('prueba_capas.py','prueba_v2.py')) {
    # Ejecuta la instruccion PowerShell indicada.
    Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','api-v3','python',"pruebas/$prueba"))
# Ejecuta la instruccion PowerShell indicada.
}
# Ejecuta la instruccion PowerShell indicada.
Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','front-v3','python','-m','unittest','discover','-s','pruebas','-p','prueba_front_seguro_v3.py','-v'))
# Ejecuta la instruccion PowerShell indicada.
try {
    # Ejecuta la instruccion PowerShell indicada.
    Ejecutar-Docker (@('compose') + $v3 + @('up','-d','--force-recreate','pruebas-api-v3'))
    # Ejecuta la instruccion PowerShell indicada.
    Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','pruebas-front-v3'))
# Ejecuta la instruccion PowerShell indicada.
} finally {
    # Ejecuta la instruccion PowerShell indicada.
    & docker compose @v3 stop pruebas-api-v3
# Ejecuta la instruccion PowerShell indicada.
}
# Ejecuta la instruccion PowerShell indicada.
Write-Output 'Verificaciones automáticas v3 completadas.'
