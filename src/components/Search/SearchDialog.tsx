"use client"

// Algolia imports commented out - not using Algolia
// import algoliasearch from "algoliasearch/lite"
// import type { Hit } from "instantsearch.js"
// import debounce from "lodash/debounce"
import { Search } from "lucide-react"
// import { ChangeEvent, ReactNode, useMemo, useState } from "react"
// import {
//   Configure,
//   Highlight,
//   Hits,
//   InstantSearch,
//   Snippet,
//   useInstantSearch,
//   useSearchBox,
//   UseSearchBoxProps,
// } from "react-instantsearch"
import { Button } from "@/components/ui/Button/Button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/Dialog/Dialog"
// import { Input } from "@/components/ui/Input/Input"
// import { env } from "@/env.mjs"
import { useLocale } from "@/i18n/i18n"
// import { useTranslations } from "@/i18n/useTranslations"
// import { RefinementCombobox } from "./RefinementCombobox"
// import { Tag } from "../ArticleCard/Buttons/Tag"
// import { Popover } from "../ui/Popover/Popover"

// Algolia disabled - not using it
// const algoliaClient = algoliasearch(env.NEXT_PUBLIC_ALGOLIA_API_ID, env.NEXT_PUBLIC_ALGOLIA_SEARCH_API_KEY)

function SearchDialogContent() {
  const _lang = useLocale() // Prefixed with underscore to avoid unused warning

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          className="rounded-xl p-4 font-semibold hover:bg-custom-dim"
          variant="ghost"
          aria-label="Open search dialog"
          name="Search"
        >
          <Search className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Search</DialogTitle>
        </DialogHeader>
        <div className="p-4">
          <p className="text-sm text-gray-600">Search functionality is currently disabled.</p>
          <p className="text-xs text-gray-500 mt-2">Algolia integration has been removed.</p>
        </div>
      </DialogContent>
    </Dialog>
  )
}

// Algolia-related components commented out - not using Algolia
/*
type ArticleHit = Hit<{
  title: string
  content: string
  objectID: string
  slug: string
  tags: string[]
}>

... rest of Algolia components ...
*/

export default SearchDialogContent
