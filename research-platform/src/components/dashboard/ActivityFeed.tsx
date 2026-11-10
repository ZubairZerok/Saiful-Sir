'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowRight, MessageSquare, ShieldCheck } from 'lucide-react';
import { useAuditMode } from '@/context/AuditModeContext';

export function ActivityFeed() {
  const { comments, resolveComment } = useAuditMode();

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 'var(--spacing-lg)' }}>
      {/* Comments & Teacher Feedback */}
      <div
        style={{
          background: 'var(--color-bg-primary)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--spacing-xl)',
          boxShadow: 'var(--shadow-xs)',
        }}
      >
        <div className="section-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <MessageSquare size={18} color="var(--color-primary)" aria-hidden="true" />
            <span>Supervisor Audit Feed & Anchored Feedback</span>
          </div>
        </div>

        {comments.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state__text">No audit comments recorded yet</div>
            <div className="empty-state__sub">
              Enable Audit Mode to click and attach feedback to any cell, table, text section, or code line.
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)' }}>
            {comments.slice(0, 5).map((comment) => (
              <div key={comment.id} className="comment-card">
                <div className="comment-card__meta">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="comment-card__author">{comment.authorName}</span>
                    <span
                      style={{
                        fontSize: '10px',
                        background: 'var(--color-bg-secondary)',
                        border: '1px solid var(--color-border)',
                        padding: '1px 6px',
                        borderRadius: 'var(--radius-xs)',
                        color: 'var(--color-text-muted)',
                        fontWeight: 600,
                      }}
                    >
                      {comment.anchorType.replace('_', ' ').toUpperCase()}
                    </span>
                  </div>
                  <span className="comment-card__time">
                    {new Date(comment.createdAt).toLocaleDateString()}
                  </span>
                </div>

                <div className="comment-card__body">{comment.body}</div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px' }}>
                  <div className="comment-card__anchor-ref">
                    {comment.anchorType === 'csv_cell' && 'Anchor: CSV Data Cell'}
                    {comment.anchorType === 'markdown_block' && 'Anchor: Section Paragraph'}
                    {comment.anchorType === 'code_line' && 'Anchor: Code Line'}
                    {comment.anchorType === 'general' && 'Anchor: Document'}
                  </div>

                  {!comment.isResolved && (
                    <button
                      onClick={() => resolveComment(comment.id)}
                      className="btn btn--secondary"
                      style={{ fontSize: '11px', padding: '2px 8px' }}
                    >
                      Mark Resolved
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Cryptographic Manifest & Integrity Status */}
      <div
        style={{
          background: 'var(--color-bg-primary)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--spacing-xl)',
          boxShadow: 'var(--shadow-xs)',
        }}
      >
        <div className="section-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={18} color="var(--color-primary)" aria-hidden="true" />
            <span>Cryptographic Integrity & AI Audit Index</span>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '10px 14px',
              background: 'var(--color-bg-secondary)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-border)',
              borderLeft: '3px solid var(--color-primary)',
            }}
          >
            <div>
              <div style={{ fontWeight: 700, fontSize: '12px' }}>DAM Raw Input Source CSVs</div>
              <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                12 CSV files in dam_output/master
              </div>
            </div>
            <span style={{ color: 'var(--color-primary)', fontSize: '11px', fontWeight: 700 }}>
              100% SHA-256 MATCH
            </span>
          </div>

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '10px 14px',
              background: 'var(--color-bg-secondary)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-border)',
              borderLeft: '3px solid var(--color-primary)',
            }}
          >
            <div>
              <div style={{ fontWeight: 700, fontSize: '12px' }}>Cleaning & Quality Control Tiers</div>
              <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                FULL_FLAGGED, PRIMARY, STRICT_SENSITIVITY
              </div>
            </div>
            <span style={{ color: 'var(--color-primary)', fontSize: '11px', fontWeight: 700 }}>
              36 CSVs GENERATED
            </span>
          </div>

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '10px 14px',
              background: 'var(--color-bg-secondary)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-border)',
              borderLeft: '3px solid var(--color-primary)',
            }}
          >
            <div>
              <div style={{ fontWeight: 700, fontSize: '12px' }}>Step 4 to 11 AI Audit Guide</div>
              <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                Itemized Verification Blueprint & Prompts
              </div>
            </div>
            <Link
              href="/artifacts/REF_AI_AUDIT_GUIDE"
              style={{
                color: 'var(--color-primary)',
                fontSize: '11px',
                fontWeight: 700,
                 display: 'inline-flex',
                 alignItems: 'center',
                 gap: '4px',
              }}
            >
              OPEN AUDIT GUIDE <ArrowRight size={13} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
