import type { Metadata } from "next";
import { createPageMetadata } from "@/lib/metadata";
import { AqiClient } from "./AqiClient";

export const metadata: Metadata = createPageMetadata({
  path: "/aqi",
  title: "03 · Daily Surface AQI Map across India | VayuDrishti",
  description:
    "Explore satellite-derived daily surface AQI estimates and CPCB-validated RAPI risk across India.",
});

export default function AqiPage() {
  return <AqiClient />;
}
