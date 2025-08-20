import { useLocale as useLocaleIntl } from "next-intl"

// Define supported locales without Hygraph dependency
export type Locale = "en" | "es" | "fr" | "de" | "it" | "pt" | "ja" | "ko" | "zh" | "ar"

const locales: Locale[] = ["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ar"]

const defaultLocale: Locale = "en"

export const useLocale = () => useLocaleIntl() as Locale

// Backward compatibility function for Hygraph locale conversion
export const hygraphLocaleToStandardNotation = (locale: string): Locale => {
  // Convert Hygraph locale format to standard locale
  const localeMap: Record<string, Locale> = {
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ja': 'ja',
    'ko': 'ko',
    'zh': 'zh',
    'ar': 'ar',
  }
  
  return localeMap[locale] || 'en'
}

export const i18n = {
  locales,
  defaultLocale,
}
