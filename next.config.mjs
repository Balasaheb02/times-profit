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
    experimental: { instrumentationHook: true },
    eslint: {
      // Disable ESLint during builds on Vercel
      ignoreDuringBuilds: true,
    },
    typescript: {
      // Disable TypeScript type checking during builds on Vercel
      ignoreBuildErrors: true,
    },
    rewrites() {
      return {
        beforeFiles: [
          { source: "/healthz", destination: "/api/health" },
          { source: "/api/healthz", destination: "/api/health" },
          { source: "/health", destination: "/api/health" },
          { source: "/ping", destination: "/api/health" },
        ],
      }
    },
    images: {
      domains: ['timesprofit.com', 'api.timesprofit.com'],
      remotePatterns: [
        {
          protocol: "https",
          hostname: "**.graphassets.com",
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
