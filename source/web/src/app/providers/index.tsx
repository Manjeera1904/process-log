import React from 'react'
import './i18n'
import { ThemeProvider, ToasterProvider } from 'supernova-core'
import { QueryProvider } from './query-client'
import { RouterProcessLog } from './Router'
import theme from '@/theme'

export function Providers() {
  return (
    <ThemeProvider theme={theme}>
      <QueryProvider>
        <ToasterProvider>
          <RouterProcessLog />
        </ToasterProvider>
      </QueryProvider>
    </ThemeProvider>
  )
}
