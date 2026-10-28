# Paso 1: voz con pausas naturales (solo se acortan las largas) y con volumen parejo (-14 LUFS, rango ~3 LU, como el video de referencia).
# Uso: powershell -File src\voz.ps1 -Entrada "C:\ruta\audio_original.wav"   -> audio\voz_final.wav
param([Parameter(Mandatory)][string]$Entrada)
$ErrorActionPreference = 'Stop'
$dir = Join-Path $PSScriptRoot '..\audio'; New-Item -ItemType Directory -Force $dir | Out-Null
Copy-Item $Entrada "$dir\original.wav"
Push-Location $dir
# Luis 2026-10-27: no cortar tanto. Solo las pausas de más de 0.8 s quedan en 0.5 s; las normales no se tocan
python (Join-Path $PSScriptRoot pausas.py) original.wav pausas.wav 0.8 0.5
ffmpeg -v error -y -i pausas.wav -ar 48000 sin_silencios.wav
# loudnorm de dos pasadas
$f = "acompressor=threshold=-24dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=4"
cmd /c "ffmpeg -hide_banner -i sin_silencios.wav -af $f`:print_format=json -f null - 2> ln.txt"
$m = [regex]::Match((Get-Content ln.txt -Raw), '\{[^{}]*"input_i"[^{}]*\}').Value | ConvertFrom-Json
ffmpeg -v error -y -i sin_silencios.wav -af "$f`:measured_I=$($m.input_i):measured_TP=$($m.input_tp):measured_LRA=$($m.input_lra):measured_thresh=$($m.input_thresh):offset=$($m.target_offset):linear=true" -ar 48000 voz_final.wav
ffprobe -v error -show_entries format=duration -of default=nw=1 voz_final.wav
Pop-Location
