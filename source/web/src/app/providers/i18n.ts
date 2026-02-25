import i18next from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import general from './locales/en/general.json'
import processMonitor from './locales/en/processMonitor.json'

export const resources = {
  en: {
    general,
    processMonitor,
  },
} as const

export const defaultNS = 'general'

const appI18Next = i18next.createInstance({
  resources,
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
  defaultNS,
})
appI18Next.use(LanguageDetector).use(initReactI18next).init()

export const i18n = appI18Next
