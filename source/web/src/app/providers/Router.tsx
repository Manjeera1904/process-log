import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { ToasterProvider } from 'supernova-core'
import { ApiContextProvider } from '@/context/api.context'
import { ProcessLogPage } from '@/pages'
import { MainLayout } from '@/shared/layouts'
import EventContextProvider from '@/shared/context/event.context'
import { ProcessFiltersProvider } from '@/context/ProcessFiltersContext'

export function RouterProcessLog() {
  return (
    <EventContextProvider>
      <ApiContextProvider>
        <ToasterProvider>
          <BrowserRouter basename="/process-log">
            <Routes>
              <Route path="/" element={<MainLayout />}>
                <Route
                  path="/"
                  element={(
                    <ProcessFiltersProvider>
                      <ProcessLogPage />
                    </ProcessFiltersProvider>
                  )}
                />
              </Route>
            </Routes>
          </BrowserRouter>
        </ToasterProvider>
      </ApiContextProvider>
    </EventContextProvider>
  )
}
