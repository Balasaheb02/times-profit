// static i18n configuration - English only for deployment
import { getRequestConfig } from 'next-intl/server';

// Force English only - keeps folder structure but only builds EN
export const locales = ['en'];
export const defaultLocale = 'en';

export default getRequestConfig(async () => {
  // Static configuration for English only
  return {
    locale: 'en',
    messages: {
      // Nested object structure (not flat keys with dots)
      header: {
        home: 'Home',
        about: 'About'
      },
      footer: {
        copyright: '© 2025 Times Profit'
      },
      showing: 'Showing',
      resultsFor: 'results for',
    }
  };
});
