import React, { useEffect, useState } from 'react'
import { Loader } from 'supernova-core'
import { useModuleFederation } from '@/app/providers/ModuleFederation'
import name from '@/config'

interface DynamicComponentProps {
  remoteName: string
  componentName: string
  [key: string]: unknown
}

function DynamicComponent(props: DynamicComponentProps) {
  const { componentName, remoteName, ...rest } = props
  const { loadComponentByRemote } = useModuleFederation(name)

  const [LoadedComponent, setComponent] = useState<{
    default: React.ComponentType | null
  }>({
    default: null,
  })

  useEffect(() => {
    const load = async () => {
      const Elements = await loadComponentByRemote(remoteName, componentName)
      setComponent({
        default: Elements,
      })
    }
    if (componentName) {
      load()
    }
  }, [componentName, loadComponentByRemote, remoteName])

  if (!LoadedComponent) {
    return <Loader />
  }

  return LoadedComponent.default ? <LoadedComponent.default {...rest} /> : null
}

export default DynamicComponent
