import type { TelemetryType } from '../types'
import { fetchApi } from './fetch'

const TELEMTRY_URL = 'UiTelemetry'

export function getMaskedUrl(url: string) {
  const urlObj = new URL(url, 'http://dummy')

  const maskedPath = urlObj.pathname
    .split('/')
    .map(segment => (segment.includes('-') ? 'xxxx-xxxx-xxxx-xxxx' : segment))
    .join('/')

  const maskedSearchParams = new URLSearchParams(urlObj.search)
  for (const [key, value] of maskedSearchParams.entries()) {
    if (value.includes('-')) {
      maskedSearchParams.set(key, 'xxxx-xxxx-xxxx-xxxx')
    }
  }

  return `${maskedPath}?${maskedSearchParams.toString()}`
}

export function generateTraceId() {
  const time = Date.now()
  const timeHex = time.toString(16).padStart(12, '0')

  const randomBytes = new Uint8Array(10)
  crypto.getRandomValues(randomBytes)

  const randomHex = Array.from(randomBytes, b =>
    b.toString(16).padStart(2, '0')).join('')

  return timeHex + randomHex
}

export function postTelemetry<T>(
  apiUrl: string,
  telemetryType: TelemetryType,
  payload: T,
  token: string,
): Promise<unknown> {
  const typeToEndpoint = {
    event: 'Event',
    exception: 'Exception',
    metric: 'Metric',
    trace: 'Trace',
    span: 'Span',
  } as const

  const url = `${TELEMTRY_URL}/${typeToEndpoint[telemetryType] ?? ''}`

  return fetchApi({
    apiUrl,
    method: 'POST',
    url,
    service: 'web_platform_core',
    params: { 'api-version': '1.0' },
    data: payload,
    token,
  }).catch(console.error)
}

export function getApiTokenFromHeadersObj(obj: Record<string, string>) {
  const authHeader = obj.Authorization || obj.authorization
  if (!authHeader || typeof authHeader !== 'string')
    return ''
  return authHeader.startsWith('Bearer ')
    ? authHeader.slice(7).trim()
    : authHeader.trim()
}
