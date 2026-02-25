import React, { useCallback, useEffect, useMemo, useState } from 'react'
import {
  Box,
  DynamicTableServerSide,
  Loader,
  MaterialIcons,
  useSuperNovaTheme,
  useTokenPermission,
} from 'supernova-core'
import { useTranslation } from 'react-i18next'
import type {
  DynamicTableHeaderProps,
  DynamicTableRowProps,
} from 'supernova-core/dist/components/DynamicTable/DynamicTable'
import { useClientMethod } from 'react-use-signalr'
import { HubConnectionState } from '@microsoft/signalr'
import { jwtDecode } from 'jwt-decode'
import DynamicComponent from '@/shared/DynamicApp'
import { ProcessState } from '@/constants/enums'
import useSignalR from '@/shared/hooks/useSignalR'
import type { LoadComponentAction, SignalRResponse } from '@/types/rules'

interface ProcessItem {
  type: string
  id: string
  description: string
  client: string
  source: string
  processedOn: string
  duration: string
  state: ProcessState
  docs?: number
  disposition?: string
}

interface ActivityType {
  id: string
  type: string
  name: string
  description: string
}

interface ProcessStatus {
  id: string
  status: string
  name: string
  description: string
}

interface DecodedToken {
  sub?: string
  [key: string]: any
}

interface ProcessMonitorListTableProps {
  tokenClientId: string
  data: ProcessItem[]
  totalRows: number
  page: number
  rowsPerPage: number
  onPageChange: (page: number) => void
  onRowsPerPageChange: (rowsPerPage: number) => void
  loading?: boolean
  order?: 'asc' | 'desc'
  orderBy?: string
  filterText: string
  onSortChange?: (columnId: string) => void
  onFilterChange?: (filter: string) => void
  onExpand?: (
    index: number,
    row: Record<string, unknown>,
    isExpanded: boolean,
  ) => void
  activityTypes: ActivityType[]
  processStatuses: ProcessStatus[]
}

