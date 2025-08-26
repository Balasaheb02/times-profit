import { useLocale as useLocaleIntl } from "next-intl"

// Define supported locales without Hygraph dependency - English only for now
export type Locale = "en"

const locales: Locale[] = ["en"]

const defaultLocale: Locale = "en"

export const useLocale = () => useLocaleIntl() as Locale

// Backward compatibility function for Hygraph locale conversion - now defaults to English
export const hygraphLocaleToStandardNotation = (locale: string): Locale => {
  // Convert any locale to English since we only support English now
  return 'en'
}

export const i18n = {
  locales,
  defaultLocale,
}
