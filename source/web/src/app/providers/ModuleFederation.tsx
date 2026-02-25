import React, { createContext, useCallback, useEffect, useState } from 'react'
import {
  loadRemote,
  registerRemotes,
} from '@module-federation/enhanced/runtime'
import type { PropsWithChildren } from 'react'
import { Loader } from 'supernova-core'
import name from '@/config'

type FederationAwareFn<T extends any[], R> = (
  current: App | undefined,
  ...args: T
) => R

interface App {
  name: string
  url: string
  apiUrl: string
  exposedModules?: string[]
  [x: string]: string | unknown
}

type ModuleFederationProviderProps = {
  apps?: App[]
  current?: App
  name?: string
  loadComponents: (...component: string[]) => Record<string, any>
  loadComponent: (component: string) => any
  loadComponentByRemote: (remote: string, component: string) => any
  loading?: boolean
} & PropsWithChildren

const ModuleFederationContext = createContext<ModuleFederationProviderProps>({
  apps: [],
  current: undefined,
  name: '',
  loadComponents: () => ({}),
  loadComponent: () => ({}),
  loadComponentByRemote: () => ({}),
})

function useApps(moduleName: string) {
  const [apps, setApps] = useState<App[]>([])
  const [data, setData] = useState<App[]>([])
  const [current, setCurrent] = useState<App>()
  const [loadedComponents, setLoadedComponents] = useState<
    Record<string, any[]>
  >({})
  const [loading, setLoading] = useState(false)

  const globalAppsKey = '__ALL_APPS__'
  const globalComponentsKey = '__MF_COMPONENTS__'

  useEffect(() => {
    const initial = async () => {
      try {
        if ((window as any)[globalAppsKey]) {
          setData((window as any)[globalAppsKey])
          return
        }

        const localOverride = localStorage.getItem('mfConfigOverride')
        if (localOverride) {
          const parsed = JSON.parse(localOverride);
          (window as any)[globalAppsKey] = parsed
          setData(parsed)
          return
        }

        const result = await fetch('/config.json')
        if (result.ok) {
          const response = await result.json();
          (window as any)[globalAppsKey] = response
          setData(response)
        }
      }
      catch (error) {
        console.error('Error loading module federation configuration:', error)
      }
    }

    initial()
  }, [])

  useEffect(() => {
    if (data.length > 0) {
      const currentApp = data.find(c => c.name === moduleName)
      const otherApps = data.filter(c => c.name !== moduleName)

      registerRemotes(
        [...otherApps, currentApp!].map(app => ({
          name: app?.name,
          entry: `${app?.url}/remoteEntry.js`,
        })),
        {
          force: true,
        },
      )

      setCurrent(currentApp)
      setApps(otherApps)
    }
  }, [data, moduleName])

  const loadModule = useCallback(async (remoteName: string) => {
    const global = ((window as any)[globalComponentsKey] ||= {})

    if (global[remoteName]) {
      setLoadedComponents(prev => ({
        ...prev,
        [remoteName]: global[remoteName],
      }))
      return global[remoteName]
    }

    try {
      const Elements = await loadRemote<any>(remoteName as any, {
        from: 'runtime',
      })

      global[remoteName] = Elements

      setLoadedComponents(prev => ({
        ...prev,
        [remoteName]: Elements,
      }))

      return Elements
    }
    catch (error) {
      console.error(`Error loading remote module ${remoteName}:`, error)
      throw error
    }
  }, [])

  const findComponent = useCallback(
    (component: string) => {
      for (const key of Object.keys(loadedComponents)) {
        const module = loadedComponents[key] as Record<string, any>
        if (module && Object.prototype.hasOwnProperty.call(module, component)) {
          return module[component]
        }
      }
      return undefined
    },
    [loadedComponents],
  )

  const findComponentByRemote = useCallback(
    (remote: string, component: string) => {
      for (const key of Object.keys(loadedComponents)) {
        if (!key.startsWith(remote))
          continue
        const module = loadedComponents[key] as Record<string, any>
        if (module && Object.prototype.hasOwnProperty.call(module, component)) {
          return module[component]
        }
      }
      return undefined
    },
    [loadedComponents],
  )

  const loadComponents = useCallback(
    (...components: string[]) => {
      return components.reduce(
        (acc, component) => {
          const loadedComponent = findComponent(component)
          if (loadedComponent) {
            acc[component] = loadedComponent
          }
          return acc
        },
        {} as Record<string, any>,
      )
    },
    [findComponent],
  )

  const loadComponentByRemote = useCallback(
    (remote: string, component: string) => {
      return findComponentByRemote(remote, component)
    },
    [findComponentByRemote],
  )

  const loadComponent = useCallback(
    (component: string) => {
      return findComponent(component)
    },
    [findComponent],
  )
  useEffect(() => {
    if (current?.exposedModules?.length) {
      setLoading(true)
      const loadAllModules = async () => {
        for (const module of current.exposedModules!) {
          await loadModule(module)
        }
        setLoading(false)
      }

      loadAllModules()
    }
  }, [current, loadModule])

  useEffect(() => {
    if (!current)
      return

    setLoading(true)

    const discoverAll = async () => {
      try {
        if (current && current.name !== 'web_platform_core') {
          try {
            // fetch exposes.json
            const exposes = await fetch(`${current.url}/exposes.json`).then(
              r => r.json(),
            )

            // keys of exposes are module names like "./Event"
            const moduleNames = Object.keys(exposes).map(key =>
              key.replace('./', ''),
            )

            // load all modules
            await Promise.all(
              moduleNames.map(mod => loadModule(`${current.name}/${mod}`)),
            )
          }
          catch (err) {
            console.error(
              `[MF] Failed to load exposes.json for ${current.name}`,
              err,
            )
          }
        }
      }
      finally {
        setLoading(false)
      }
    }

    discoverAll()
  }, [current, apps, loadModule])

  return {
    apps,
    current,
    name: moduleName,
    loadComponents,
    loadComponentByRemote,
    loadComponent,
    loading: !apps || apps.length === 0 || !moduleName || !current || loading,
    loadedComponents,
  }
}

function ModuleFederationProvider({
  children,
  name,
}: Partial<ModuleFederationProviderProps>) {
  const {
    apps,
    current,
    loadComponents,
    loadComponent,
    loadComponentByRemote,
    loading,
  } = useApps(name!)

  const contextValue = React.useMemo(
    () => ({
      apps,
      current,
      loadComponents,
      loadComponent,
      loadComponentByRemote,
    }),
    [apps, current, loadComponents, loadComponent, loadComponentByRemote],
  )

  if (loading) {
    return <Loader />
  }

  return (
    <ModuleFederationContext.Provider value={contextValue}>
      {children}
    </ModuleFederationContext.Provider>
  )
}

function useModuleFederation(name?: string) {
  const context = React.useContext(ModuleFederationContext)
  const fallback = useApps(name || 'default')
  return context.apps?.length === 0 ? fallback : context
}

function withModuleFederationContext<T extends any[], R>(
  fn: FederationAwareFn<T, R>,
): (...args: T) => R {
  return (...args: T) => {
    const { current } = useModuleFederation(name)
    return fn(current, ...args)
  }
}

export {
  ModuleFederationProvider,
  ModuleFederationContext,
  useModuleFederation,
  withModuleFederationContext,
}
