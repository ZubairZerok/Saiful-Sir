'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import type { WorkflowStep, Paper } from '@/types';
import { ChevronLeft, ChevronRight, FileText, LayoutDashboard } from 'lucide-react';

interface SidebarProps {
  steps: WorkflowStep[];
  papers: Paper[];
}

export function Sidebar({ steps, papers }: SidebarProps) {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const isStepActive = (stepNum: number) => pathname === `/steps/${stepNum}`;
  const isPaperActive = (paperId: string) => pathname === `/papers/${paperId}`;
  const isDashboardActive = pathname === '/';

  return (
    <aside
      className="sidebar"
      style={{
        width: isCollapsed ? '64px' : '260px',
        minWidth: isCollapsed ? '64px' : '260px',
      }}
    >
      {/* Logo & Collapse Toggle */}
      <div className="sidebar__logo">
        <Link href="/" className="sidebar__logo-brand">
          <div className="sidebar__logo-icon">A</div>
          {!isCollapsed && (
            <div className="sidebar__logo-text">
              Audit<span>insyt</span>
            </div>
          )}
        </Link>

        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="sidebar__toggle-btn"
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <ChevronRight size={15} /> : <ChevronLeft size={15} />}
        </button>
      </div>

      <nav className="sidebar__nav">
        {/* Overview Dashboard */}
        <Link
          href="/"
          className={`sidebar__nav-item ${isDashboardActive ? 'sidebar__nav-item--active' : ''}`}
          title="Overview Dashboard"
        >
          <span className="sidebar__nav-item-icon">
            <LayoutDashboard size={16} />
          </span>
          {!isCollapsed && <span>Overview Dashboard</span>}
        </Link>

        {/* Papers Section */}
        {!isCollapsed && <div className="sidebar__section-label">Research Papers</div>}
        {papers.map((p, idx) => (
          <Link
            key={p.id}
            href={`/papers/${p.id}`}
            className={`sidebar__nav-item ${isPaperActive(p.id) ? 'sidebar__nav-item--active' : ''}`}
            title={`Paper ${idx + 1}: ${p.title}`}
          >
            <span className="sidebar__nav-item-icon">
              <FileText size={16} />
            </span>
            {!isCollapsed && (
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                Paper {idx + 1}
              </span>
            )}
          </Link>
        ))}

        {/* 17 Steps Section */}
        {!isCollapsed && <div className="sidebar__section-label">17 Execution Steps</div>}
        <div className="sidebar__step-list">
          {steps.map((step) => {
            const active = isStepActive(step.number);
            let numCls = 'sidebar__step-number';
            if (step.status === 'approved') numCls += ' sidebar__step-number--approved';
            else if (step.status === 'in_progress') numCls += ' sidebar__step-number--progress';
            else if (step.status === 'review_requested') numCls += ' sidebar__step-number--review';
            else if (step.status === 'changes_requested') numCls += ' sidebar__step-number--changes';

            return (
              <Link
                key={step.number}
                href={`/steps/${step.number}`}
                className={`sidebar__step-item ${active ? 'sidebar__step-item--active' : ''}`}
                title={`Step ${step.number}: ${step.name}`}
              >
                <div className={numCls}>{step.number}</div>
                {!isCollapsed && <div className="sidebar__step-name">{step.name}</div>}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Footer Info */}
      {!isCollapsed && (
        <div
          style={{
            padding: '12px 16px',
            borderTop: '1px solid var(--color-border)',
            fontSize: '11px',
            color: 'var(--color-text-muted)',
            lineHeight: 1.3,
          }}
        >
          <div style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>PI: Zubair</div>
          <div>DAM_ANALYSIS_READY_2026</div>
        </div>
      )}
    </aside>
  );
}
