'use client';

import React, { useState } from 'react';
import { X } from 'lucide-react';
import { useAuditMode } from '@/context/AuditModeContext';

export function CommentComposer() {
  const { activeAnchor, closeComposer, addComment, userName } = useAuditMode();
  const [commentText, setCommentText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!activeAnchor) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setIsSubmitting(true);
    try {
      await addComment(commentText);
      setCommentText('');
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : 'Unable to save comment');
    } finally {
      setIsSubmitting(false);
    }
  };

  const anchorDesc = () => {
    const a = activeAnchor.anchor;
    switch (a.type) {
      case 'csv_cell':
        return `CSV Cell [${a.columnName}] (Row ${a.rowIndex})`;
      case 'markdown_block':
        return `Text Section: ${a.headingPath.join(' > ') || 'Paragraph'}`;
      case 'code_line':
        return `Code Lines ${a.lineStart}-${a.lineEnd}`;
      case 'figure_region':
        return `Figure Region (${Math.round(a.normalizedX * 100)}%, ${Math.round(a.normalizedY * 100)}%)`;
      default:
        return 'Document Level';
    }
  };

  return (
    <div className="decision-dialog__overlay" onClick={closeComposer}>
      <div
        className="decision-dialog"
        onClick={(e) => e.stopPropagation()}
        style={{
          border: '1px solid var(--color-border)',
          boxShadow: 'var(--shadow-lg)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-primary)' }}>
            {activeAnchor.parentCommentId ? 'Reply to comment' : 'Leave audit comment'}
          </div>
          <button
            onClick={closeComposer}
            className="btn btn--icon"
            aria-label="Close comment composer"
            title="Close"
          >
            <X size={16} />
          </button>
        </div>

        {/* Anchor Context Reference */}
        <div
          style={{
            background: 'var(--color-bg-secondary)',
            padding: '6px 10px',
            borderRadius: 'var(--radius-sm)',
            fontSize: '11px',
            color: 'var(--color-text-secondary)',
            marginBottom: '12px',
            borderLeft: '3px solid var(--color-primary)',
          }}
        >
          <strong>Anchored to:</strong> {anchorDesc()}
        </div>

        <form onSubmit={handleSubmit}>
          <textarea
            className="decision-dialog__textarea"
            placeholder="Enter your audit feedback or notes"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            autoFocus
            rows={4}
          />

          {error && <div className="form-error" role="alert">{error}</div>}

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
              Author: <strong style={{ color: 'var(--color-text-primary)' }}>{userName}</strong>
            </span>

            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                type="button"
                onClick={closeComposer}
                className="btn btn--secondary"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn--primary"
                disabled={isSubmitting || !commentText.trim()}
              >
                {isSubmitting ? 'Saving...' : 'Post Comment'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
