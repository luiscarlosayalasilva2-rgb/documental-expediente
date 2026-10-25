# Pasos 11-12: render del EDL + efectos sintetizados + mezcla final con la voz (sin música).
# Uso: powershell -File src\mezclar.ps1 -Edl final\edl_v3.json -Salida final\video_FINAL.mp4
# La laptop debe estar conectada al cargador (si se suspende, el render se cae).
param([string]$Edl = 'final\edl_v3.json', [string]$Salida = 'final\video_FINAL.mp4')
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
python -W ignore src\render.py $Edl final\_sin_audio.mp4 --workers 4
python -W ignore src\efectos.py $Edl audio\efectos.wav
ffmpeg -v error -y -i final\_sin_audio.mp4 -i audio\voz_final.wav -i audio\efectos.wav -filter_complex "[1:a]aresample=48000[v];[2:a]aresample=48000[e];[v][e]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k $Salida
Remove-Item final\_sin_audio.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 $Salida
