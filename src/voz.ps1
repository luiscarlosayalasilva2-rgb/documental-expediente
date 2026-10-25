# Paso 1: voz sin espacios vacíos y con volumen parejo (-14 LUFS, rango ~3 LU, como el video de referencia).
# Uso: powershell -File src\voz.ps1 -Entrada "C:\ruta\audio_original.wav"   -> audio\voz_final.wav
param([Parameter(Mandatory)][string]$Entrada)
$ErrorActionPreference = 'Stop'
$dir = Join-Path $PSScriptRoot '..\audio'; New-Item -ItemType Directory -Force $dir | Out-Null
Copy-Item $Entrada "$dir\original.wav"
Push-Location $dir
# quita toda pausa de más de 0.15 s y deja 0.12 s entre frases
ffmpeg -v error -y -i original.wav -af "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05:stop_periods=-1:stop_duration=0.15:stop_threshold=-40dB:stop_silence=0.12" -ar 48000 sin_silencios.wav
# loudnorm de dos pasadas
$f = "acompressor=threshold=-24dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=4"
cmd /c "ffmpeg -hide_banner -i sin_silencios.wav -af $f`:print_format=json -f null - 2> ln.txt"
$m = [regex]::Match((Get-Content ln.txt -Raw), '\{[^{}]*"input_i"[^{}]*\}').Value | ConvertFrom-Json
ffmpeg -v error -y -i sin_silencios.wav -af "$f`:measured_I=$($m.input_i):measured_TP=$($m.input_tp):measured_LRA=$($m.input_lra):measured_thresh=$($m.input_thresh):offset=$($m.target_offset):linear=true" -ar 48000 voz_final.wav
ffprobe -v error -show_entries format=duration -of default=nw=1 voz_final.wav
Pop-Location
