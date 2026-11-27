import type { Metadata } from "next";
import { createPageMetadata } from "@/lib/metadata";
import { HchoClient } from "./HchoClient";

export const metadata: Metadata = createPageMetadata({
  path: "/hcho",
  title: "04 · TROPOMI HCHO Hotspots & Source Attribution | VayuDrishti",
  description:
    "Identify persistent formaldehyde (HCHO) VOC anomalies, biomass burning clusters, and wind transport pathways across India.",
});

export default function HchoPage() {
  return <HchoClient />;
}
