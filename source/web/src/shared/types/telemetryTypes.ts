export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'

export type TelemetryType = 'event' | 'trace' | 'span' | 'metric' | 'exception'

export interface EventTelemetryPayload {
  Name: string
  Details: string
  OperatingSystem: string
  Browser: string
  traceId: string
  ApiUrl?: string
  ApiVersion?: string
  ApiResponseTime?: string
  HttpMethod?: HttpMethod
  Page?: string
  UserAction?: string
  ClickCount?: number
  [key: string]: any
}

export interface TraceTelemetryPayload {
  Name: string
  Message: string
  traceId: string
  OperatingSystem: string
  Browser: string
  Severity?: 'Verbose' | 'Information' | 'Warning' | 'Error' | 'Critical'
  Component?: string
  DurationMs?: number
  [key: string]: any
}

export interface SpanTelemetryPayload {
  Name: string
  Operation: string
  traceId: string
  OperatingSystem: string
  Browser: string
  Target?: string
  Success: boolean
  Duration?: number
  [key: string]: any
}

export interface MetricTelemetryPayload {
  MetricName: string
  Value: number
  traceId: string
  OperatingSystem: string
  Browser: string
  Unit?: string
  [key: string]: any
}

export interface ExceptionTelemetryPayload {
  Name: string
  Exception: string
  Message: string
  OperatingSystem: string
  traceId: string
  Browser: string
  ApiUrl?: string
  ApiVersion?: string
  ApiResponseTime?: string
  HttpMethod?: HttpMethod
  StackTrace?: string
  Severity?: 'Verbose' | 'Information' | 'Warning' | 'Error' | 'Critical'
  [key: string]: any
}

export interface LimitedEventTelemetryPayload {
  Name: string
  Details: string
}

export interface LimitedExceptionTelemetryPayload {
  Exception: string
  Message: string
}
