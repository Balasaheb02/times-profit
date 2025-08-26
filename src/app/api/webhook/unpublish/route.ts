import { NextRequest, NextResponse } from "next/server"
import { z } from "zod"
// import { hygraphLocaleToStandardNotation } from "@/i18n/i18n" // Not using Hygraph
// import { pipe } from "@/utils/pipe"
import { errorToNextResponse } from "../../httpError"
// import { algoliaClient } from "../algoliaClient" // Not using Algolia
import { handleRevalidation, modelTypesSchema } from "../handleRevalidation"
import { NextRequestWithValidBody, validateBody } from "../validateBody"
import { validateSignature } from "../validateSignature"

// Commented out Algolia functionality - not using it
/*
async function handleAlgoliaUnpublishWebhook(req: NextRequestWithValidBody<UnpublishWebhookBody>) {
  const article = req.validBody.data
  if (!isArticle(article)) return NextResponse.json({ result: "success" }, { status: 200 })

  const indexingResults = await Promise.allSettled(
    article.localizations.map(async ({ locale: hygraphLocale }) => {
      const locale = hygraphLocaleToStandardNotation(hygraphLocale)
      const index = algoliaClient.initIndex(`articles-${locale}`)
      await index.deleteObject(article.id)

      return { locale }
    })
  )

  return NextResponse.json({ result: indexingResults }, { status: 201 })
}
*/

// Simplified unpublish handler without Algolia
async function handleUnpublishWebhook(_req: NextRequestWithValidBody<UnpublishWebhookBody>) {
  // Just return success without Algolia deletion
  return NextResponse.json({ result: "success - not using Algolia" }, { status: 200 })
}

// Commented out unused functions
/*
const isArticle = (data: UnpublishWebhookBody["data"]): data is z.infer<typeof articleSchema> =>
  data.__typename === "Article"

const articleSchema = z.object({
  __typename: z.enum(["Article"]),
  localizations: z.array(z.object({ locale: z.string() })),
  id: z.string(),
})
*/

export async function POST(req: NextRequest) {
  try {
    // Simplified without pipe utility and Algolia
    const validatedReq = await validateSignature(req)
    const bodyValidatedReq = await validateBody(bodySchema)(validatedReq)
    await handleRevalidation(bodyValidatedReq)
    return await handleUnpublishWebhook(bodyValidatedReq)
  } catch (error) {
    return errorToNextResponse(error)
  }
}

const bodySchema = z.object({
  data: modelTypesSchema, // Simplified without article schema
})

type UnpublishWebhookBody = z.infer<typeof bodySchema>
