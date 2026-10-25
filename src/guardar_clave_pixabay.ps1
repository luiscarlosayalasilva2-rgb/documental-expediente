# Pide la clave de Pixabay sin mostrarla en pantalla y la guarda en la variable de usuario PIXABAY_API_KEY.
$seg = Read-Host 'Pega tu clave de Pixabay y pulsa Enter' -AsSecureString
$clave = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($seg)).Trim()
if (-not $clave) { Write-Host 'No se pegó ninguna clave. Vuelve a ejecutar el script.' -ForegroundColor Red; exit 1 }
$r = try { Invoke-RestMethod "https://pixabay.com/api/?key=$clave&q=helado&per_page=3" } catch { $null }
if (-not $r) { Write-Host 'Pixabay rechazó la clave. Revísala y vuelve a ejecutar el script.' -ForegroundColor Red; exit 1 }
[Environment]::SetEnvironmentVariable('PIXABAY_API_KEY', $clave, 'User')
Write-Host "Listo: clave guardada y comprobada ($($r.totalHits) resultados de prueba). Ya puedes volver al chat." -ForegroundColor Green
