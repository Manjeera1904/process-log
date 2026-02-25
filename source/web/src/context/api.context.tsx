import React, { createContext, useContext, useMemo } from 'react'
import type { FetchApiParams } from '@/shared/api/fetch'
import { fetchApi } from '@/shared/api/fetch'

interface ApiContextProps<T> {
  client?: (payload: FetchApiParams<T>) => Promise<T> | null
  children?: React.ReactNode
}

const ApiContext = createContext<ApiContextProps<any> | null>(null)

export const ApiContextProvider: React.FC<ApiContextProps<any>> = ({
  children,
}) => {
  const value = useMemo(() => ({ client: fetchApi }), [])
  return <ApiContext.Provider value={value}>{children}</ApiContext.Provider>
}

export function useApiContext() {
  const context = useContext(ApiContext)
  if (!context) {
    throw new Error('useApiContext must be used within a ApiContextProvider')
  }
  return context
}
