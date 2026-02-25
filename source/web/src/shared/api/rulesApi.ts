import { fetchApi } from './fetch'
import type { RuleRequestDto } from '@/types/rules'

const API_VERSION = '1.0'

export async function triggerRule(
  apiUrl: string,
  token: string,
  payload: RuleRequestDto,
): Promise<any[]> {
  const response = await fetchApi<any[]>({
    apiUrl,
    method: 'POST',
    data: payload,
    url: 'rules-engine-facade/evaluate',
    token,
    params: { 'api-version': API_VERSION },
    headers: { 'X-EI-ClientId': payload.clientId },
  })

  return response
}
