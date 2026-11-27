import type { Metadata } from "next";
import "maplibre-gl/dist/maplibre-gl.css";
import "./globals.css";
import { SmoothScroll } from "@/components/SmoothScroll";
import { ChapterNav } from "@/components/ChapterNav";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Footer } from "@/components/sections";
import { createPageMetadata } from "@/lib/metadata";

export const metadata: Metadata = createPageMetadata();

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
        <SmoothScroll />
        <ChapterNav />
        <ThemeToggle />
        {children}
        <Footer />
      </body>
    </html>
  );
}
