import React, { useContext, useMemo } from 'react'
import { atom, useAtomValue } from 'jotai'
import { Breadcumb } from 'supernova-core'
import { createPortal } from 'react-dom'
import { EventContext } from '@/shared/context/event.context'

export const reportAtom = atom('')

interface Breadcrumb {
  href?: string
  label: string
}

interface BreadcrumbsProps {
  baseBreadcrumbs: Breadcrumb[]
}

export function Breadcrumbs({ baseBreadcrumbs }: BreadcrumbsProps) {
  const currentReportName = useAtomValue(reportAtom)
  const { breadcumbRef } = useContext(EventContext)
  const items = useMemo(() => {
    const result: Breadcrumb[] = [...baseBreadcrumbs]
    if (currentReportName && currentReportName.length > 0) {
      result.push({
        label: currentReportName,
      })
    }
    return result
  }, [baseBreadcrumbs, currentReportName])

  return (
    breadcumbRef
    && createPortal(<Breadcumb items={items} />, breadcumbRef as Element)
  )
}
