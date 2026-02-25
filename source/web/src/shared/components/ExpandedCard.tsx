import React from 'react'
import { Box, MaterialIcons, useSuperNovaTheme } from 'supernova-core'
import { useTranslation } from 'react-i18next'
import type { SxProps, Theme } from '@mui/material/styles'
import type expandedCardContent from '@/shared/const/mockExpandedCardData.json'

type ExpandedCardData = (typeof expandedCardContent)[number]

type ExpandedCardProps = ExpandedCardData & {
  processLogId: string
  actionType: string
}

export const ExpandedCard: React.FC<ExpandedCardProps> = ({
  dates,
  insurancePayer,
  paymentPolicy,
  rate,
  services,
  summary,
}) => {
  const theme = useSuperNovaTheme()
  const { t } = useTranslation('processMonitor')

  const cardWrapperSx: SxProps<Theme> = {
    display: 'flex',
    flexDirection: 'column',
    pl: 6,
    pr: 4,
    py: 3,
    borderLeft: `2px solid ${theme.palette.primary.main}`,
    backgroundColor: 'background.paper',
    fontSize: 'body1.fontSize',
    color: 'text.primary',
    gap: 2.5,
    position: 'relative',
  }

  const labelSx: SxProps<Theme> = {
    color: 'text.primary',
    fontWeight: 500,
    fontSize: 'body2.fontSize',
    mb: 0.75,
  }

  const summaryTextSx: SxProps<Theme> = {
    color: 'text.secondary',
    display: 'grid',
    gridTemplateColumns: '1fr 2fr',
  }

  return (
    <Box className="expanded-row" sx={cardWrapperSx}>
      <Box
        sx={{
          'display': 'grid',
          'gridTemplateColumns': 'repeat(4, 1fr)',
          'gap': 2.5,
          'alignItems': 'start',
          'width': '100%',
          '@media (max-width: 768px)': {
            gridTemplateColumns: 'repeat(2, 1fr)',
          },
        }}
      >
        <Box sx={{ position: 'relative' }}>
          <MaterialIcons.AutoAwesome
            sx={{
              position: 'absolute',
              top: -5,
              left: '-53px',
              fontSize: 36,
              color: 'primary.main',
              px: 1,
              transform: 'rotate(270deg)',
            }}
          />
          <Box sx={labelSx}>{t('expandedCard.payor')}</Box>
          <Box>{insurancePayer}</Box>
        </Box>

        <Box>
          <Box sx={labelSx}>{t('expandedCard.services')}</Box>
          <Box>{services}</Box>
        </Box>

        <Box>
          <Box sx={labelSx}>{t('expandedCard.rate')}</Box>
          <Box>{rate}</Box>
        </Box>

        <Box>
          <Box sx={labelSx}>{t('expandedCard.dates')}</Box>
          <Box>{dates}</Box>
        </Box>
      </Box>

      <Box
        sx={{
          'display': 'grid',
          'gridTemplateColumns': 'repeat(2, 1fr)',
          'gap': 2.5,
          'mt': 2,
          '@media (max-width: 768px)': {
            gridTemplateColumns: '1fr',
          },
        }}
      >
        <Box>
          <Box sx={labelSx}>{t('expandedCard.summary')}</Box>
          <Box sx={summaryTextSx}>{summary}</Box>
        </Box>

        <Box>
          <Box sx={labelSx}>{t('expandedCard.paymentPolicy')}</Box>
          <Box>{paymentPolicy}</Box>
        </Box>
      </Box>
    </Box>
  )
}
