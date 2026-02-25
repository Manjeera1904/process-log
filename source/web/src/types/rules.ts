interface ConnectionDto {
  connectionId: string
  clientTargetMethod: string
  clientTargetMethodError: string
}

interface RuleRequestDto {
  clientId: string
  connection: ConnectionDto
  productId: string
  endpointKey: string
  applicationComponentKey: string
  applicationComponentVersion: string
  eventType: string
  eventName: string
  userId: string
  version: string
  currentRoute: string
  payload?: Record<string, unknown>
}

interface RequestDtoException {
  message: string
}

interface RulesResponseDto {
  message?: string
  error?: string
}

interface StartTaskResponseDto extends RulesResponseDto {
  dateTime: Date
  correlationId: string
  status: string
}

interface TaskCompletedResponseDto extends RulesResponseDto {
  finishedAt: Date
  payload: Record<string, unknown>
}

interface Action {
  name: string
}

interface SignalRResponse {
  actions: Action[]
}

interface ComponentData {
  componentKey: string
  endpointKey: string
  properties: Record<string, unknown>
}

interface LoadComponentAction extends Action {
  componentData: ComponentData
}

export type {
  RuleRequestDto,
  RulesResponseDto,
  StartTaskResponseDto,
  TaskCompletedResponseDto,
  SignalRResponse,
  LoadComponentAction,
  RequestDtoException,
}
