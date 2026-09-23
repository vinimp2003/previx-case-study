// Helpers de pantalla completa con tipado para las APIs con prefijo de proveedor
// (webkit/moz/ms), evitando los `as any` repetidos. Comportamiento idéntico a las
// cadenas de fallback originales.

interface FullscreenCapableElement extends HTMLElement {
  webkitRequestFullscreen?: () => void;
  mozRequestFullScreen?: () => void;
  msRequestFullscreen?: () => void;
}

interface FullscreenCapableDocument extends Document {
  webkitExitFullscreen?: () => void;
  mozCancelFullScreen?: () => void;
  msExitFullscreen?: () => void;
  webkitFullscreenElement?: Element | null;
  mozFullScreenElement?: Element | null;
  msFullscreenElement?: Element | null;
}

/** Solicita pantalla completa para `el`. Devuelve true si el navegador lo soporta. */
export function requestFullscreenCompat(el: HTMLElement): boolean {
  const e = el as FullscreenCapableElement;
  if (e.requestFullscreen) { e.requestFullscreen(); return true; }
  if (e.webkitRequestFullscreen) { e.webkitRequestFullscreen(); return true; }
  if (e.mozRequestFullScreen) { e.mozRequestFullScreen(); return true; }
  if (e.msRequestFullscreen) { e.msRequestFullscreen(); return true; }
  return false;
}

/** Sale de pantalla completa (con fallbacks por proveedor). */
export function exitFullscreenCompat(): void {
  const d = document as FullscreenCapableDocument;
  if (d.exitFullscreen) d.exitFullscreen();
  else if (d.webkitExitFullscreen) d.webkitExitFullscreen();
  else if (d.mozCancelFullScreen) d.mozCancelFullScreen();
  else if (d.msExitFullscreen) d.msExitFullscreen();
}

/** Elemento actualmente en pantalla completa (con fallbacks por proveedor), o null. */
export function getFullscreenElement(): Element | null {
  const d = document as FullscreenCapableDocument;
  return d.fullscreenElement || d.webkitFullscreenElement || d.mozFullScreenElement || d.msFullscreenElement || null;
}
