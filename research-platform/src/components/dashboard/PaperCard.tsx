'use client';

import React from 'react';
import Link from 'next/link';
import type { Paper } from '@/types';
import { StatusBadge } from '@/components/shared/StatusBadge';

interface PaperCardProps {
  paper: Paper;
  index: number;
}

export function PaperCard({ paper, index }: PaperCardProps) {
  return (
    <Link href={`/papers/${paper.id}`} className="paper-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
        <div className="paper-card__number">PAPER {index + 1}</div>
        <StatusBadge status={paper.status} size="sm" />
      </div>

      <div className="paper-card__title">{paper.title}</div>
      <div className="paper-card__subtitle">{paper.subtitle}</div>

      <div className="paper-card__meta">
        <div className="paper-card__meta-item">
          <span>Target Econometric Sample:</span>
          <strong>{paper.targetSample}</strong>
        </div>
        <div className="paper-card__meta-item">
          <span>Primary Price Variable:</span>
          <strong>{paper.primaryPriceVar}</strong>
        </div>
      </div>
    </Link>
  );
}
