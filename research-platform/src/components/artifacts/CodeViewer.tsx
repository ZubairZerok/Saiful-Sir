'use client';

import React from 'react';
import { useAuditMode } from '@/context/AuditModeContext';

interface CodeViewerProps {
  content: string;
  fileName: string;
  sha256?: string;
}

export function CodeViewer({ content, fileName, sha256 }: CodeViewerProps) {
  const { isAuditMode, openComposer } = useAuditMode();
  const lines = content.split('\n');

  const handleLineClick = (e: React.MouseEvent, lineNum: number) => {
    if (!isAuditMode) return;
    const rect = e.currentTarget.getBoundingClientRect();
    openComposer(
      {
        type: 'code_line',
        lineStart: lineNum,
        lineEnd: lineNum,
        contentHash: `line-${lineNum}`,
      },
      sha256 || 'code-artifact-version',
      {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        width: rect.width,
        height: rect.height,
      }
    );
  };

  return (
    <div style={{ border: '1px solid var(--color-border)', borderRadius: 'var(--radius-md)', overflow: 'hidden' }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '8px 14px',
          background: 'var(--color-bg-secondary)',
          borderBottom: '1px solid var(--color-border)',
          fontSize: '11px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <strong style={{ color: 'var(--color-text-primary)' }}>{fileName}</strong>
          <span style={{ color: 'var(--color-text-muted)' }}>{lines.length} lines</span>
          {sha256 && (
            <span style={{ color: 'var(--color-text-muted)', fontFamily: 'var(--font-code)' }}>
              SHA-256: {sha256.substring(0, 10)}...
            </span>
          )}
        </div>

        {isAuditMode && (
          <span style={{ color: 'var(--color-primary)', fontWeight: 600 }}>
            Audit Mode Active: Click any line to comment
          </span>
        )}
      </div>

      <div
        style={{
          background: '#ffffff',
          overflowX: 'auto',
          maxHeight: 'calc(100vh - 260px)',
          fontFamily: 'var(--font-code)',
          fontSize: '12px',
        }}
      >
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <tbody>
            {lines.map((line, idx) => {
              const lineNum = idx + 1;
              return (
                <tr
                  key={idx}
                  onClick={(e) => handleLineClick(e, lineNum)}
                  style={{
                    cursor: isAuditMode ? 'crosshair' : 'default',
                  }}
                >
                  <td
                    style={{
                      width: '45px',
                      textAlign: 'right',
                      padding: '2px 10px',
                      color: 'var(--color-text-muted)',
                      userSelect: 'none',
                      borderRight: '1px solid var(--color-border)',
                      background: 'var(--color-bg-secondary)',
                      fontSize: '11px',
                    }}
                  >
                    {lineNum}
                  </td>
                  <td
                    style={{
                      padding: '2px 12px',
                      color: 'var(--color-text-primary)',
                      whiteSpace: 'pre',
                    }}
                  >
                    {line}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
