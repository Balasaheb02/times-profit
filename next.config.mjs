import withBundleAnalyzer from "@next/bundle-analyzer"
import withPlugins from "next-compose-plugins"
import withNextIntl from "next-intl/plugin"
import { env } from "./src/env.mjs"

/**
 * @type {import('next').NextConfig}
 */
const config = withPlugins(
  [[withBundleAnalyzer({ enabled: env.ANALYZE })]],
  withNextIntl("./i18n.ts")({
    reactStrictMode: true,
    eslint: {
      // Disable ESLint during builds on Vercel
      ignoreDuringBuilds: true,
    },
    typescript: {
      // Disable TypeScript type checking during builds on Vercel
      ignoreBuildErrors: true,
    },
    images: {
      domains: ['images.unsplash.com'],
      remotePatterns: [
        {
          protocol: "https",
          hostname: "images.unsplash.com",
        },
        {
          protocol: "https",
          hostname: "images.unsplash.com",
        },
        {
          protocol: "https",
          hostname: "example.com",
        }
      ],
    },
    env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "https://api.timesprofit.com/api",
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL || "https://timesprofit.com",
  }
  })
)

export default config
