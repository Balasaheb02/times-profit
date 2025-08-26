import type { Metadata } from "next"

// Commented out unused types
// type OpenGraphType =
//   | "article"
//   | "website"
//   | "book"
//   | "profile"
//   | "music.song"
//   | "music.album"
//   | "music.playlist"
//   | "music.radio_station"
//   | "video.movie"
//   | "video.episode"
//   | "video.tv_show"
//   | "video.other"

// type AuthorInfo = {
//   name?: string
// }

// type ImageData = {
//   url?: string
// }

// type ImageDescription = {
//   text: string
// }

// type ImageInfo = {
//   title: string
//   description?: ImageDescription | null
//   data: ImageData
// }

export const getMetadataObj = (metadataOptions: {
  title: string | undefined
  description: string | undefined
}): Metadata => {
  const { title, description } = metadataOptions
  return {
    title,
    description,
    openGraph: {
      title: title || "",
      description: description || "",
      siteName: "Times Profit",
    },
    twitter: {
      card: "summary_large_image",
      title: title || "",
      description: description || "",
    },
  }
}
