import type { ReactNode } from 'react'
import React, { createContext, useEffect, useMemo, useState } from 'react'

import { useModuleFederation } from '@/app/providers/ModuleFederation'

interface EventContextProps {
  breadcumbRef?: HTMLDivElement
}

const EventContext = createContext<EventContextProps>({})

function EventContextProvider(props: { children: ReactNode }) {
  const { children } = props
  const { loadComponent } = useModuleFederation('web_platform_core')
  const EventStore = loadComponent('EventStore')

  const [container, setContainer] = useState<HTMLDivElement>()

  useEffect(() => {
    if (!EventStore)
      return

    const handleRef = (ref: HTMLDivElement) => {
      if (ref)
        setContainer(ref)
    }

    EventStore.onHeaderRef(handleRef)

    return () => {
      EventStore.offHeaderRef(handleRef)
    }
  }, [EventStore])

  const contextValue = useMemo<EventContextProps>(
    () => ({
      breadcumbRef: container,
    }),
    [container],
  )

  return (
    <EventContext.Provider value={contextValue}>
      {children}
    </EventContext.Provider>
  )
}

export default EventContextProvider
export { EventContext }
