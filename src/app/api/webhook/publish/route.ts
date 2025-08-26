import { NextRequest, NextResponse } from "next/server"
import { z } from "zod"
// import { hygraphLocaleToStandardNotation } from "@/i18n/i18n" // Not using Hygraph
// import { pipe } from "@/utils/pipe"
// import { slateToText } from "@/utils/slateToText"
import { errorToNextResponse } from "../../httpError"
// import { algoliaClient } from "../algoliaClient" // Not using Algolia
import { handleRevalidation, modelTypesSchema } from "../handleRevalidation"
import { NextRequestWithValidBody, validateBody } from "../validateBody"
import { validateSignature } from "../validateSignature"

// Commented out Algolia functionality - not using it
/*
async function handleAlgoliaPublishWebhook(req: NextRequestWithValidBody<PublishWebhookBody>) {
  const article = req.validBody.data
  if (!isArticle(article)) return NextResponse.json({ result: "success" }, { status: 200 })

  const indexingResults = await Promise.allSettled(
    article.localizations.map(async ({ locale: hygraphLocale, title, content, slug }) => {
      const locale = hygraphLocaleToStandardNotation(hygraphLocale)
      const index = algoliaClient.initIndex(`articles-${locale}`)
      index.setSettings({
        searchableAttributes: ["title", "content", "tags"],
        attributesForFaceting: ["searchable(tags)"],
      })
      await index.saveObject({
        objectID: article.id,
        title,
        content: slateToText(content),
        slug,
        tags: article.tags
          .map((tag) => tag.localizations.find((localization) => localization.locale === hygraphLocale)?.tag)
          .filter((tag) => tag !== undefined),
      })

      return { title, locale }
    })
  )

  return NextResponse.json({ result: indexingResults }, { status: 201 })
}
*/

// Simplified webhook handler without Algolia
async function handlePublishWebhook(_req: NextRequestWithValidBody<PublishWebhookBody>) {
  // Just return success without Algolia indexing
  return NextResponse.json({ result: "success - not using Algolia" }, { status: 200 })
}

export async function POST(req: NextRequest) {
  try {
    // Simplified without pipe utility and Algolia
    const validatedReq = await validateSignature(req)
    const bodyValidatedReq = await validateBody(bodySchema)(validatedReq)
    await handleRevalidation(bodyValidatedReq)
    return await handlePublishWebhook(bodyValidatedReq)
  } catch (error) {
    return errorToNextResponse(error)
  }
}

// Commented out unused functions since we're not using Hygraph/Algolia
/*
const isArticle = (data: PublishWebhookBody["data"]): data is z.infer<typeof articleSchema> =>
  data.__typename === "Article"

const articleSchema = z.object({
  __typename: z.enum(["Article"]),
  localizations: z.array(
    z.object({
      content: z.any(),
      title: z.string(),
      locale: z.string(),
      slug: z.string(),
    })
  ),
  tags: z.array(z.object({ localizations: z.array(z.object({ tag: z.string(), locale: z.string() })) })),
  id: z.string(),
})
*/

const bodySchema = z.object({
  data: modelTypesSchema, // Simplified without article schema
})

type PublishWebhookBody = z.infer<typeof bodySchema>
