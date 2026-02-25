import { getClientIdFromToken } from '../utils/getClient'
import { fetchApi } from './fetch'

export interface Client {
  id: string
  name: string
  isDefault: boolean
}

const API_VERSION = '1.0'

function sortByName<T extends { name?: string }>(items: T[]): T[] {
  return items.sort((a, b) => (a.name ?? '').localeCompare(b.name ?? ''))
}

export async function getClients(
  apiUrl: string,
  token: string,
): Promise<Client[]> {
  if (!token)
    return []

  const response = await fetchApi<Client[]>({
    apiUrl,
    method: 'GET',
    url: 'Client/User/self',
    token,
    service: 'web_platform_core',
    params: { 'api-version': API_VERSION },
  })

  const defaultClientId = getClientIdFromToken(token)

  return sortByName(response).map(client => ({
    ...client,
    isDefault: client.id === defaultClientId,
  }))
}
