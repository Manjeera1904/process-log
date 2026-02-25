import { postTelemetry } from '../api/telemetry'
import type { ExceptionTelemetryPayload } from '../types'

export function handleError(
  apiUrl: string,
  error: unknown,
  context: string,
  exceptionPayload?: ExceptionTelemetryPayload,
  token?: string,
): never {
  console.error(`Error in ${context}:`, error)
  if (exceptionPayload && token) {
    postTelemetry(apiUrl, 'exception', exceptionPayload, token)
  }
  throw error
}
