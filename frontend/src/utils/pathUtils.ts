/** Get nested value by dot path, e.g. "home.introPara1" or "phases.0.title" */
export function getByPath(obj: unknown, path: string): unknown {
  return path.split('.').reduce((o: unknown, k) => (o != null && typeof o === 'object' ? (o as Record<string, unknown>)[k] : undefined), obj)
}

/** Set nested value by dot path, returns new object (immutable) */
export function setByPath<T>(obj: T, path: string, value: unknown): T {
  const keys = path.split('.')
  if (keys.length === 0) return obj
  const result = JSON.parse(JSON.stringify(obj)) as Record<string, unknown>
  let current: Record<string, unknown> = result
  for (let i = 0; i < keys.length - 1; i++) {
    const k = keys[i]
    const nextKey = keys[i + 1]
    const isNextArray = /^\d+$/.test(nextKey)
    if (!(k in current) || current[k] == null) {
      current[k] = isNextArray ? [] : {}
    }
    const next = current[k]
    current = (Array.isArray(next) ? next : next) as Record<string, unknown>
  }
  const lastKey = keys[keys.length - 1]
  if (/^\d+$/.test(lastKey)) {
    (current as unknown as unknown[])[parseInt(lastKey, 10)] = value
  } else {
    current[lastKey] = value
  }
  return result as T
}
