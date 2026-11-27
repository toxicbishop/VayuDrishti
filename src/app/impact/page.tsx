import type { Metadata } from "next";
import { PolicyActionBoard, Evidence, Future, FinalImpact } from "@/components/sections";
import { ChapterPager } from "@/components/ChapterNav";
import { createPageMetadata } from "@/lib/metadata";

export const metadata: Metadata = createPageMetadata({
  path: "/impact",
  title: "06 · Impact & Policy Applications | VayuDrishti",
  description:
    "Decision-support applications, policy action workflows, and future operational roadmap for VayuDrishti.",
});

export default function ImpactPage() {
  return (
    <main>
      <PolicyActionBoard />
      <Evidence />
      <Future />
      <FinalImpact />
      <ChapterPager current="/impact" />
    </main>
  );
}
