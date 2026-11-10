import React from 'react';
import { notFound } from 'next/navigation';
import { loadStepRegistry, loadPapers } from '@/lib/config';
import { scanStepArtifacts, buildFileTree } from '@/lib/ingestion/scanner';
import { StepDetailClient } from './StepDetailClient';

export function generateStaticParams() {
  return Array.from({ length: 17 }, (_, i) => ({
    stepNumber: String(i + 1),
  }));
}

export default async function StepPage({
  params,
}: {
  params: Promise<{ stepNumber: string }>;
}) {
  const { stepNumber } = await params;
  const num = parseInt(stepNumber, 10);
  if (isNaN(num) || num < 1 || num > 17) {
    notFound();
  }

  const steps = loadStepRegistry();
  const step = steps.find((s) => s.number === num);
  if (!step) {
    notFound();
  }

  const artifacts = scanStepArtifacts(num);
  const fileTree = buildFileTree(artifacts);
  const papers = loadPapers().filter((p) => step.papers.includes(p.id));

  return (
    <StepDetailClient
      step={step}
      artifacts={artifacts}
      fileTree={fileTree}
      papers={papers}
    />
  );
}
