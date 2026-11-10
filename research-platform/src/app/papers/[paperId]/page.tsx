import React from 'react';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { loadPapers, loadStepRegistry } from '@/lib/config';
import { StatusBadge } from '@/components/shared/StatusBadge';

export function generateStaticParams() {
  return [
    { paperId: 'paper-1' },
    { paperId: 'paper-2' },
    { paperId: 'paper-3' },
  ];
}

export default async function PaperPage({
  params,
}: {
  params: Promise<{ paperId: string }>;
}) {
  const { paperId } = await params;
  const papers = loadPapers();
  const paper = papers.find((p) => p.id === paperId);

  if (!paper) {
    notFound();
  }

  const allSteps = loadStepRegistry();
  const paperSteps = allSteps.filter((s) => s.papers.includes(paper.id));

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '10px 0' }}>
      {/* Header Card */}
      <div
        style={{
          background: 'var(--color-bg-primary)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-lg)',
          padding: '24px',
          marginBottom: '24px',
          boxShadow: 'var(--shadow-xs)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <div style={{ color: 'var(--color-primary)', fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            Target Empirical Research Paper
          </div>
          <StatusBadge status={paper.status} />
        </div>

        <h1 style={{ fontSize: '22px', fontWeight: 800, color: 'var(--color-text-primary)', marginBottom: '4px' }}>
          {paper.title}
        </h1>
        <div style={{ fontSize: '15px', color: 'var(--color-text-muted)', fontStyle: 'italic', marginBottom: '20px' }}>
          {paper.subtitle}
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '16px',
            background: 'var(--color-bg-secondary)',
            border: '1px solid var(--color-border)',
            padding: '16px',
            borderRadius: 'var(--radius-md)',
            fontSize: '12px',
          }}
        >
          <div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '11px', marginBottom: '2px' }}>
              PRIMARY OUTCOME VARIABLE:
            </div>
            <div style={{ color: 'var(--color-primary)', fontWeight: 700 }}>{paper.primaryPriceVar}</div>
          </div>

          <div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '11px', marginBottom: '2px' }}>
              TARGET ECONOMETRIC SAMPLE:
            </div>
            <div style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{paper.targetSample}</div>
          </div>

          <div>
            <div style={{ color: 'var(--color-text-muted)', fontSize: '11px', marginBottom: '2px' }}>
              FEASIBILITY STATUS:
            </div>
            <div style={{ color: 'var(--color-status-approved)', fontWeight: 700 }}>
              {paper.status === 'analysis-ready' ? 'Analysis Ready' : 'Ready with Conditions'}
            </div>
          </div>
        </div>
      </div>

      {/* Associated Execution Steps */}
      <div style={{ marginBottom: '32px' }}>
        <div className="section-header">
          <span>Workflow Execution Pipeline for this Paper</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {paperSteps.map((step) => (
            <Link
              key={step.number}
              href={`/steps/${step.number}`}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 16px',
                background: 'var(--color-bg-primary)',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                textDecoration: 'none',
                color: 'inherit',
                transition: 'all var(--transition-fast)',
                boxShadow: 'var(--shadow-xs)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div
                  className={`sidebar__step-number sidebar__step-number--${
                    step.status === 'approved' ? 'approved' : 'not-started'
                  }`}
                >
                  {step.status === 'approved' ? (
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  ) : (
                    step.number
                  )}
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '13px', color: 'var(--color-text-primary)' }}>{step.name}</div>
                  <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>{step.description}</div>
                </div>
              </div>

              <StatusBadge status={step.status} size="sm" />
            </Link>
          ))}
        </div>
      </div>

      {/* Feasibility & Readiness Details */}
      <div
        style={{
          background: 'var(--color-bg-primary)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-lg)',
          padding: '24px',
          boxShadow: 'var(--shadow-xs)',
        }}
      >
        <div className="section-header">
          <span>Data Readiness Evaluation & Forensic Validation</span>
        </div>

        <div style={{ fontSize: '13px', lineHeight: 1.6, color: 'var(--color-text-secondary)' }}>
          {paper.id === 'paper-2' ? (
            <div>
              <p style={{ marginBottom: '12px' }}>
                <strong style={{ color: 'var(--color-primary)' }}>Paper 2 is fully ANALYSIS READY.</strong> The
                cleaned dataset yields over <strong>5,500 bilateral market pairs</strong> with common
                observation months, and <strong>990 local onion pairs</strong> with continuous 12-month series.
              </p>
              <p>
                Spatial distance matrices and monthly price dispersion ($|\ln(P_i) - \ln(P_j)|$) can be estimated
                immediately using <code>DAM_ALL_11_PRIMARY_ANALYSIS.csv</code> and <code>DAM_ALL_11_STRICT_SENSITIVITY.csv</code>.
              </p>
            </div>
          ) : paper.id === 'paper-1' ? (
            <div>
              <p style={{ marginBottom: '12px' }}>
                <strong style={{ color: 'var(--color-primary)' }}>Paper 1 is READY WITH CONDITIONS.</strong> The 15-month
                empirical span covers the complete 2025/2026 Rabi season (planting, growth, harvest, storage liquidation).
              </p>
              <p>
                Condition: Econometric models must utilize monthly/seasonal fixed-effects panels focusing on pre-harvest shock
                windows rather than multi-year time-series regressions.
              </p>
            </div>
          ) : (
            <div>
              <p style={{ marginBottom: '12px' }}>
                <strong style={{ color: 'var(--color-primary)' }}>Paper 3 is READY WITH CONDITIONS.</strong> Over 3,100
                observations feature concurrent wholesale and retail prices, allowing precise measurement of
                marketing margins (<code>wholesale_retail_spread_kg</code>).
              </p>
              <p>
                Condition: Merge flood event polygons (e.g. 2025 Eastern Bangladesh flood event) before running final spatial
                threshold regressions in Step 14.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
