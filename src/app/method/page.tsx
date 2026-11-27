import type { Metadata } from "next";
import { Section } from "@/components/Section";
import { Pipeline } from "@/components/Pipeline";
import { Observations } from "@/components/sections";
import { ChapterPager } from "@/components/ChapterNav";
import { createPageMetadata } from "@/lib/metadata";

export const metadata: Metadata = createPageMetadata({
  path: "/method",
  title: "02 · The Method — Multi-Satellite & ML Fusion Pipeline | VayuDrishti",
  description:
    "How INSAT-3D, Sentinel-5P TROPOMI, MODIS, ERA5 meteorology, and CPCB ground data are fused via Random Forest modeling.",
});

export default function MethodPage() {
  return (
    <main>
      <Section
        id="pipeline"
        index="02"
        eyebrow="The Method"
        title="From raw signal to insight."
        lede="Six observation streams are fused, quality-screened, gridded and converted into AQI maps, HCHO anomaly layers and source-attribution hypotheses."
      >
        <Pipeline />
      </Section>
      <Observations />
      <ChapterPager current="/method" />
    </main>
  );
}
