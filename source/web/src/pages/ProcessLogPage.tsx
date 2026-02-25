import React, { useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Card, useTokenPermission } from 'supernova-core'
import { ProcessMonitorListTable } from '../shared/components/ProcessMonitorListTable'
import { ProcessMonitorFilters } from './ProcessMonitorFilters'
import { useFetchClients } from '@/shared/hooks/useFetchClients'
import { useProcessStatuses } from '@/hooks/useProcessStatuses'
import { useActivityTypes } from '@/hooks/useActivityTypes'
import { useProcessLogs } from '@/hooks/useProcessLogs'
import { getClientIdFromToken } from '@/shared/utils/getClient'
import { useProcessFilters } from '@/context/ProcessFiltersContext'

export function ProcessLogPage() {
  const { t } = useTranslation()
  const { token, refreshTokenByClientId } = useTokenPermission() as any
  const { filters, updateFilters } = useProcessFilters()

  const {
    data: clientsData,
    isLoading: clientsLoading,
    error: clientsError,
  } = useFetchClients(token)

  const tokenClientId = useMemo(() => getClientIdFromToken(token), [token])

  const [searchText, setSearchText] = useState('')
  const [debouncedFilterText, setDebouncedFilterText] = useState('')
  const [isTokenRefreshing, setIsTokenRefreshing] = useState(false)

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedFilterText(searchText), 500)
    return () => clearTimeout(handler)
  }, [searchText])

  useEffect(() => {
    if (!filters.client && tokenClientId) {
      updateFilters({ client: tokenClientId })
    }
  }, [tokenClientId, filters.client, updateFilters])

  const clientOptions = useMemo(() => {
    if (!clientsData)
      return []

    return [...clientsData]
      .sort((a, b) => (a.name || '').localeCompare(b.name || ''))
      .map(client => ({
        label: client.name || t('unnamedClient'),
        value: client.id,
      }))
  }, [clientsData, t])

  const { data: statusLogs } = useProcessStatuses(token, filters.client, {
    enabled: Boolean(filters.client),
  })

  const { data: activityTypes } = useActivityTypes(token, filters.client, {
    enabled: Boolean(filters.client),
  })

  useEffect(() => {
    if (statusLogs && (filters.states === undefined || filters.states === null)) {
      updateFilters({ states: statusLogs.map(s => s.status) })
    }
  }, [statusLogs, filters.states, updateFilters])

  const {
    data: processLogs,
    isLoading: processLogLoading,
    error: processLogErr,
  } = useProcessLogs(
    token,
    filters.client,
    { ...filters, filterText: debouncedFilterText },
    { enabled: Boolean(filters.client) },
  )

  const handleClientChange = async (clientId: string) => {
    setIsTokenRefreshing(true)
    try {
      await refreshTokenByClientId(clientId)
    }
    finally {
      updateFilters({ client: clientId })
      setIsTokenRefreshing(false)
    }
  }

  if (clientsLoading)
    return <div>{t('loadingClients')}</div>

  if (clientsError) {
    return (
      <div>
        {t('errorLoadingClients', { error: String(clientsError) })}
      </div>
    )
  }

  return (
    <Card header={<div>{t('processMonitor')}</div>}>
      <ProcessMonitorFilters
        filters={filters}
        onFilterChange={updateFilters}
        availableStatuses={
          statusLogs || [
            {
              id: '0',
              status: t('noStatusFound'),
              name: t('noStatusFound'),
              description: t('noStatusFound'),
            },
          ]
        }
        clientOptions={clientOptions}
        defaultClient={tokenClientId}
        refreshTokenByClientId={handleClientChange}
        isTokenRefreshing={isTokenRefreshing}
      />

      {processLogLoading && <div>{t('loadingProcessLogs')}</div>}

      {!processLogLoading && !processLogErr && (
        <ProcessMonitorListTable
          tokenClientId={tokenClientId!}
          data={processLogs?.items || []}
          totalRows={processLogs?.totalCount || 0}
          page={filters.pageNumber - 1}
          rowsPerPage={filters.pageSize}
          onPageChange={page => updateFilters({ pageNumber: page + 1 })}
          onRowsPerPageChange={rowsPerPage =>
            updateFilters({ pageSize: rowsPerPage })}
          order={filters.sortDirection as 'asc' | 'desc'}
          orderBy={filters.sortBy}
          onSortChange={columnId =>
            updateFilters({
              sortBy: columnId,
              sortDirection:
                filters.sortDirection === 'asc' ? 'desc' : 'asc',
            })}
          loading={processLogLoading || isTokenRefreshing}
          filterText={searchText}
          onFilterChange={setSearchText}
          activityTypes={activityTypes || []}
          processStatuses={statusLogs || []}
        />
      )}

      {processLogErr && (
        <div style={{ color: 'red' }}>
          {processLogErr.toString()}
        </div>
      )}
    </Card>
  )
}

export default ProcessLogPage
