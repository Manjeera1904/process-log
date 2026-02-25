import React from 'react'

import { Providers } from './providers'
import { ModuleFederationProvider } from './providers/ModuleFederation'
import name from '@/config'

export function AppProcessLog() {
  return (
    <ModuleFederationProvider name={name}>
      <Providers />
    </ModuleFederationProvider>
  )
}
