// Formateadores compartidos (sin dependencias de UI).

/** Bytes → tamaño legible (B, KB, MB, GB). Redondea a 1 decimal desde KB. */
export function formatBytes(bytes: number | null | undefined): string {
  const n = Number(bytes) || 0;
  if (n < 1024) return `${n} B`;
  const units = ['KB', 'MB', 'GB', 'TB'];
  let value = n / 1024;
  let i = 0;
  while (value >= 1024 && i < units.length - 1) {
    value /= 1024;
    i++;
  }
  return `${value.toFixed(1)} ${units[i]}`;
}

/** Normaliza texto para búsquedas: sin tildes, minúsculas (NFD). */
export function normalizarTexto(s: string): string {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

const pad2 = (n: number) => String(n).padStart(2, '0');

/**
 * Fecha → "dd/MM/yyyy" (locale-agnóstico, sin dependencias). El repo no usa date-fns;
 * los formateadores de fecha del módulo documental viven aquí.
 * Acepta Date, timestamp ISO o `null`/`undefined` (devuelve "—").
 */
export function formatFecha(value: Date | string | number | null | undefined): string {
  if (value === null || value === undefined || value === '') return '—';
  const d = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(d.getTime())) return '—';
  return `${pad2(d.getDate())}/${pad2(d.getMonth() + 1)}/${d.getFullYear()}`;
}

/**
 * Fecha → "dd/MM/yyyy HH:mm". Mismas garantías que {@link formatFecha}. Año de 4 cifras
 * para que coincida con {@link formatFecha} y no convivan "08/07/2026" y "08/07/26" en la
 * misma pantalla (un único formato de fecha en todo el módulo documental).
 */
export function formatFechaHora(value: Date | string | number | null | undefined): string {
  if (value === null || value === undefined || value === '') return '—';
  const d = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(d.getTime())) return '—';
  return `${pad2(d.getDate())}/${pad2(d.getMonth() + 1)}/${d.getFullYear()} ${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
}
