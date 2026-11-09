# Genera solo secretos faltantes. Nunca imprime ni reemplaza valores existentes.
$ErrorActionPreference = 'Stop'
$ruta = Join-Path $PSScriptRoot '../v3-local.env'
$lineas = if (Test-Path -LiteralPath $ruta) { @(Get-Content -LiteralPath $ruta) } else { @() }
foreach ($nombre in @('V3_DB_PASSWORD', 'JWT_SECRET', 'CLAVE_SESION')) {
    if (-not ($lineas -match "^${nombre}=")) {
        $bytes = New-Object byte[] 48
        $generador = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        try { $generador.GetBytes($bytes) } finally { $generador.Dispose() }
        $valor = -join ($bytes | ForEach-Object { $_.ToString('x2') })
        $lineas += "${nombre}=$valor"
    }
}
if (-not ($lineas -match '^JWT_MINUTOS=')) { $lineas += 'JWT_MINUTOS=30' }
if (-not ($lineas -match '^COOKIE_SECURE=')) { $lineas += 'COOKIE_SECURE=0' }
$lineas | Set-Content -LiteralPath $ruta -Encoding ascii
Write-Output 'Configuración local lista; valores existentes conservados.'
