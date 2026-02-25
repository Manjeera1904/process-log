export function loadFromStorage<T>(key: string, defaultValue: T): T {
  if (typeof window === 'undefined')
    return defaultValue
  try {
    const raw = localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : defaultValue
  }
  catch {
    return defaultValue
  }
}

export function saveToStorage(key: string, value: unknown) {
  if (typeof window === 'undefined')
    return
  try {
    localStorage.setItem(key, JSON.stringify(value))
  }
  catch (err) {
    console.error(`Failed to save ${key}:`, err)
  }
}
