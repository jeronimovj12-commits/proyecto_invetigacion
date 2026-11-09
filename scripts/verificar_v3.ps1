# Ejecutar desde la raíz del repositorio. Se detiene al primer fallo.
$ErrorActionPreference = 'Stop'
$v3 = @('-p','investigacion-v3','--env-file','v3-local.env','-f','docker-compose.v3.yml','-f','docker-compose.v3.pruebas.yml')
function Ejecutar-Docker {
    param([string[]] $ArgumentosDocker)
    & docker @ArgumentosDocker
    if ($LASTEXITCODE -ne 0) { throw 'Falló una verificación; revise la salida anterior.' }
}
Ejecutar-Docker (@('compose') + $v3 + @('build'))
foreach ($prueba in @('prueba_migracion_v3.py','prueba_autenticacion_v3.py','prueba_administracion_v3.py')) {
    Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','-e','PRUEBAS_V3=1','api-v3','python',"pruebas/$prueba"))
}
foreach ($prueba in @('prueba_capas.py','prueba_v2.py')) {
    Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','api-v3','python',"pruebas/$prueba"))
}
Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','front-v3','python','-m','unittest','discover','-s','pruebas','-p','prueba_front_seguro_v3.py','-v'))
try {
    Ejecutar-Docker (@('compose') + $v3 + @('up','-d','--force-recreate','pruebas-api-v3'))
    Ejecutar-Docker (@('compose') + $v3 + @('run','--rm','-T','pruebas-front-v3'))
} finally {
    & docker compose @v3 stop pruebas-api-v3
}
Write-Output 'Verificaciones automáticas v3 completadas.'
