import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'
import {
  loadFromStorage,
  saveToStorage,
} from '@/shared/utils/localStorageHelpers'

export interface ProcessFilters {
  client: string | undefined
  activityType: string
  dateRange: string
  states: string[]
  sortBy: string
  sortDirection: 'asc' | 'desc'
  pageNumber: number
  pageSize: number
  timeZone: string
}

const DEFAULT_FILTERS: ProcessFilters = {
  client: undefined,
  activityType: '',
  dateRange: 'Today',
  states: [],
  sortBy: 'processedOn',
  sortDirection: 'desc',
  pageNumber: 1,
  pageSize: 20,
  timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
}

interface FilterContextValue {
  filters: ProcessFilters
  setFilters: React.Dispatch<React.SetStateAction<ProcessFilters>>
  updateFilters: (updates: Partial<ProcessFilters>) => void
}

const ProcessFiltersContext = createContext<FilterContextValue | undefined>(
  undefined,
)

export function ProcessFiltersProvider({
  children,
}: {
  children: React.ReactNode
}) {
  const savedFilters = loadFromStorage<ProcessFilters>(
    'processFilters',
    DEFAULT_FILTERS,
  )

  const [filters, setFilters] = useState<ProcessFilters>(savedFilters)

  useEffect(() => {
    saveToStorage('processFilters', filters)
  }, [filters])

  const updateFilters = (updates: Partial<ProcessFilters>) => {
    setFilters((prev) => {
      const newFilters = { ...prev, ...updates }

      if (
        Object.keys(updates).some(
          key => key !== 'pageNumber' && key !== 'pageSize',
        )
      ) {
        newFilters.pageNumber = 1
      }
      return newFilters
    })
  }

  const value = useMemo(
    () => ({ filters, setFilters, updateFilters }),
    [filters],
  )

  return (
    <ProcessFiltersContext.Provider value={value}>
      {children}
    </ProcessFiltersContext.Provider>
  )
}

export function useProcessFilters() {
  const ctx = useContext(ProcessFiltersContext)
  if (!ctx) {
    throw new Error(
      'useProcessFilters must be used inside ProcessFiltersProvider',
    )
  }
  return ctx
}
