# Crea el primer administrador conectándose de forma segura a PostgreSQL de Render.
$ErrorActionPreference = 'Stop'

# Construye la imagen de ayuda desde la raíz sin guardar credenciales en ella.
docker build -f api_investigacion/Dockerfile.render -t investigacion-api-v3-render .
if ($LASTEXITCODE -ne 0) { throw 'No se pudo construir la imagen local de apoyo.' }

# Solicita la URL externa de la base sin mostrarla en pantalla.
$urlSegura = Read-Host 'Pega la URL externa de PostgreSQL de Render (entrada oculta)' -AsSecureString
$punteroUrl = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($urlSegura)
$urlBase = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($punteroUrl)

# Genera una clave de prueba efímera; el comando de bootstrap no emite JWT.
$bytesJwt = [byte[]]::new(32)
$generador = [Security.Cryptography.RandomNumberGenerator]::Create()
$generador.GetBytes($bytesJwt)
$generador.Dispose()
$secretoJwt = [Convert]::ToBase64String($bytesJwt)

# Guarda temporalmente variables en el directorio del usuario y nunca en el repositorio.
$archivoTemporal = Join-Path $env:TEMP ('investigacion-render-' + [guid]::NewGuid().ToString('N') + '.env')
try {
    @(
        "DATABASE_URL=$urlBase"
        "JWT_SECRET=$secretoJwt"
        'JWT_ISSUER=investigacion-v3'
        'JWT_AUDIENCE=investigacion-api'
    ) | Set-Content -LiteralPath $archivoTemporal -Encoding ascii

    # Ejecuta el mismo inicializador protegido; no pasa contraseñas como argumentos.
    docker run --rm -it --env-file $archivoTemporal investigacion-api-v3-render python -m comandos.crear_administrador
    if ($LASTEXITCODE -ne 0) { throw 'No se creó el administrador; revisa la conexión y el mensaje del comando.' }
}
finally {
    # Borra el archivo temporal aunque el comando falle o se interrumpa.
    Remove-Item -LiteralPath $archivoTemporal -Force -ErrorAction SilentlyContinue
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($punteroUrl)
    $urlSegura.Dispose()
    [Array]::Clear($bytesJwt, 0, $bytesJwt.Length)
    $urlBase = $null
    $secretoJwt = $null
}
