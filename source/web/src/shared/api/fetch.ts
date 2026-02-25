import type { HttpMethod } from '@/shared/types'

export interface FetchApiParams<D = unknown> {
  apiUrl: string
  token?: string
  url: string
  method: HttpMethod
  params?: Record<string, string>
  data?: D | FormData
  service?: 'web_platform_core' | 'web_process_log' | string
  headers?: Record<string, string>
  signal?: AbortSignal
}

export async function fetchApi<T = unknown, D = unknown>({
  apiUrl,
  url,
  method,
  token,
  params,
  data,
  headers: customHeaders = {},
  signal,
}: FetchApiParams<D>): Promise<T> {
  const baseUrl = apiUrl
  if (!baseUrl) {
    throw new Error('ModuleFederation service URL not ready')
  }

  const finalUrl = new URL(`${baseUrl}/api/${url}`)

  if (params) {
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null) {
        finalUrl.searchParams.append(key, val)
      }
    })
  }

  const isFormData
    = typeof FormData !== 'undefined' && data instanceof FormData

  const headers: Record<string, string> = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
    ...customHeaders,
  }

  const body = data
    ? isFormData
      ? (data as FormData)
      : JSON.stringify(data)
    : undefined

  const response = await fetch(finalUrl.toString(), {
    method,
    headers,
    body,
    mode: 'cors',
    signal,
  })

  if (!response.ok) {
    let message = `Error ${response.status}: ${response.statusText}`
    let parsedBody: any = null

    try {
      const clone = response.clone()
      const contentType = clone.headers.get('content-type') || ''

      if (contentType.includes('application/json')) {
        parsedBody = await clone.json()
      }
      else {
        parsedBody = await clone.text()
      }

      if (parsedBody) {
        if (typeof parsedBody === 'object') {
          message = parsedBody.message || parsedBody.error || message
        }
        else if (typeof parsedBody === 'string') {
          message = parsedBody
        }
      }
    }
    catch (err) {
      console.warn('Failed to parse error body', err)
    }

    if (response.status === 500) {
      message = 'There is no configured database for this client.'
    }
    else if (response.status === 404) {
      message = 'The requested data could not be found.'
    }
    else if (!message || message.startsWith('Error')) {
      message = 'Something went wrong. Please try again later.'
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return null as T
  }

  return response.json() as Promise<T>
}
