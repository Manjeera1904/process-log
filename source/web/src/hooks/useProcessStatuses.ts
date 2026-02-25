import { useQuery } from '@tanstack/react-query'
import { fetchApi } from '@/shared/api/fetch'
import { useModuleFederation } from '@/app/providers/ModuleFederation'
import name from '@/config'

interface ProcessStatus {
  id: string
  status: string
  name: string
  description: string
}

const DEFAULT_CULTURE_CODE = 'en-US'

export function useProcessStatuses(
  token?: string,
  clientId?: string,
  options?: { enabled?: boolean },
) {
  const { current } = useModuleFederation(name)

  return useQuery<ProcessStatus[], Error>({
    queryKey: ['process-statuses', clientId],
    queryFn: async ({ signal }) => {
      if (!token || !clientId) {
        throw new Error('Missing token or clientId')
      }
      if (!current?.apiUrl) {
        throw new Error('Missing API URL in module federation config')
      }

      return fetchApi<ProcessStatus[]>({
        apiUrl: current.apiUrl,
        token,
        url: 'ProcessStatus',
        method: 'GET',
        params: {
          'api-version': '1.0',
          'cultureCode': DEFAULT_CULTURE_CODE,
          'X-EI-ClientId': clientId,
        },
        headers: {
          'X-EI-ClientId': clientId,
        },
        signal,
      })
    },
    enabled:
      !!token && !!clientId && !!current?.apiUrl && options?.enabled !== false,
  })
}
