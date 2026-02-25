import * as signalR from '@microsoft/signalr'
import { useTokenPermission } from 'supernova-core'
import { useEffect, useState } from 'react'
import { useHub } from 'react-use-signalr'
import { useModuleFederation } from '@/app/providers/ModuleFederation'
import name from '@/config'

function useSignalR() {
  const { token } = useTokenPermission()
  const { current } = useModuleFederation(name)
  const [connection, setConnection] = useState<signalR.HubConnection | null>(
    null,
  )

  const url = current!.signalRUrl as string

  if (!url) {
    throw new Error('SignalR URL not found in module federation config')
  }

  const { hubConnectionState } = useHub(connection!)

  useEffect(() => {
    if (!token) {
      throw new Error('Token not found for SignalR connection')
    }
    if (!url) {
      throw new Error('SignalR URL not found in module federation config')
    }
    setConnection(
      new signalR.HubConnectionBuilder()
        .withUrl(url, {
          withCredentials: false,
          accessTokenFactory: () => token, // JWT Token
        })
        .withAutomaticReconnect({
          nextRetryDelayInMilliseconds: _retryContext => 1000,
        })
        .withServerTimeout(180000) // 3 minutes
        .build(),
    )
  }, [token, url])

  return { connection, hubConnectionState }
}

export default useSignalR
