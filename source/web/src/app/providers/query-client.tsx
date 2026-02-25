import type { PropsWithChildren } from 'react'
import React from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

export const queryClient = new QueryClient()

type QueryProviderProps = PropsWithChildren

export function QueryProvider({ children }: QueryProviderProps) {
  return (
    <QueryClientProvider client={queryClient} i18nIsDynamicList>
      {children}
    </QueryClientProvider>
  )
}
