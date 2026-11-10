'use client';

import React, { useState } from 'react';
import { MessageSquarePlus, Reply } from 'lucide-react';
import { useAuditMode } from '@/context/AuditModeContext';

interface CommentPanelProps {
  artifactVersionId?: string;
}

export function CommentPanel({ artifactVersionId }: CommentPanelProps) {
  const { comments, resolveComment, isAuditMode, openComposer, exportAuditData } = useAuditMode();
  const [filter, setFilter] = useState<'active' | 'resolved' | 'all'>('active');

  const artifactComments = artifactVersionId
    ? comments.filter((c) => c.artifactVersionId === artifactVersionId)
    : comments;
  const filteredComments = artifactComments.filter((comment) =>
    filter === 'all' || (filter === 'resolved' ? comment.isResolved : !comment.isResolved)
  );
  const visibleIds = new Set(filteredComments.map((comment) => comment.id));
  const roots = filteredComments.filter((comment) => !comment.parentCommentId || !visibleIds.has(comment.parentCommentId));

  const renderComment = (comment: (typeof comments)[number], depth = 0): React.ReactNode => {
    const replies = filteredComments
      .filter((candidate) => candidate.parentCommentId === comment.id)
      .sort((a, b) => a.createdAt.localeCompare(b.createdAt));

    return (
      <div key={comment.id} className={`comment-thread ${depth > 0 ? 'comment-thread--reply' : ''}`}>
        <div className={`comment-card ${comment.isResolved ? 'comment-card--resolved' : ''}`}>
          <div className="comment-card__meta">
            <span className="comment-card__author">{comment.authorName}</span>
            <span className="comment-card__time">
              {new Date(comment.createdAt).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })}
            </span>
          </div>

          <div className="comment-card__body">{comment.body}</div>

          <div className="comment-card__actions">
            <span className="comment-card__anchor-ref">{comment.anchorType.replaceAll('_', ' ')}</span>
            <div>
              {isAuditMode && !comment.isResolved && (
                <button
                  className="comment-card__action"
                  onClick={() => openComposer(comment.anchorData, comment.artifactVersionId, undefined, comment.id)}
                >
                  <Reply size={12} /> Reply
                </button>
              )}
              {!comment.isResolved && (
                <button className="comment-card__action" onClick={() => resolveComment(comment.id)}>
                  Resolve
                </button>
              )}
              {comment.isResolved && <span className="comment-card__resolved">Resolved</span>}
            </div>
          </div>
        </div>
        {replies.map((reply) => renderComment(reply, depth + 1))}
      </div>
    );
  };

  return (
    <div className="comment-panel">
      <div className="comment-panel__header">
        <div className="comment-panel__title">Audit Comments</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            onClick={exportAuditData}
            title="Export all comments and audit notes to a JSON file"
            style={{
              background: 'none',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--radius-xs)',
              padding: '2px 6px',
              fontSize: '10px',
              color: 'var(--color-text-secondary)',
              cursor: 'pointer',
            }}
          >
            Export JSON
          </button>
          <div className="comment-panel__count">
            {artifactComments.filter((c) => !c.isResolved).length} pending
          </div>
        </div>
      </div>

      <div className="comment-panel__filters" role="group" aria-label="Comment filters">
        {(['active', 'resolved', 'all'] as const).map((value) => (
          <button key={value} className={filter === value ? 'is-active' : ''} onClick={() => setFilter(value)}>{value}</button>
        ))}
        <button onClick={() => setFilter('all')}>Clear filters</button>
      </div>

      <div className="comment-panel__list">
        {filteredComments.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '30px 10px', color: 'var(--color-text-muted)', fontSize: '12px' }}>
            <div>No comments on this view.</div>
            {isAuditMode && (
              <button
                onClick={() =>
                  openComposer(
                    { type: 'general' },
                    artifactVersionId || 'general-artifact-version'
                  )
                }
                className="btn btn--secondary"
                style={{ marginTop: '12px', fontSize: '11px', width: '100%' }}
              >
                <MessageSquarePlus size={14} /> Add note
              </button>
            )}
          </div>
        ) : (
          roots.map((comment) => renderComment(comment))
        )}
      </div>
    </div>
  );
}
