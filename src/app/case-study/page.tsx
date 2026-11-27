import type { Metadata } from "next";
import { createPageMetadata } from "@/lib/metadata";
import { CaseStudyClient } from "./CaseStudyClient";

export const metadata: Metadata = createPageMetadata({
  path: "/case-study",
  title: "Case Study · Punjab–Haryana–Delhi Fire-Smoke Corridor | VayuDrishti",
  description:
    "Post-monsoon evidence chain linking MODIS active fires, TROPOMI HCHO anomalies, ERA5 back-trajectories, and Delhi NCR surface AQI.",
});

export default function CaseStudyPage() {
  return <CaseStudyClient />;
}
