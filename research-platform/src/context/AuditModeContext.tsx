'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import type { Comment, CommentAnchor } from '@/types';

const INITIAL_COMMENTS: Comment[] = [
  {
    id: 'comm-1',
    artifactVersionId: 'ver-readiness-report',
    authorId: 'supervisor-1',
    authorName: 'Prof. S. Ahmed (Advisor)',
    authorRole: 'teacher',
    anchorType: 'markdown_block',
    anchorData: {
      type: 'markdown_block',
      headingPath: ['Answers to the 16 Mandatory Forensic & Methodological Questions', '6. What is the primary analytical price variable and WHY?'],
      blockHash: 'block-p6',
      blockIndex: 6,
    },
    body: 'Excellent econometric rationale for using raw price midpoints (price_wholesale_raw_mid_kg) over DAM adjusted averages to avoid institutional smoothing distortion in Paper 1 and 2.',
    isResolved: false,
    createdAt: new Date(Date.now() - 3600000 * 4).toISOString(),
    updatedAt: new Date(Date.now() - 3600000 * 4).toISOString(),
  },
  {
    id: 'comm-2',
    artifactVersionId: 'ver-price-semantics',
    authorId: 'supervisor-1',
    authorName: 'Prof. S. Ahmed (Advisor)',
    authorRole: 'teacher',
    anchorType: 'csv_cell',
    anchorData: {
      type: 'csv_cell',
      rowKey: { market_id: '275', commodity_id: '831', price_date: '2026-02-25' },
      columnName: 'price_wholesale_raw_mid_kg',
      rowIndex: 0,
    },
    body: 'Note the 7.50 Tk/kg wholesale-retail spread for Chandina Bazar onion. This will serve as a clean baseline for Paper 3 flood shock transmission.',
    isResolved: false,
    createdAt: new Date(Date.now() - 3600000 * 2).toISOString(),
    updatedAt: new Date(Date.now() - 3600000 * 2).toISOString(),
  }
];

interface AuditModeContextType {
  isAuditMode: boolean;
  toggleAuditMode: () => void;
  userName: string;
  setUserName: (name: string) => void;
  activeAnchor: {
    anchor: CommentAnchor;
    artifactVersionId: string;
    parentCommentId?: string;
    targetRect?: { top: number; left: number; width: number; height: number };
  } | null;
  openComposer: (
    anchor: CommentAnchor,
    artifactVersionId: string,
    targetRect?: { top: number; left: number; width: number; height: number },
    parentCommentId?: string
  ) => void;
  closeComposer: () => void;
  comments: Comment[];
  refreshComments: () => Promise<void>;
  addComment: (body: string, parentCommentId?: string) => Promise<void>;
  resolveComment: (commentId: string) => Promise<void>;
  exportAuditData: () => void;
}

const AuditModeContext = createContext<AuditModeContextType | undefined>(undefined);

export function AuditModeProvider({ children }: { children: React.ReactNode }) {
  const [isAuditMode, setIsAuditMode] = useState<boolean>(true);
  const [userName, setUserName] = useState<string>('Auditor / Reviewer');
  const [comments, setComments] = useState<Comment[]>(INITIAL_COMMENTS);
  const [activeAnchor, setActiveAnchor] = useState<{
    anchor: CommentAnchor;
    artifactVersionId: string;
    parentCommentId?: string;
    targetRect?: { top: number; left: number; width: number; height: number };
  } | null>(null);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem('auditinsyt_comments');
      if (saved) {
        setComments(JSON.parse(saved));
      }
    } catch {
      // ignore
    }
  }, []);

  // Save to localStorage on updates
  const saveComments = (newComments: Comment[]) => {
    setComments(newComments);
    try {
      localStorage.setItem('auditinsyt_comments', JSON.stringify(newComments));
    } catch {
      // ignore
    }
  };

  const refreshComments = async () => {
    try {
      const saved = localStorage.getItem('auditinsyt_comments');
      if (saved) {
        setComments(JSON.parse(saved));
      }
    } catch {
      // ignore
    }
  };

  const toggleAuditMode = () => {
    setIsAuditMode((prev) => !prev);
    if (activeAnchor) setActiveAnchor(null);
  };

  const openComposer = (
    anchor: CommentAnchor,
    artifactVersionId: string,
    targetRect?: { top: number; left: number; width: number; height: number },
    parentCommentId?: string
  ) => {
    if (!isAuditMode) return;
    setActiveAnchor({ anchor, artifactVersionId, targetRect, parentCommentId });
  };

  const closeComposer = () => {
    setActiveAnchor(null);
  };

  const addComment = async (body: string, parentCommentId?: string) => {
    if (!activeAnchor || !body.trim()) return;

    const newComment: Comment = {
      id: `comm-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      artifactVersionId: activeAnchor.artifactVersionId,
      authorId: 'user-default',
      authorName: userName,
      authorRole: 'teacher',
      anchorType: activeAnchor.anchor.type,
      anchorData: activeAnchor.anchor,
      body,
      isResolved: false,
      parentCommentId: parentCommentId ?? activeAnchor.parentCommentId,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    saveComments([newComment, ...comments]);
    closeComposer();
  };

  const resolveComment = async (commentId: string) => {
    const resolvedAt = new Date().toISOString();
    const updated = comments.map((comment) =>
      comment.id === commentId
        ? { ...comment, isResolved: true, resolvedBy: userName, resolvedAt, updatedAt: resolvedAt }
        : comment
    );
    saveComments(updated);
  };

  const exportAuditData = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(comments, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `Auditinsyt_Audit_Log_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <AuditModeContext.Provider
      value={{
        isAuditMode,
        toggleAuditMode,
        userName,
        setUserName,
        activeAnchor,
        openComposer,
        closeComposer,
        comments,
        refreshComments,
        addComment,
        resolveComment,
        exportAuditData,
      }}
    >
      {children}
    </AuditModeContext.Provider>
  );
}

export function useAuditMode() {
  const context = useContext(AuditModeContext);
  if (!context) {
    throw new Error('useAuditMode must be used within an AuditModeProvider');
  }
  return context;
}
