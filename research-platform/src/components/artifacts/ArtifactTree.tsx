'use client';

import React, { useState } from 'react';
import type { FileTreeNode } from '@/types';

interface ArtifactTreeProps {
  tree: FileTreeNode[];
  onSelectArtifact?: (artifactPath: string) => void;
  selectedPath?: string;
}

export function ArtifactTree({ tree, onSelectArtifact, selectedPath }: ArtifactTreeProps) {
  const [searchTerm, setSearchTerm] = useState('');

  const renderIcon = (type?: string, isDir?: boolean) => {
    if (isDir) {
      return (
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
        </svg>
      );
    }
    switch (type) {
      case 'csv':
        return (
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
            <line x1="18" y1="20" x2="18" y2="10" />
            <line x1="12" y1="20" x2="12" y2="4" />
            <line x1="6" y1="20" x2="6" y2="14" />
          </svg>
        );
      case 'md':
      case 'txt':
        return (
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
        );
      case 'py':
        return (
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
            <polyline points="16 18 22 12 16 6" />
            <polyline points="8 6 2 12 8 18" />
          </svg>
        );
      default:
        return (
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          </svg>
        );
    }
  };

  const renderNode = (node: FileTreeNode, depth = 0) => {
    if (searchTerm && !node.isDirectory && !node.name.toLowerCase().includes(searchTerm.toLowerCase())) {
      return null;
    }

    const isSelected = selectedPath === node.path;

    if (node.isDirectory) {
      return (
        <div key={node.path} style={{ marginLeft: depth > 0 ? '10px' : '0' }}>
          <div className="artifact-tree__item artifact-tree__item--dir">
            <span className="artifact-tree__icon">{renderIcon(undefined, true)}</span>
            <span className="artifact-tree__name">{node.name}</span>
          </div>
          {node.children && node.children.map((child) => renderNode(child, depth + 1))}
        </div>
      );
    }

    return (
      <div
        key={node.path}
        onClick={() => onSelectArtifact?.(node.path)}
        className={`artifact-tree__item ${isSelected ? 'artifact-tree__item--active' : ''}`}
        style={{ marginLeft: depth > 0 ? '10px' : '0' }}
        title={`${node.name} (${formatBytes(node.sizeBytes || 0)})`}
      >
        <span className="artifact-tree__icon">{renderIcon(node.fileType, false)}</span>
        <span className="artifact-tree__name">{node.name}</span>
        {node.sizeBytes !== undefined && (
          <span className="artifact-tree__size">{formatBytes(node.sizeBytes)}</span>
        )}
      </div>
    );
  };

  return (
    <div className="artifact-tree">
      <div style={{ padding: '0 12px 10px 12px' }}>
        <input
          type="text"
          placeholder="Filter artifacts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            background: 'var(--color-bg-secondary)',
            border: '1px solid var(--color-border)',
            borderRadius: 'var(--radius-sm)',
            padding: '5px 8px',
            fontSize: '11px',
            color: 'var(--color-text-primary)',
            outline: 'none',
          }}
        />
      </div>

      <div style={{ maxHeight: 'calc(100vh - 280px)', overflowY: 'auto', padding: '0 4px' }}>
        {tree.map((node) => renderNode(node))}
      </div>
    </div>
  );
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}
