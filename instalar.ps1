# Deja una PC con Windows lista para este pipeline. Se puede correr varias veces: lo ya instalado se salta.
# Uso (PowerShell, dentro de la carpeta del repo):  powershell -ExecutionPolicy Bypass -File instalar.ps1
#
# Instala desde sus fuentes oficiales:
#   - Python 3.13 y ffmpeg (winget)
#   - faster-whisper, numpy y pillow (pip, versiones de requirements.txt)
#   - Real-ESRGAN ncnn-vulkan (release oficial de GitHub, xinntao/Real-ESRGAN) en ..\herramientas\realesrgan
#   - el modelo "small" de Whisper (primera transcripción)
# Lo que NO puede instalar solo: la clave de Pixabay (correr src\guardar_clave_pixabay.ps1)
# y la extensión Claude in Chrome (se instala en Chrome desde claude.ai).
$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
function Refrescar-Path { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') }
function Tiene($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

Write-Host '1/5 Python' -ForegroundColor Cyan
if (-not (Tiene python) -or -not ((python --version 2>&1) -match 'Python 3\.(1[1-9])')) {
    winget install --id Python.Python.3.13 -e --source winget --accept-package-agreements --accept-source-agreements --silent
    Refrescar-Path
}
python --version

Write-Host '2/5 ffmpeg' -ForegroundColor Cyan
if (-not (Tiene ffmpeg)) {
    winget install --id Gyan.FFmpeg -e --source winget --accept-package-agreements --accept-source-agreements --silent
    Refrescar-Path
}
(ffmpeg -version | Select-Object -First 1)

Write-Host '3/5 Paquetes de Python' -ForegroundColor Cyan
python -m pip install --user -r "$raiz\requirements.txt"

Write-Host '4/5 Real-ESRGAN' -ForegroundColor Cyan
$esr = Join-Path (Split-Path $raiz -Parent) 'herramientas\realesrgan'
$exe = Join-Path $esr 'realesrgan-ncnn-vulkan.exe'
if (-not (Test-Path $exe)) {
    New-Item -ItemType Directory -Force $esr | Out-Null
    $zip = Join-Path $esr 'realesrgan.zip'
    Invoke-WebRequest 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip' -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $esr -Force
    Remove-Item $zip
}
Write-Host "   $exe  (usar siempre -t 64 en tarjetas Intel: si no, sale negro)"

Write-Host '5/5 Modelo de Whisper' -ForegroundColor Cyan
python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8'); print('   modelo small listo')"

Write-Host ''
Write-Host 'Listo. Falta, a mano:' -ForegroundColor Green
Write-Host '  - Clave de Pixabay:  powershell -ExecutionPolicy Bypass -File src\guardar_clave_pixabay.ps1'
Write-Host '  - Extensión Claude in Chrome (para bajar fotos de Google Imágenes).'
Write-Host '  - Real-ESRGAN queda al lado del repo (..\herramientas). Para otra ubicación: variable REALESRGAN_EXE.'
