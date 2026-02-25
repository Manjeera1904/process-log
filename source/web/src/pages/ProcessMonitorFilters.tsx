import React from 'react'
import { useTranslation } from 'react-i18next'
import { Box, FilterButton, IconButton, MaterialIcons } from 'supernova-core'
import { FilterMenu } from './FilterMenu'
import { dateRanges } from '@/constants/dateRanges'

interface ProcessStatus {
  id: string
  status: string
  name: string
  description: string
}

interface ClientOption {
  label: string
  value: string
}

interface ProcessMonitorFiltersProps {
  filters: any
  onFilterChange: (newFilters: any) => void
  availableStatuses: ProcessStatus[]
  clientOptions: ClientOption[]
  defaultClient: string | null
  refreshTokenByClientId: (clientId: string) => void
  isTokenRefreshing?: boolean
}

export function ProcessMonitorFilters({
  filters,
  onFilterChange,
  availableStatuses,
  clientOptions,
  defaultClient,
  refreshTokenByClientId,
  isTokenRefreshing,
}: ProcessMonitorFiltersProps) {
  const { t } = useTranslation('processMonitor')

  const statusOptions = availableStatuses.map(status => ({
    label: status.name,
    value: status.status,
  }))

  const handleReset = () => {
    onFilterChange({
      client: defaultClient,
      dateRange: dateRanges[0]?.value,
      states: statusOptions.map(s => s.value),
    })
  }

  const dateRangeLabel
    = dateRanges.find(opt => opt.value === filters.dateRange)?.label ?? ''

  return (
    <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>

      <FilterMenu
        disabled={isTokenRefreshing}
        button={props => (
          <FilterButton
            {...props}
            sx={theme => ({
              'color': theme.palette.text.secondary,
              'borderColor': theme.palette.text.secondary,
              '& .MuiSvgIcon-root': { color: theme.palette.text.secondary },
            })}
            icon={<MaterialIcons.Business />}
          >
            {clientOptions.find(opt => opt.value === filters.client)?.label ?? ''}
          </FilterButton>
        )}
        options={clientOptions}
        value={filters.client}
        onChange={(val) => {
          onFilterChange({ ...filters, client: val })
          refreshTokenByClientId(val)
        }}
      />

      <FilterMenu
        disabled={isTokenRefreshing}
        button={props => (
          <FilterButton
            {...props}
            sx={theme => ({
              'color': theme.palette.text.secondary,
              'borderColor': theme.palette.text.secondary,
              '& .MuiSvgIcon-root': { color: theme.palette.text.secondary },
            })}
            icon={<MaterialIcons.Today />}
          >
            {dateRangeLabel}
          </FilterButton>
        )}
        options={dateRanges}
        value={filters.dateRange}
        onChange={val => onFilterChange({ ...filters, dateRange: val })}
      />

      <FilterMenu
        disabled={isTokenRefreshing}
        button={props => (
          <FilterButton
            {...props}
            sx={theme => ({
              'color': theme.palette.text.secondary,
              'borderColor': theme.palette.text.secondary,
              '& .MuiSvgIcon-root': { color: theme.palette.text.secondary },
            })}
            icon={<MaterialIcons.Tune />}
          >
            {t('filters.status')}
          </FilterButton>
        )}
        options={statusOptions}
        value={filters.states}
        onChange={val => onFilterChange({ ...filters, states: val })}
        multiple
      />

      <IconButton
        disabled={isTokenRefreshing}
        sx={{ color: theme => theme.palette.text.secondary }}
        onClick={handleReset}
      >
        <MaterialIcons.RestartAlt />
      </IconButton>
    </Box>
  )
}
