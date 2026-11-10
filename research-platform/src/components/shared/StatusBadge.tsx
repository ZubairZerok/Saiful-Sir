import React from 'react';
import type { StepStatus } from '@/types';

interface StatusBadgeProps {
  status: StepStatus | string;
  className?: string;
  size?: 'sm' | 'md';
}

export function StatusBadge({ status, className = '', size = 'md' }: StatusBadgeProps) {
  const getLabelAndClass = () => {
    switch (status) {
      case 'approved':
        return { label: 'Approved', cls: 'status-badge--approved' };
      case 'in_progress':
        return { label: 'In Progress', cls: 'status-badge--progress' };
      case 'review_requested':
        return { label: 'In Review', cls: 'status-badge--review' };
      case 'changes_requested':
        return { label: 'Changes Req.', cls: 'status-badge--changes' };
      case 'locked':
        return { label: 'Locked', cls: 'status-badge--locked' };
      case 'analysis-ready':
        return { label: 'Analysis Ready', cls: 'status-badge--approved' };
      case 'data-ready-with-conditions':
        return { label: 'Ready w/ Conditions', cls: 'status-badge--review' };
      default:
        return { label: 'Not Started', cls: 'status-badge--not-started' };
    }
  };

  const { label, cls } = getLabelAndClass();

  return (
    <span
      className={`status-badge ${cls} ${className}`}
      style={{
        fontSize: size === 'sm' ? '10px' : undefined,
        padding: size === 'sm' ? '1px 6px' : undefined,
      }}
    >
      <span className="status-badge__dot" />
      {label}
    </span>
  );
}
