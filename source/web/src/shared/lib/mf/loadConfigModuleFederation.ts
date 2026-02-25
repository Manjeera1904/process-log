import process from 'node:process'
import * as v from 'valibot'

export const configModuleFederationSchema = v.object({
  web_platform_core: v.pipe(v.string(), v.minLength(2), v.url()),
  web_user_work_queues: v.pipe(v.string(), v.minLength(2), v.url()),
  api_platform_core: v.pipe(v.string(), v.minLength(2), v.url()),
  api_eclipse_analytics: v.pipe(v.string(), v.minLength(2), v.url()),
  web_eclipse_analytics: v.pipe(v.string(), v.minLength(2), v.url()),
  web_process_log: v.pipe(v.string(), v.minLength(2), v.url()),
})

export type ConfigModuleFederation = v.InferOutput<
  typeof configModuleFederationSchema
>

export async function loadConfigModuleFederation() {
  try {
    let updatedData: Record<string, string> = {}

    const response = await fetch('/url.json')
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    const data = await response.json()

    if (process.env.NODE_ENV !== 'development') {
      // Define key patterns for dynamic processing
      const keyMapping: Record<string, string> = {
        web_platform_core: 'aca-platform-core-web',
        web_user_work_queues: 'aca-work-queues',
        api_platform_core: 'aca-platform-core-api',
        api_eclipse_analytics: 'aca-eclipse-analytics-api',
        web_eclipse_analytics: 'aca-eclipse-analytics-web',
        web_process_log: 'aca-process-logging-web',
      }

      // Dynamically process the data to ensure https for fdqn keys
      const processedData = Object.keys(data).reduce(
        (acc: Record<string, string>, key) => {
          if (key.endsWith('fdqn')) {
            acc[key] = data[key].startsWith('http')
              ? data[key]
              : `https://${data[key] || ''}`
          }
          else {
            acc[key] = data[key]
          }
          return acc
        },
        {},
      )

      // Assign processed values to the respective logical keys
      updatedData = Object.entries(keyMapping).reduce(
        (acc: Record<string, string>, [logicalKey, keyPattern]) => {
          const matchedKey = Object.keys(processedData).find(
            key => key.startsWith(keyPattern) && key.endsWith('fdqn'),
          )
          if (matchedKey) {
            acc[logicalKey] = processedData[matchedKey]
          }
          return acc
        },
        {},
      )
    }
    else {
      // Use environment variables in development
      updatedData = {
        web_platform_core:
          data.web_platform_core || process.env.REACT_APP_WEB_PLATFORM_CORE_URL,
        web_user_work_queues:
          data.web_user_work_queues
          || process.env.REACT_APP_WEB_USER_WORK_QUEUES_URL,
        api_platform_core:
          data.api_platform_core || process.env.REACT_APP_PLATFORMCOREAPI,
        web_eclipse_analytics:
          data.web_eclipse_analytics
          || process.env.REACT_APP_WEB_ECLIPSE_ANALYTICS_URL,
        api_eclipse_analytics:
          data.api_eclipse_analytics
          || process.env.REACT_APP_API_ECLIPSE_ANALYTICS_URL,
        web_process_log:
          data.web_process_log || process.env.REACT_APP_WEB_PROCESS_LOG_URL,
      }
    }

    console.warn(updatedData)

    // Validate the updated data against the schema
    const result = v.safeParse(configModuleFederationSchema, updatedData)

    if (result.success) {
      return result.output
    }
    else {
      throw new v.ValiError(result.issues)
    }
  }
  catch (error) {
    console.error('Failed to load configuration:', error)
    throw error
  }
}
