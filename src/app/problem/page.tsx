import type { Metadata } from "next";
import { AirQuality, Signals, WhySatellites } from "@/components/sections";
import { ChapterPager } from "@/components/ChapterNav";
import { createPageMetadata } from "@/lib/metadata";

export const metadata: Metadata = createPageMetadata({
  path: "/problem",
  title: "01 · The Problem — Surface AQI Coverage Gaps over India | VayuDrishti",
  description:
    "Why most of India's air goes unmeasured by ground stations alone, and how satellite observations fill the spatial monitoring gap.",
});

export default function ProblemPage() {
  return (
    <main>
      <AirQuality />
      <Signals />
      <WhySatellites />
      <ChapterPager current="/problem" />
    </main>
  );
}
