import { registerRemotes } from '@module-federation/enhanced/runtime'
import type { ConfigModuleFederation } from './loadConfigModuleFederation'

interface RegisterModuleFederationParams {
  modules: Array<keyof ConfigModuleFederation>
  config: ConfigModuleFederation
}

export function registerModuleFederation({
  config,
  modules,
}: RegisterModuleFederationParams) {
  for (const module of modules) {
    registerRemotes([
      {
        name: module,
        entry: `${config[module as keyof ConfigModuleFederation]}/remoteEntry.js`,
      },
    ])
  }
}
