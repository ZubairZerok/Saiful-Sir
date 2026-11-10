'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuditMode } from '@/context/AuditModeContext';

export function Header() {
  const pathname = usePathname();
  const { isAuditMode, toggleAuditMode, comments } = useAuditMode();

  const getBreadcrumbs = () => {
    if (pathname === '/') {
      return [{ label: 'Auditinsyt', href: '/' }, { label: 'Workspace Overview', href: '/' }];
    }
    const parts = pathname.split('/').filter(Boolean);
    const crumbs = [{ label: 'Auditinsyt', href: '/' }];

    if (parts[0] === 'steps' && parts[1]) {
      crumbs.push({ label: `Step ${parts[1]}`, href: `/steps/${parts[1]}` });
    } else if (parts[0] === 'papers' && parts[1]) {
      crumbs.push({ label: `Paper ${parts[1].replace('paper-', '')}`, href: `/papers/${parts[1]}` });
    } else if (parts[0] === 'artifacts' && parts[1]) {
      crumbs.push({ label: 'Artifact Audit', href: pathname });
    }

    return crumbs;
  };

  const breadcrumbs = getBreadcrumbs();
  const unresolvedComments = comments.filter((c) => !c.isResolved).length;

  return (
    <header className="header">
      {/* Breadcrumb Navigation */}
      <nav className="header__breadcrumb" aria-label="Breadcrumb">
        {breadcrumbs.map((crumb, idx) => (
          <React.Fragment key={crumb.href}>
            {idx > 0 && <span className="header__breadcrumb-sep">/</span>}
            {idx === breadcrumbs.length - 1 ? (
              <span className="header__breadcrumb-current">{crumb.label}</span>
            ) : (
              <Link href={crumb.href}>{crumb.label}</Link>
            )}
          </React.Fragment>
        ))}
      </nav>

      {/* Header Actions */}
      <div className="header__actions">
        {/* Source of Truth Indicator */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'var(--color-bg-secondary)',
            border: '1px solid var(--color-border)',
            padding: '4px 10px',
            borderRadius: 'var(--radius-sm)',
            fontSize: '11px',
            color: 'var(--color-text-secondary)',
            fontWeight: 500,
          }}
        >
          <span
            style={{
              width: '6px',
              height: '6px',
              borderRadius: '50%',
              background: 'var(--color-primary)',
            }}
          />
          Local File System (Source of Truth)
        </div>

        {/* Audit Mode Toggle */}
        <button
          onClick={toggleAuditMode}
          className={`audit-toggle ${isAuditMode ? 'audit-toggle--active' : ''}`}
          aria-label="Toggle Audit Mode"
          title="Click to enable inline audit comments anywhere on the workspace"
        >
          <span className="audit-toggle__dot" />
          <span>Audit Mode: {isAuditMode ? 'ON' : 'OFF'}</span>
          {unresolvedComments > 0 && (
            <span
              style={{
                background: 'var(--color-primary)',
                color: '#ffffff',
                padding: '0 5px',
                borderRadius: '10px',
                fontSize: '10px',
                fontWeight: 700,
                marginLeft: '4px',
              }}
            >
              {unresolvedComments}
            </span>
          )}
        </button>
      </div>
    </header>
  );
}
