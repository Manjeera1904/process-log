import { useQuery } from '@tanstack/react-query'
import { fetchApi } from '@/shared/api/fetch'
import { useModuleFederation } from '@/app/providers/ModuleFederation'
import name from '@/config'

interface ActivityType {
  id: string
  type: string
  name: string
  description: string
}

const DEFAULT_CULTURE_CODE = 'en-US'

export function useActivityTypes(
  token?: string,
  clientId?: string,
  options?: { enabled?: boolean },
) {
  const { current } = useModuleFederation(name)

  return useQuery<ActivityType[], Error>({
    queryKey: ['activity-types', clientId],
    queryFn: async ({ signal }) => {
      if (!token || !clientId) {
        throw new Error('Missing token or clientId')
      }
      if (!current?.apiUrl) {
        throw new Error('Missing API URL in module federation config')
      }

      return fetchApi<ActivityType[]>({
        apiUrl: current.apiUrl,
        token,
        url: 'ActivityType',
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
