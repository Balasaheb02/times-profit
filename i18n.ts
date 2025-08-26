// static i18n configuration - English only for deployment
import { getRequestConfig } from 'next-intl/server';

// Force English only - keeps folder structure but only builds EN
export const locales = ['en'];
export const defaultLocale = 'en';

export default getRequestConfig(async ({ locale }) => ({
  messages: {
    // Simple English messages
    'header.home': 'Home',
    'header.about': 'About', 
    'footer.copyright': '© 2025 Times Profit',
    'showing': 'Showing',
    'resultsFor': 'results for',
  }
}));
