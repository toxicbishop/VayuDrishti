import type { Metadata } from "next";

export const SITE_URL = "https://vayu-drishti-one.vercel.app";

export interface ImageMetadataConfig {
  url: string;
  secureUrl?: string;
  type?: string;
  width?: number;
  height?: number;
  alt?: string;
}

export interface PageMetadataOptions {
  title?: string;
  description?: string;
  path?: string;
  siteName?: string;
  type?: "website" | "article";
  image?: string | Partial<ImageMetadataConfig>;
  twitterCard?: "summary" | "summary_large_image";
  twitterTitle?: string;
  twitterDescription?: string;
}

export const DEFAULT_IMAGE: Required<ImageMetadataConfig> = {
  url: `${SITE_URL}/dashboard.png`,
  secureUrl: `${SITE_URL}/dashboard.png`,
  type: "image/png",
  width: 1911,
  height: 910,
  alt: "VayuDrishti satellite-derived surface AQI estimation and TROPOMI HCHO hotspot dashboard over India",
};

export const DEFAULT_SEO = {
  siteName: "VayuDrishti",
  title:
    "Satellite-derived Surface AQI estimation & TROPOMI HCHO hotspot detection/attribution over India using INSAT-3D, Sentinel-5P, ERA5 & ML | ISRO BAH-2026",
  description:
    "Satellite-derived surface AQI estimation and TROPOMI HCHO hotspot detection over India fusing INSAT-3D, Sentinel-5P, ERA5, and machine learning (ISRO BAH-2026).",
  canonicalUrl: `${SITE_URL}/`,
  type: "website" as const,
  twitterCard: "summary_large_image" as const,
  image: DEFAULT_IMAGE,
};

function toAbsoluteHttpsUrl(input: string): string {
  if (/^https?:\/\//i.test(input)) {
    return input.replace(/^http:\/\//i, "https://");
  }
  const normalizedPath = input === "/" || input === "" ? "/" : input.startsWith("/") ? input : `/${input}`;
  return `${SITE_URL}${normalizedPath}`;
}

export function createPageMetadata(options: PageMetadataOptions = {}): Metadata {
  const siteName = options.siteName ?? DEFAULT_SEO.siteName;
  const title = options.title ?? DEFAULT_SEO.title;
  const description = options.description ?? DEFAULT_SEO.description;
  const canonicalUrl = options.path ? toAbsoluteHttpsUrl(options.path) : DEFAULT_SEO.canonicalUrl;
  const type = options.type ?? DEFAULT_SEO.type;
  const twitterCard = options.twitterCard ?? DEFAULT_SEO.twitterCard;

  const imageOverride: Partial<ImageMetadataConfig> =
    typeof options.image === "string" ? { url: options.image, secureUrl: options.image } : (options.image ?? {});

  const imageUrl = toAbsoluteHttpsUrl(imageOverride.url ?? DEFAULT_IMAGE.url);
  const imageSecureUrl = toAbsoluteHttpsUrl(imageOverride.secureUrl ?? imageUrl);
  const resolvedImage: Required<ImageMetadataConfig> = {
    url: imageUrl,
    secureUrl: imageSecureUrl,
    type: imageOverride.type ?? DEFAULT_IMAGE.type,
    width: imageOverride.width ?? DEFAULT_IMAGE.width,
    height: imageOverride.height ?? DEFAULT_IMAGE.height,
    alt: imageOverride.alt ?? DEFAULT_IMAGE.alt,
  };

  return {
    metadataBase: new URL(SITE_URL),
    title,
    description,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      type,
      siteName,
      title,
      description,
      url: canonicalUrl,
      images: [resolvedImage],
    },
    twitter: {
      card: twitterCard,
      title: options.twitterTitle ?? title,
      description: options.twitterDescription ?? description,
      images: [
        {
          url: resolvedImage.url,
          alt: resolvedImage.alt,
        },
      ],
    },
  };
}
