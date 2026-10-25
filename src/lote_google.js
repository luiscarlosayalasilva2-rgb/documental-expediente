// Descarga fotos de Google Imágenes en tamaño original (se pega en la consola de una pestaña de google.com con Claude in Chrome).
// Requiere src/receptor.py corriendo en 127.0.0.1:8765. Chrome puede pedir permiso de "red local": darle Permitir.
// Búsqueda recomendada: https://www.google.com/search?q=<consulta>&udm=2&tbs=isz:l   (isz:l = tamaño grande)
// Uso:  localStorage.loteHD = <este archivo como texto>;  eval(localStorage.loteHD);  loteHD('prefijo', 6, 1100, 1.2)
//       -> guarda prefijo_00.jpg … con ancho >= 1100 px y proporción ancho/alto >= 1.2 (horizontal).
//       Progreso: window.res (lista) y window.listo (true al terminar).
// La URL original y su tamaño están en los <script> de la página como ["url",alto,ancho] después del data-docid.
window.loteHD = async (prefijo, n, minW = 1100, minR = 1.2) => {
  window.res = []; window.listo = false;
  for (let w = 0; w < 20 && document.querySelectorAll('div[data-lpage]').length < 12; w++) await new Promise(r => setTimeout(r, 300));
  const html = [...document.scripts].map(s => s.textContent).join('\n');
  const re = /\["(https?:\/\/[^"]+?)",(\d+),(\d+)\]/g;
  const els = [...document.querySelectorAll('div[data-lpage]')].slice(0, 60);
  let guardadas = 0; const usadas = new Set();
  for (const el of els) {
    if (guardadas >= n) break;
    try {
      const idx = html.indexOf(el.dataset.docid); if (idx < 0) continue;
      re.lastIndex = idx; let m, orig = null;
      while ((m = re.exec(html)) && m.index < idx + 6000) {
        if (!m[1].includes('encrypted-tbn') && !m[1].includes('gstatic.com')) { orig = { u: JSON.parse('"' + m[1] + '"'), h: +m[2], w: +m[3] }; break; }
      }
      if (!orig || usadas.has(orig.u)) continue;
      if (orig.w < minW || orig.w / orig.h < minR) continue;
      usadas.add(orig.u);
      const host = new URL(el.dataset.lpage).hostname;
      const titulo = (el.innerText || '').split('\n')[0].slice(0, 70);
      const nombre = prefijo + '_' + String(guardadas).padStart(2, '0') + '.jpg';
      const r = await fetch('http://127.0.0.1:8765/guardar?nombre=' + nombre + '&info=' + encodeURIComponent(host + ' | ' + titulo + ' | ' + orig.w + 'x' + orig.h) + '&u=' + encodeURIComponent(orig.u) + '&ref=' + encodeURIComponent(el.dataset.lpage), { method: 'POST', body: '' });
      if (r.status === 200) { guardadas++; res.push(nombre + ' ' + orig.w + 'x' + orig.h + ' ' + host); } else res.push('fallo ' + host + ' ' + orig.w + 'x' + orig.h);
    } catch (e) { res.push('error ' + e.message); }
  }
  window.listo = true;
};
