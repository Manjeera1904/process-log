import { useQuery } from '@tanstack/react-query'

import { getClients } from '../api/clientsApi'
import { handleError } from '../utils/errors'
import { useModuleFederation } from '@/app/providers/ModuleFederation'

export function useFetchClients(token?: string) {
  const { apps } = useModuleFederation()

  const url = apps?.find(i => i.name === 'web_platform_core')?.apiUrl

  return useQuery({
    queryKey: ['clients', 'clientList'],
    queryFn: async () => {
      if (!token) {
        handleError(url!, new Error('Token not found'), 'useFetchClients')
        return []
      }
      return getClients(url!, token)
    },
    retry: (failureCount, error) => {
      if ((error as any).status === 404)
        return false
      return failureCount < 2
    },
    enabled: !!token && !!url,
  })
}
