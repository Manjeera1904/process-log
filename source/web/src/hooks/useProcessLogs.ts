import { type UseQueryResult, useQuery } from '@tanstack/react-query'
import { fetchApi } from '@/shared/api/fetch'
import { useFetchClients } from '@/shared/hooks/useFetchClients'
import { ProcessState } from '@/constants/enums'
import { useModuleFederation } from '@/app/providers/ModuleFederation'
import name from '@/config'

export interface ProcessItem {
  type: string
  id: string
  description: string
  client: string
  source: string
  processedOn: string
  state: ProcessState
  disposition: string
  docs?: number
  duration: string
}

export interface ProcessLogsResponse {
  items: ProcessItem[]
  totalCount: number
}

interface Filters {
  dateRange?: string
  sortBy?: string
  sortDirection?: string
  pageNumber?: number
  pageSize?: number
  timeZone?: string
  activityType?: string
  states?: string[]
  filterText?: string
}

interface RawProcessLogItem {
  status?: string
  startTimestamp?: string
  lastUpdatedTimestamp?: string
  type?: string
  id?: string
  files?: { fileName: string }[]
  fileCount?: number
  updatedBy?: string
  disposition?: string
}

const statusMap: Record<string, ProcessState> = {
  completed: ProcessState.Completed,
  success: ProcessState.Completed,
  failed: ProcessState.Failed,
  error: ProcessState.Failed,
  inprogress: ProcessState.InProgress,
  running: ProcessState.InProgress,
  new: ProcessState.New,
  pending: ProcessState.Pending,
}

export function useProcessLogs(
  token?: string,
  clientId?: string,
  filters?: Filters,
  options?: { enabled?: boolean },
): UseQueryResult<ProcessLogsResponse, Error> {
  const { data: clients } = useFetchClients(token)
  const { current } = useModuleFederation(name)

  const getClientName = (id: string) => {
    return clients?.find(c => c.id === id)?.name || id
  }

  return useQuery<ProcessLogsResponse, Error>({
    queryKey: ['process-logs', clientId, JSON.stringify(filters)],
    queryFn: async ({ signal }) => {
      if (!token || !clientId) {
        throw new Error('Missing token or clientId')
      }
      if (!current?.apiUrl) {
        throw new Error('Missing API URL in module federation config')
      }

      const params: Record<string, string> = {
        'api-version': '1.0',
        ...(filters?.dateRange && { DateRange: filters.dateRange }),
        ...(filters?.sortBy && { SortBy: filters.sortBy }),
        ...(filters?.sortDirection && { SortDirection: filters.sortDirection }),
        ...(filters?.pageNumber !== undefined && {
          PageNumber: filters.pageNumber.toString(),
        }),
        ...(filters?.pageSize !== undefined && {
          PageSize: filters.pageSize.toString(),
        }),
        ...(filters?.timeZone && { TimeZone: filters.timeZone }),
        ...(filters?.filterText && { Filter: filters.filterText }),
      }

      if (filters?.activityType) {
        params.ActivityType = filters.activityType
      }

      const url = 'ProcessLog/Search'
      const queryParams = new URLSearchParams(params)
      filters?.states?.forEach(state =>
        queryParams.append('Statuses', state),
      )
      const fullUrl = `${url}?${queryParams.toString()}`

      const data = await fetchApi<{
        items: RawProcessLogItem[]
        totalCount: number
      }>({
        apiUrl: current.apiUrl,
        token,
        url: fullUrl,
        method: 'GET',
        headers: { 'X-EI-ClientId': clientId },
        signal,
      })

      const items = (data?.items || []).map((item: RawProcessLogItem) => {
        const state
          = statusMap[item.status?.toLowerCase() || ''] || ProcessState.Unknown
        const start = item.startTimestamp && new Date(item.startTimestamp)
        const end
          = item.lastUpdatedTimestamp && new Date(item.lastUpdatedTimestamp)

        const processedOn = end
          ? end.toLocaleString('en-US', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
              hour12: false,
            })
          : ''

        const duration
          = start && end
            ? new Date(end.getTime() - start.getTime())
                .toISOString()
                .substr(11, 8)
            : ''

        return {
          type: item.type || '',
          id: item.id || '',
          description:
            item.files && item.files.length > 0
              ? `${item.files.map(file => file.fileName.split('/').pop()).join(', ')} (${item.fileCount ?? item.files.length} files)`
              : item.type || '',
          client: getClientName(clientId),
          source: item.updatedBy || '',
          processedOn,
          disposition: item.disposition || '',
          docs: item.fileCount ?? item.files?.length ?? 0,
          state,
          duration,
        }
      })

      return { items, totalCount: data?.totalCount ?? 0 }
    },
    enabled:
      !!token
      && !!clientId
      && !!clients
      && !!current?.apiUrl
      && options?.enabled !== false,
  })
}
