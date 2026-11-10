'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import { useAuditMode } from '@/context/AuditModeContext';

interface MarkdownViewerProps {
  content: string;
  sha256?: string;
  fileName?: string;
}

export function MarkdownViewer({ content, sha256, fileName }: MarkdownViewerProps) {
  const { isAuditMode, openComposer } = useAuditMode();

  const handleBlockClick = (e: React.MouseEvent, headingText: string, index: number) => {
    if (!isAuditMode) return;
    e.stopPropagation();

    const rect = e.currentTarget.getBoundingClientRect();
    openComposer(
      {
        type: 'markdown_block',
        headingPath: [headingText || 'Section'],
        blockHash: `block-${index}`,
        blockIndex: index,
      },
      sha256 || 'markdown-artifact-version',
      {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        width: rect.width,
        height: rect.height,
      }
    );
  };

  return (
    <div className="md-viewer-wrap">
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
            {fileName || 'Document'}
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
          <span
            style={{
              color: 'var(--color-primary)',
              fontSize: '11px',
              fontWeight: 600,
            }}
          >
            Audit Mode Active: Click any section to comment
          </span>
        )}
      </div>

      <div className="md-viewer" style={{ padding: '0 8px' }}>
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex, rehypeRaw]}
          components={{
            h1: ({ children }) => (
              <h1
                onClick={(e) => handleBlockClick(e, String(children), 1)}
                style={{ cursor: isAuditMode ? 'crosshair' : 'default' }}
              >
                {children}
              </h1>
            ),
            h2: ({ children }) => (
              <h2
                onClick={(e) => handleBlockClick(e, String(children), 2)}
                style={{ cursor: isAuditMode ? 'crosshair' : 'default' }}
              >
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3
                onClick={(e) => handleBlockClick(e, String(children), 3)}
                style={{ cursor: isAuditMode ? 'crosshair' : 'default' }}
              >
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p
                onClick={(e) => handleBlockClick(e, 'Paragraph', 4)}
                style={{ cursor: isAuditMode ? 'crosshair' : 'default' }}
              >
                {children}
              </p>
            ),
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}
