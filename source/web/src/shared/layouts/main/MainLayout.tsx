import { Outlet } from 'react-router-dom'
import React from 'react'
import { Box } from 'supernova-core'
import { Breadcrumbs } from '@/widgets/breadcrumbs'
import { routsUrl } from '@/routes'

export function MainLayout() {
  return (
    <Box
      sx={{
        display: 'flex',
        width: '100%',
        marginTop: '60px',
        overflow: 'hidden',
      }}
    >
      <Box
        sx={{
          padding: 2,
          width: '100%',
          overflowY: 'auto',
          height: 'calc(100vh - 60px)',
        }}
      >
        <Breadcrumbs
          baseBreadcrumbs={[
            {
              href: routsUrl.home,
              label: 'Home',
            },
            {
              href: routsUrl.processLog,
              label: 'Process Monitor',
            },
          ]}
        />
        <Outlet />
      </Box>
    </Box>
  )
}
