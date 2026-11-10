import React from 'react';
import { loadProjectConfig, loadStepRegistry, loadPapers } from '@/lib/config';
import { getAllArtifacts } from '@/lib/ingestion/scanner';
import { StepStepper } from '@/components/dashboard/StepStepper';
import { PaperCard } from '@/components/dashboard/PaperCard';
import { ActivityFeed } from '@/components/dashboard/ActivityFeed';

export default function DashboardPage() {
  const config = loadProjectConfig();
  const steps = loadStepRegistry();
  const papers = loadPapers();
  const { totalCount, totalSizeBytes } = getAllArtifacts();

  const approvedSteps = steps.filter((s) => s.status === 'approved').length;

  return (
    <div className="dashboard">
      {/* Hero Header */}
      <div className="dashboard__hero">
        <h1 className="dashboard__title">
          Auditinsyt <span>Research Audit Workspace</span>
        </h1>
        <p className="dashboard__subtitle">
          Agricultural Economics & Climate Shock Analysis in Bangladesh — 17-Step Forensic Execution & Audit Pipeline
        </p>
      </div>

      {/* Metrics Row */}
      <div className="metrics-row">
        <div className="metric-card">
          <div className="metric-card__label">Pipeline Progress</div>
          <div className="metric-card__value">
            {approvedSteps} / {steps.length}
          </div>
          <div className="metric-card__detail">Steps Approved & Audited</div>
        </div>

        <div className="metric-card">
          <div className="metric-card__label">Analyzed Observations</div>
          <div className="metric-card__value">
            {config.datasetMetrics.totalObservations.toLocaleString()}
          </div>
          <div className="metric-card__detail">
            {config.datasetMetrics.primaryAnalysisObs.toLocaleString()} Primary Clean
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card__label">Markets & Geographic Span</div>
          <div className="metric-card__value">
            {config.datasetMetrics.uniqueMarkets} Markets
          </div>
          <div className="metric-card__detail">
            8 of 8 Divisions (100% Complete)
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card__label">Indexed Artifacts</div>
          <div className="metric-card__value">{totalCount} Files</div>
          <div className="metric-card__detail">
            {(totalSizeBytes / (1024 * 1024)).toFixed(1)} MB SHA-256 Verified
          </div>
        </div>
      </div>

      {/* 17-Step Stepper */}
      <StepStepper steps={steps} />

      {/* Papers Section */}
      <div style={{ marginBottom: 'var(--spacing-2xl)' }}>
        <div className="section-header">
          <span>Target Empirical Research Papers</span>
        </div>

        <div className="papers-grid">
          {papers.map((paper, idx) => (
            <PaperCard key={paper.id} paper={paper} index={idx} />
          ))}
        </div>
      </div>

      {/* Live Audit & Manifest Feed */}
      <ActivityFeed />
    </div>
  );
}