export function ProcessMonitorListTable({
  tokenClientId,
  data,
  totalRows,
  page,
  rowsPerPage,
  onPageChange,
  onRowsPerPageChange,
  loading,
  order,
  filterText,
  orderBy,
  onSortChange,
  onFilterChange,
  activityTypes,
  processStatuses,
}: ProcessMonitorListTableProps) {
  const theme = useSuperNovaTheme()
  const { token } = useTokenPermission()
  const [rowId, setRowId] = useState<string>('')
  const { connection: signalRConnection, hubConnectionState } = useSignalR()
  const clientTargetMethod = 'onProcessLogExpand'
  const clientTargetMethodError = 'onProcessLogExpandError'

  const [socketId, setSocketId] = useState<string>('')

  const { t } = useTranslation('processMonitor')

  const decodedToken = useMemo(() => {
    if (!token)
      return null
    try {
      return jwtDecode<DecodedToken>(token)
    }
    catch (error) {
      console.error('Failed to decode token:', error)
      return null
    }
  }, [token])

  const [components, setComponents] = useState<{
    [key: string]: { name: string, props: any, remote: string } | null
  }>({})

  const activityTypeMap = useMemo(
    () =>
      Object.fromEntries((activityTypes ?? []).map(at => [at.type, at.name])),
    [activityTypes],
  )

  const processStatusMap = useMemo(
    () =>
      Object.fromEntries(
        (processStatuses ?? []).map(ps => [ps.status, ps.name]),
      ),
    [processStatuses],
  )

  useEffect(() => {
    if (
      hubConnectionState === HubConnectionState.Connected
      && signalRConnection?.connectionId
    ) {
      setSocketId(signalRConnection.connectionId)
    }
  }, [hubConnectionState, signalRConnection])

  const columns = useMemo(() => {
    const iconStyleSx = {
      fontSize: 18,
      color: theme.palette.text.secondary,
    }

    return [
      {
        label: '',
        identifier: 'collapse',
        sort: true,
        width: 24,
        sx: {
          padding: '0 2px',
          textAlign: 'center',
          minWidth: '24px',
          maxWidth: '32px',
        },
        columnDataType: 'string',
      },

      {
        label: t('columns.type'),
        identifier: 'type',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => (
          <Box
            sx={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              maxWidth: '100%',
            }}
          >
            {activityTypeMap[obj.type] || obj.type}
          </Box>
        ),
        columnDataType: 'string',
      },

      {
        label: t('columns.id'),
        identifier: 'id',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => (
          <Box
            sx={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              maxWidth: '100%',
            }}
          >
            {obj.id}
          </Box>
        ),
        columnDataType: 'string',
      },

      {
        label: t('columns.description'),
        identifier: 'description',
        sort: true,
        render: (obj: ProcessItem) => {
          const text = obj.description
            .split(',')
            .map(s => s.trim())
            .filter(Boolean)
            .join(', ')

          return (
            <Box
              sx={{
                whiteSpace: 'normal',
                wordBreak: 'break-word',
                overflowWrap: 'anywhere',
                lineHeight: 1.5,
                maxWidth: '100%',
              }}
            >
              {text}
            </Box>
          )
        },
        columnDataType: 'string',
      },

      {
        label: t('columns.client'),
        identifier: 'client',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => obj.client,
        columnDataType: 'string',
      },

      {
        label: t('columns.source'),
        identifier: 'source',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => obj.source,
        columnDataType: 'string',
      },

      {
        label: t('columns.processedOn'),
        identifier: 'processedOn',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => obj.processedOn,
        columnDataType: 'string',
      },

      {
        label: t('columns.duration'),
        identifier: 'duration',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => obj.duration,
        columnDataType: 'string',
      },

      {
        label: t('columns.state'),
        identifier: 'state',
        sort: true,
        tooltip: false,
        render: (obj: ProcessItem) => {
          let icon = null
          const iconSx = { fontSize: 16, mr: 0 }
          const statusName = processStatusMap[obj.state] || obj.state

          switch (obj.state) {
            case ProcessState.New:
            case ProcessState.Pending:
              icon = (
                <MaterialIcons.Pending
                  sx={{ ...iconSx, color: theme.palette.text.disabled }}
                />
              )
              break
            case ProcessState.InProgress:
              icon = (
                <MaterialIcons.Timelapse
                  sx={{ ...iconSx, color: theme.palette.warning.main }}
                />
              )
              break
            case ProcessState.Completed:
              icon = (
                <MaterialIcons.CheckCircle
                  sx={{ ...iconSx, color: theme.palette.success.main }}
                />
              )
              break
            case ProcessState.Failed:
              icon = (
                <MaterialIcons.Error
                  sx={{ ...iconSx, color: theme.palette.error.main }}
                />
              )
              break
          }

          return (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, maxWidth: '120px' }}>
              {icon}
              <Box
                component="span"
                sx={{
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: 'inline-block',
                  maxWidth: '100%',
                }}
              >
                {statusName}
              </Box>
            </Box>
          )
        },
        columnDataType: 'string',
      },

      {
        label: t('columns.disposition'),
        identifier: 'disposition',
        sort: true,
        width: 120,
        tooltip: false,
        render: (obj: ProcessItem) => {
          const totalSegments = 20
          let percentage = 0
          let barColor = theme.palette.error.main

          switch (obj.state) {
            case ProcessState.Completed:
              percentage = 100
              break
            case ProcessState.InProgress:
              percentage = Math.floor(Math.random() * 61) + 20
              break
            case ProcessState.New:
            case ProcessState.Pending:
              percentage = 0
              break
            case ProcessState.Failed:
              percentage = 100
              barColor = theme.palette.error.main
              break
          }

          const filledSegments = Math.round((percentage / 100) * totalSegments)

          return (
            <Box sx={{ display: 'flex', alignItems: 'center', cursor: 'default' }}>
              {Array.from({ length: totalSegments }).map((_, i) => {
                const segmentId = `${obj.id}-segment-${i < filledSegments ? 'filled' : 'empty'}-${i < filledSegments}`

                return (
                  <Box
                    key={segmentId}
                    sx={{
                      width: '4px',
                      height: '16px',
                      backgroundColor: i < filledSegments ? barColor : theme.palette.divider,
                      marginRight: '2px',
                      borderRadius: '2px',
                    }}
                  />
                )
              })}
            </Box>
          )
        },
        columnDataType: 'string',
      },

      {
        label: '',
        identifier: 'filePresent',
        sort: true,
        width: 24,
        sx: {
          padding: '0 2px',
          textAlign: 'center',
          minWidth: '24px',
        },
        tooltip: false,
        render: (obj: ProcessItem) => (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4 }}>
            <MaterialIcons.FilePresent sx={iconStyleSx} />
            <span>{obj.docs ?? 2}</span>
          </div>
        ),
        columnDataType: 'number',
      },

      {
        label: '',
        identifier: 'actionIcon',
        sort: true,
        width: 24,
        sx: {
          padding: '0 2px',
          textAlign: 'center',
          minWidth: '24px',
          maxWidth: '32px',
        },
        render: (obj: ProcessItem) => {
          const icon
            = obj.state === ProcessState.Failed
              ? <MaterialIcons.SaveAlt sx={iconStyleSx} />
              : <MaterialIcons.Visibility sx={iconStyleSx} />

          return <div style={{ display: 'flex', justifyContent: 'center' }}>{icon}</div>
        },
        columnDataType: 'string',
      },
    ]
  }, [theme.palette, t, activityTypeMap, processStatusMap])

  const callRule = useCallback(
    (socketId: string, payload: Record<string, unknown>) => {
      const data = {
        connection: {
          connectionId: socketId,
          clientTargetMethod,
          clientTargetMethodError,
        },
        clientId: tokenClientId,
        endpointKey: 'web_process_log',
        applicationComponentKey: 'ProcessMonitorListTable',
        applicationComponentVersion: '6a318ba4-f7f8-4da3-9d3c-93b31ea52448',
        currentRoute: '/process-monitoring/list',
        version: '1.0',
        eventName: 'Expand',
        eventType: 'Expand',
        productId: 'd17a34b0-0d5d-4c24-a5a0-9f8bc1c44798',
        userId: decodedToken?.sub as string,
        payload,
      }
      signalRConnection?.invoke('EvaluateComponentRules', data)
    },
    [
      clientTargetMethod,
      clientTargetMethodError,
      signalRConnection,
      tokenClientId,
      decodedToken?.sub,
    ],
  )

  const onExpand = useCallback(
    (_index: number, row: Record<string, unknown>, isExpanded: boolean) => {
      if (!isExpanded) {
        setComponents((prev) => {
          const newComp = { ...prev }
          delete newComp[row.id as string]
          return newComp
        })
        setRowId('')
      }
      else {
        setRowId(row.id as string)
        callRule(socketId, row)
      }
    },
    [socketId, callRule],
  )

  useClientMethod(
    signalRConnection!,
    clientTargetMethod,
    (_correlationId, apiResponse: SignalRResponse) => {
      const [firstAction] = apiResponse.actions as LoadComponentAction[]
      if (!firstAction)
        return

      setComponents(prev => ({
        ...prev,
        [rowId]: {
          name: firstAction.componentData?.componentKey,
          props: firstAction.componentData?.properties,
          remote: firstAction.componentData?.endpointKey,
        },
      }))
    },
  )

  useClientMethod(signalRConnection!, clientTargetMethodError, (error) => {
    console.error('Error received from SignalR:', error)
  })

  if (!socketId) {
    return <Loader />
  }

  return (
    <Box
      sx={{
        '& td:has(.expanded-row)': {
          padding: '0!important',
        },

        '& .MuiTable-root': {
          tableLayout: 'auto',
        },

        '& .MuiTableCell-root:first-of-type': {
          width: '20px',
          minWidth: '20px',
          maxWidth: '20px',
          padding: '0px',
          paddingLeft: '8px',
        },
        '& .MuiTableCell-root:nth-last-of-type(1)': {
          width: '32px',
          minWidth: '32px',
          maxWidth: '32px',
        },
        '& .MuiTableCell-root:nth-last-of-type(2)': {
          width: '50px',
          minWidth: '50px',
          maxWidth: '50px',
        },
      }}
    >
      <DynamicTableServerSide
        {...{
          totalRows,
          page,
          rowsPerPage,
          onPageChange,
          onRowsPerPageChange,
          loading,
          order,
          orderBy,
          onSortChange,
          filterText,
          onFilterChange,
          columns: columns as DynamicTableHeaderProps[],
          data: data as unknown as DynamicTableRowProps[],
          onExpand,
          renderExpansion: (_rowIndex, rowData) =>
            components[rowData.id as string]
              ? (
                  <DynamicComponent
                    remoteName={components[rowData.id as string]!.remote}
                    componentName={components[rowData.id as string]!.name}
                    {...components[rowData.id as string]!.props}
                  />
                )
              : null,
        }}
      />
    </Box>
  )
}

export default ProcessMonitorListTable
