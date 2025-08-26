import { createEnv } from "@t3-oss/env-nextjs"
import { z } from "zod"

export const env = createEnv({
  server: {
    ANALYZE: z
      .enum(["true", "false"])
      .optional()
      .transform((value) => value === "true"),
    GA_MEASUREMENT_ID: z.string().optional(),
    GA_PROPERTY_ID: z.string().optional(),
    GA_BASE64_SERVICE_ACCOUNT: z.string().optional(),
    // HYGRAPH_WEBOOK_SECRET: z.string().optional(), // Not using Hygraph
  },
  client: {
    // NEXT_PUBLIC_ALGOLIA_API_ID: z.string().optional(), // Not using Algolia
    // NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY: z.string().optional(), // Not using Algolia
    NEXT_PUBLIC_SITE_URL: z.string().optional(),
  },
  runtimeEnv: {
    ANALYZE: process.env.ANALYZE,
    GA_MEASUREMENT_ID: process.env.GA_MEASUREMENT_ID,
    GA_PROPERTY_ID: process.env.GA_PROPERTY_ID,
    GA_BASE64_SERVICE_ACCOUNT: process.env.GA_BASE64_SERVICE_ACCOUNT,
    // NEXT_PUBLIC_ALGOLIA_API_ID: process.env.NEXT_PUBLIC_ALGOLIA_API_ID, // Not using Algolia
    // NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY: process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY, // Not using Algolia
    NEXT_PUBLIC_SITE_URL: `https://${process.env.NEXT_PUBLIC_SITE_URL ?? process.env.VERCEL_URL ?? "localhost:3000"}`,
  },
  skipValidation: process.env.SKIP_ENV_VALIDATION?.toString() === "true",
})
