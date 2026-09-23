/**
 * Helpers para leer errores capturados como `unknown` (el tipo correcto de un
 * `catch`) sin recurrir a `any`. Centraliza el patrón de sondear errores HTTP
 * tipo axios (`error.response.status`) y de extraer el mensaje.
 */

/** Código de estado HTTP de un error tipo axios, si lo tiene. */
export function errorStatus(e: unknown): number | undefined {
  return (e as { response?: { status?: number } } | null | undefined)?.response?.status;
}

/** Mensaje legible de un error desconocido. */
export function errorMessage(e: unknown): string {
  if (e instanceof Error) return e.message;
  if (typeof e === 'string') return e;
  const m = (e as { message?: unknown } | null | undefined)?.message;
  return typeof m === 'string' ? m : '';
}
