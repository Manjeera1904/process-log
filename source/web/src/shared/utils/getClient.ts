import { jwtDecode } from 'jwt-decode'

interface DecodedToken {
  clientId?: string
  [key: string]: any
}

export function getClientIdFromToken(token?: string): string | null {
  if (!token)
    return null
  try {
    const decoded = jwtDecode<DecodedToken>(token)
    return decoded['ei-client'] || null
  }
  catch (err) {
    console.error('Failed to decode token:', err)
    return null
  }
}
