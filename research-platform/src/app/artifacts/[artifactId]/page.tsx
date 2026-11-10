import React from 'react';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { getArtifactById } from '@/lib/ingestion/scanner';
import { CsvViewer } from '@/components/artifacts/CsvViewer';
import { MarkdownViewer } from '@/components/artifacts/MarkdownViewer';
import { CodeViewer } from '@/components/artifacts/CodeViewer';
import { DocxViewer } from '@/components/artifacts/DocxViewer';
import { parseDocxFile } from '@/lib/ingestion/docx-parser';
import { CommentPanel } from '@/components/audit/CommentPanel';
import { ResizablePanel } from '@/components/layout/ResizablePanel';
import fs from 'node:fs';

import { getAllArtifacts } from '@/lib/ingestion/scanner';

export function generateStaticParams() {
  const { artifacts } = getAllArtifacts();
  const params = artifacts.map((a) => ({ artifactId: a.id }));
  params.push({ artifactId: 'REF_READINESS_REPORT' });
  params.push({ artifactId: 'REF_AI_AUDIT_GUIDE' });
  return params;
}

export default async function ArtifactPage({
  params,
}: {
  params: Promise<{ artifactId: string }>;
}) {
  const { artifactId } = await params;

  // Handle special aliases
  let targetId = artifactId;
  if (artifactId === 'REF_READINESS_REPORT') {
    targetId = Buffer.from('DAM_ANALYSIS_READY_2026/FINAL_DATA_READINESS_REPORT.md').toString('base64url');
  } else if (artifactId === 'REF_AI_AUDIT_GUIDE') {
    targetId = Buffer.from('DAM_ANALYSIS_READY_2026/STEPS_4_TO_11_AI_AUDIT_GUIDE.md').toString('base64url');
  }

  const lookup = getArtifactById(targetId);
  if (!lookup) {
    notFound();
  }

  const { artifact, fullPath, sha256 } = lookup;
  let textContent: string | undefined = undefined;
  const document = artifact.fileType === 'docx' ? await parseDocxFile(fullPath) : undefined;

  if (['md', 'py', 'json', 'txt'].includes(artifact.fileType)) {
    textContent = fs.readFileSync(fullPath, 'utf-8');
  }

  return (
    <div style={{ display: 'flex', height: 'calc(100vh - 86px)', gap: 0 }}>
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          background: 'var(--color-bg-primary)',
          borderRight: '1px solid var(--color-border)',
        }}
      >
        {/* Artifact Top Bar */}
        <div
          style={{
            padding: '12px 16px',
            borderBottom: '1px solid var(--color-border)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            background: 'var(--color-bg-secondary)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Link href="/" style={{ color: 'var(--color-text-muted)', fontSize: '12px', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <ArrowLeft size={14} aria-hidden="true" /> Overview
            </Link>
            <span style={{ color: 'var(--color-text-muted)' }}>/</span>
            <strong style={{ color: 'var(--color-text-primary)', fontSize: '13px' }}>
              {artifact.fileName}
            </strong>
          </div>

          <div style={{ fontSize: '11px', color: 'var(--color-primary)', fontWeight: 600 }}>
            Path: {artifact.relativePath}
          </div>
        </div>

        {/* Content Render */}
        <div style={{ flex: 1, overflow: 'auto', padding: '16px' }}>
          {artifact.fileType === 'csv' ? (
            <CsvViewer artifactId={artifact.id} fileName={artifact.fileName} />
          ) : artifact.fileType === 'docx' ? (
            <DocxViewer relativePath={artifact.relativePath} fileName={artifact.fileName} sha256={sha256} />
          ) : artifact.fileType === 'md' ? (
            <MarkdownViewer
              content={textContent || ''}
              sha256={sha256}
              fileName={artifact.fileName}
            />
          ) : artifact.fileType === 'py' || artifact.fileType === 'json' || artifact.fileType === 'txt' ? (
            <CodeViewer
              content={textContent || ''}
              fileName={artifact.fileName}
              sha256={sha256}
            />
          ) : (
            <div className="empty-state">
              <div className="empty-state__text">{artifact.fileName}</div>
              <div className="empty-state__sub">File size: {(artifact.sizeBytes / 1024).toFixed(1)} KB</div>
            </div>
          )}
        </div>
      </div>

      <ResizablePanel
        initialWidth={320}
        minWidth={220}
        maxWidth={500}
        side="right"
        collapsible={true}
        title="Comments"
      >
        <CommentPanel artifactVersionId={sha256} />
      </ResizablePanel>
    </div>
  );
}
