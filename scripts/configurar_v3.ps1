# Genera solo secretos faltantes. Nunca imprime ni reemplaza valores existentes.
# Guarda en $ErrorActionPreference el resultado de la expresion asignada.
$ErrorActionPreference = 'Stop'
# Guarda en $ruta el resultado de la expresion asignada.
$ruta = Join-Path $PSScriptRoot '../v3-local.env'
# Guarda en $lineas el resultado de la expresion asignada.
$lineas = if (Test-Path -LiteralPath $ruta) { @(Get-Content -LiteralPath $ruta) } else { @() }
# Repite el bloque para cada elemento de la coleccion indicada.
foreach ($nombre in @('V3_DB_PASSWORD', 'JWT_SECRET', 'CLAVE_SESION')) {
    # Ejecuta el bloque segun el resultado de la condicion.
    if (-not ($lineas -match "^${nombre}=")) {
        # Guarda en $bytes el resultado de la expresion asignada.
        $bytes = New-Object byte[] 48
        # Guarda en $generador el resultado de la expresion asignada.
        $generador = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        # Ejecuta la instruccion PowerShell indicada.
        try { $generador.GetBytes($bytes) } finally { $generador.Dispose() }
        # Guarda en $valor el resultado de la expresion asignada.
        $valor = -join ($bytes | ForEach-Object { $_.ToString('x2') })
        # Guarda en $lineas el resultado de la expresion asignada.
        $lineas += "${nombre}=$valor"
    # Ejecuta la instruccion PowerShell indicada.
    }
# Ejecuta la instruccion PowerShell indicada.
}
# Ejecuta el bloque segun el resultado de la condicion.
if (-not ($lineas -match '^JWT_MINUTOS=')) { $lineas += 'JWT_MINUTOS=30' }
# Ejecuta el bloque segun el resultado de la condicion.
if (-not ($lineas -match '^COOKIE_SECURE=')) { $lineas += 'COOKIE_SECURE=0' }
# Guarda en $lineas el resultado de la expresion asignada.
$lineas | Set-Content -LiteralPath $ruta -Encoding ascii
# Ejecuta la instruccion PowerShell indicada.
Write-Output 'Configuración local lista; valores existentes conservados.'
