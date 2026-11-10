'use client';

import React, { useState, useEffect } from 'react';
import type { WorkflowStep, Artifact, FileTreeNode, Paper, DocumentContent } from '@/types';
import { StatusBadge } from '@/components/shared/StatusBadge';
import { ArtifactTree } from '@/components/artifacts/ArtifactTree';
import { CsvViewer } from '@/components/artifacts/CsvViewer';
import { MarkdownViewer } from '@/components/artifacts/MarkdownViewer';
import { CodeViewer } from '@/components/artifacts/CodeViewer';
import { DocxViewer } from '@/components/artifacts/DocxViewer';
import { CommentPanel } from '@/components/audit/CommentPanel';
import { DecisionDialog } from '@/components/shared/DecisionDialog';
import { ResizablePanel } from '@/components/layout/ResizablePanel';

interface StepDetailClientProps {
  step: WorkflowStep;
  artifacts: Artifact[];
  fileTree: FileTreeNode[];
  papers: Paper[];
}

export function StepDetailClient({
  step,
  artifacts,
  fileTree,
  papers,
}: StepDetailClientProps) {
  const [selectedArtifact, setSelectedArtifact] = useState<Artifact | null>(
    artifacts.length > 0 ? artifacts[0] : null
  );
  const [artifactContent, setArtifactContent] = useState<{
    content?: string;
    document?: DocumentContent;
    sha256?: string;
    loading: boolean;
  }>({ loading: Boolean(artifacts[0] && artifacts[0].fileType !== 'csv') });
  const [isDecisionOpen, setIsDecisionOpen] = useState(false);
  const [stepStatus, setStepStatus] = useState(step.status);

  useEffect(() => {
    if (!selectedArtifact) return;

    if (selectedArtifact.fileType !== 'csv' && selectedArtifact.fileType !== 'docx') {
      const controller = new AbortController();
      fetch(`/api/artifacts/${selectedArtifact.id}`, { signal: controller.signal })
        .then(async (res) => {
          if (!res.ok) throw new Error('API not available, fallback to client fetch');
          return await res.json();
        })
        .then((data) => {
          setArtifactContent({
            content: data.content,
            document: data.document,
            sha256: data.sha256,
            loading: false,
          });
        })
        .catch(async (error) => {
          if (error instanceof DOMException && error.name === 'AbortError') return;
          try {
            const { fetchTextArtifactClient } = await import('@/lib/data-client');
            const text = await fetchTextArtifactClient(selectedArtifact.relativePath);
            setArtifactContent({
              content: text,
              loading: false,
            });
          } catch {
            setArtifactContent({ loading: false });
          }
        });

      return () => controller.abort();
    } else {
      setArtifactContent({ loading: false });
    }
  }, [selectedArtifact]);

  const handleSelectPath = (path: string) => {
    const found = artifacts.find((a) => a.relativePath === path);
    if (found) {
      setArtifactContent({ loading: found.fileType !== 'csv' });
      setSelectedArtifact(found);
    }
  };

  return (
    <div style={{ display: 'flex', height: 'calc(100vh - 86px)', gap: 0, position: 'relative' }}>
      {/* Left Column: Resizable & Collapsible Artifacts Tree */}
      <ResizablePanel
        initialWidth={260}
        minWidth={200}
        maxWidth={420}
        side="left"
        collapsible={true}
        title="Artifacts"
        count={artifacts.length}
      >
        <div
          style={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            borderRight: '1px solid var(--color-border)',
            background: 'var(--color-bg-primary)',
          }}
        >
          <div
            style={{
              padding: '12px 14px',
              borderBottom: '1px solid var(--color-border)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <strong style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-text-primary)' }}>
              Step Artifacts
            </strong>
            <span style={{ fontSize: '11px', color: 'var(--color-primary)', fontWeight: 600 }}>
              {artifacts.length} files
            </span>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', padding: '12px 0' }}>
            {artifacts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '30px 10px', color: 'var(--color-text-muted)', fontSize: '12px' }}>
                No artifacts linked to Step {step.number} yet.
              </div>
            ) : (
              <ArtifactTree
                tree={fileTree}
                onSelectArtifact={handleSelectPath}
                selectedPath={selectedArtifact?.relativePath}
              />
            )}
          </div>
        </div>
      </ResizablePanel>

      {/* Middle Column: Step Header + Active Artifact Viewer */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          background: 'var(--color-bg-primary)',
          minWidth: 0,
        }}
      >
        {/* Step Header */}
        <div
          style={{
            padding: '14px 20px',
            borderBottom: '1px solid var(--color-border)',
            background: 'var(--color-bg-secondary)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '6px' }}>
            <div>
              <div style={{ fontSize: '11px', color: 'var(--color-primary)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                Step {step.number} of 17
              </div>
              <h1 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--color-text-primary)' }}>
                {step.name}
              </h1>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <StatusBadge status={stepStatus} />
              <button
                onClick={() => setIsDecisionOpen(true)}
                className="btn btn--primary"
                style={{ fontSize: '11px', padding: '4px 10px' }}
              >
                Audit / Decide
              </button>
            </div>
          </div>

          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginBottom: '8px', lineHeight: 1.4 }}>
            {step.description}
          </p>

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', fontSize: '11px' }}>
            <span style={{ color: 'var(--color-text-muted)' }}>
              Associated Papers:{' '}
              {papers.map((p, i) => (
                <span key={p.id} style={{ color: 'var(--color-primary)', fontWeight: 600 }}>
                  {i > 0 && ', '}Paper {p.id.replace('paper-', '')}
                </span>
              ))}
            </span>
            {step.dependsOn.length > 0 && (
              <span style={{ color: 'var(--color-text-muted)' }}>
                Prerequisites: Steps {step.dependsOn.join(', ')}
              </span>
            )}
          </div>
        </div>

        {/* Content Viewer Body */}
        <div style={{ flex: 1, overflow: 'auto', padding: '16px' }}>
          {!selectedArtifact ? (
            <div className="empty-state">
              <div className="empty-state__text">Select an artifact from the left tree</div>
            </div>
          ) : selectedArtifact.fileType === 'csv' ? (
            <CsvViewer
              key={selectedArtifact.id}
              artifactId={selectedArtifact.id}
              fileName={selectedArtifact.fileName}
            />
          ) : selectedArtifact.fileType === 'docx' ? (
            <DocxViewer relativePath={selectedArtifact.relativePath} fileName={selectedArtifact.fileName} sha256={artifactContent.sha256} />
          ) : selectedArtifact.fileType === 'md' ? (
            artifactContent.loading ? (
              <div style={{ color: 'var(--color-primary)', fontWeight: 600, padding: '20px' }}>
                Loading document...
              </div>
            ) : (
              <MarkdownViewer
                content={artifactContent.content || ''}
                sha256={artifactContent.sha256}
                fileName={selectedArtifact.fileName}
              />
            )
          ) : selectedArtifact.fileType === 'py' || selectedArtifact.fileType === 'json' || selectedArtifact.fileType === 'txt' ? (
            artifactContent.loading ? (
              <div style={{ color: 'var(--color-primary)', fontWeight: 600, padding: '20px' }}>
                Loading script...
              </div>
            ) : (
              <CodeViewer
                content={artifactContent.content || ''}
                fileName={selectedArtifact.fileName}
                sha256={artifactContent.sha256}
              />
            )
          ) : (
            <div className="empty-state">
              <div className="empty-state__text">{selectedArtifact.fileName}</div>
              <div className="empty-state__sub">File size: {(selectedArtifact.sizeBytes / 1024).toFixed(1)} KB (Document archive)</div>
            </div>
          )}
        </div>
      </div>

      {/* Right Column: Resizable & Collapsible Comments Panel */}
      <ResizablePanel
        initialWidth={300}
        minWidth={220}
        maxWidth={480}
        side="right"
        collapsible={true}
        title="Comments"
      >
        <CommentPanel artifactVersionId={artifactContent.sha256 || selectedArtifact?.id || `step-${step.number}`} />
      </ResizablePanel>

      {/* Teacher Decision Modal */}
      <DecisionDialog
        stepNumber={step.number}
        stepName={step.name}
        isOpen={isDecisionOpen}
        onClose={() => setIsDecisionOpen(false)}
        onSuccess={() => {
          setStepStatus('approved');
        }}
      />
    </div>
  );
}
