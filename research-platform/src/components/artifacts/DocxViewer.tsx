'use client';

import React, { useState, useEffect } from 'react';
import mammoth from 'mammoth';
import { useAuditMode } from '@/context/AuditModeContext';

interface DocxViewerProps {
  relativePath: string;
  fileName: string;
  sha256?: string;
}

export function DocxViewer({ relativePath, fileName, sha256 }: DocxViewerProps) {
  const { isAuditMode, openComposer } = useAuditMode();
  const [htmlContent, setHtmlContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDocx() {
      setLoading(true);
      setError(null);
      try {
        const url = `/research_data/${relativePath.replace(/^(\.\/|\/)/, '')}`;
        const res = await fetch(url);
        if (!res.ok) {
          throw new Error(`Failed to load document: ${res.statusText}`);
        }
        const arrayBuffer = await res.arrayBuffer();
        const result = await mammoth.convertToHtml({ arrayBuffer });
        setHtmlContent(result.value);
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Unknown error parsing DOCX';
        setError(message);
      } finally {
        setLoading(false);
      }
    }

    loadDocx();
  }, [relativePath]);

  const handleBlockClick = (e: React.MouseEvent) => {
    if (!isAuditMode) return;
    const target = e.target as HTMLElement;
    const rect = target.getBoundingClientRect();
    const tag = target.tagName.toLowerCase();
    const textSnippet = target.innerText?.substring(0, 50) || 'Document Section';

    openComposer(
      {
        type: 'markdown_block',
        headingPath: [`DOCX: ${fileName}`, `${tag}: ${textSnippet}`],
        blockHash: `docx-block-${Math.abs(hashString(textSnippet))}`,
        blockIndex: 0,
      },
      sha256 || 'docx-artifact-version',
      {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        width: rect.width,
        height: rect.height,
      }
    );
  };

  return (
    <div className="docx-viewer-wrap">
      {/* File Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '8px 14px',
          background: 'var(--color-bg-secondary)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-md) var(--radius-md) 0 0',
          marginBottom: '16px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <strong style={{ color: 'var(--color-text-primary)', fontSize: '13px' }}>
            Word Document: {fileName}
          </strong>
          {sha256 && (
            <span
              style={{
                fontSize: '11px',
                color: 'var(--color-text-muted)',
                fontFamily: 'var(--font-code)',
              }}
            >
              SHA-256: {sha256.substring(0, 10)}...
            </span>
          )}
        </div>

        {isAuditMode && (
          <span style={{ color: 'var(--color-primary)', fontSize: '11px', fontWeight: 600 }}>
            Audit Mode Active: Click any paragraph or table to comment
          </span>
        )}
      </div>

      {loading && (
        <div style={{ padding: '30px', textAlign: 'center', color: 'var(--color-primary)', fontWeight: 600 }}>
          Rendering Word document...
        </div>
      )}

      {error && (
        <div className="empty-state">
          <div className="empty-state__text">Failed to render DOCX file</div>
          <div className="empty-state__sub">{error}</div>
        </div>
      )}

      {!loading && !error && (
        <div
          className="md-viewer"
          style={{ padding: '0 8px', cursor: isAuditMode ? 'crosshair' : 'default' }}
          onClick={handleBlockClick}
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
      )}
    </div>
  );
}

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0;
  }
  return hash;
}