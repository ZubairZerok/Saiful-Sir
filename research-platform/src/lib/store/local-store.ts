import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import type { Comment, StepDecision, StepStatus } from '@/types';

interface StoreData {
  comments: Comment[];
  decisions: StepDecision[];
  stepStatuses: Record<number, StepStatus>;
}

const STORE_PATH = path.join(process.cwd(), '.audit_data.json');

function getInitialData(): StoreData {
  // Steps 1-11 are complete in the checked-in workflow registry.
  const defaultStatuses: Record<number, StepStatus> = {
    1: 'approved',
    2: 'approved',
    3: 'approved',
    4: 'approved',
    5: 'approved',
    6: 'approved',
    7: 'approved',
    8: 'approved',
    9: 'approved',
    10: 'approved',
    11: 'approved',
    12: 'not_started',
    13: 'not_started',
    14: 'not_started',
    15: 'not_started',
    16: 'not_started',
    17: 'not_started',
  };

  const initialDecisions: StepDecision[] = [
    {
      id: 'dec-step-11',
      stepId: 'step-11',
      decision: 'approved',
      rationale: 'Validated against all 16 mandatory forensic questions. Paper 2 analysis-ready, Papers 1 & 3 ready with conditions.',
      decidedBy: 'Supervisor / Lead Auditor',
      decidedAt: new Date().toISOString(),
    },
    {
      id: 'dec-step-9',
      stepId: 'step-9',
      decision: 'approved',
      rationale: 'Three distinct tiers (FULL_FLAGGED, PRIMARY_ANALYSIS, STRICT_SENSITIVITY) generated with 14 boolean quality flags.',
      decidedBy: 'Supervisor / Lead Auditor',
      decidedAt: new Date().toISOString(),
    },
    {
      id: 'dec-step-6',
      stepId: 'step-6',
      decision: 'approved',
      rationale: 'Semantic resolution verified: w_avgPrice is mathematically the midpoint of adjusted prices, not raw quotes.',
      decidedBy: 'Supervisor / Lead Auditor',
      decidedAt: new Date().toISOString(),
    }
  ];

  const initialComments: Comment[] = [
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

  return {
    comments: initialComments,
    decisions: initialDecisions,
    stepStatuses: defaultStatuses,
  };
}

function readStore(): StoreData {
  try {
    if (fs.existsSync(STORE_PATH)) {
      const content = fs.readFileSync(STORE_PATH, 'utf-8');
      const parsed = JSON.parse(content) as Partial<StoreData>;
      const initial = getInitialData();
      return {
        comments: Array.isArray(parsed.comments) ? parsed.comments : initial.comments,
        decisions: Array.isArray(parsed.decisions) ? parsed.decisions : initial.decisions,
        stepStatuses: { ...initial.stepStatuses, ...(parsed.stepStatuses ?? {}) },
      };
    }
  } catch (e) {
    console.error('Error reading store, resetting to initial', e);
  }
  const initial = getInitialData();
  writeStore(initial);
  return initial;
}

function writeStore(data: StoreData): void {
  const tempPath = `${STORE_PATH}.${process.pid}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(tempPath, JSON.stringify(data, null, 2), 'utf-8');
    fs.renameSync(tempPath, STORE_PATH);
  } catch (e) {
    fs.rmSync(tempPath, { force: true });
    console.error('Error writing store', e);
    throw e;
  }
}

export const localStore = {
  getComments: (artifactVersionId?: string): Comment[] => {
    const data = readStore();
    if (artifactVersionId) {
      return data.comments.filter((c) => c.artifactVersionId === artifactVersionId);
    }
    return data.comments;
  },

  getAllComments: (): Comment[] => {
    return readStore().comments;
  },

  addComment: (comment: Omit<Comment, 'id' | 'createdAt' | 'updatedAt' | 'isResolved'>): Comment => {
    const data = readStore();
    if (comment.parentCommentId) {
      const parent = data.comments.find((item) => item.id === comment.parentCommentId);
      if (!parent || parent.artifactVersionId !== comment.artifactVersionId) {
        throw new Error('Parent comment does not belong to this artifact version');
      }
    }
    const newComment: Comment = {
      ...comment,
      id: crypto.randomUUID(),
      isResolved: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    data.comments.unshift(newComment);
    writeStore(data);
    return newComment;
  },

  resolveComment: (commentId: string, resolvedBy: string): Comment | null => {
    const data = readStore();
    const comment = data.comments.find((c) => c.id === commentId);
    if (!comment) return null;
    comment.isResolved = true;
    comment.resolvedBy = resolvedBy;
    comment.resolvedAt = new Date().toISOString();
    comment.updatedAt = new Date().toISOString();
    writeStore(data);
    return comment;
  },

  getDecisions: (stepId?: string): StepDecision[] => {
    const data = readStore();
    if (stepId) {
      return data.decisions.filter((d) => d.stepId === stepId);
    }
    return data.decisions;
  },

  addDecision: (decision: Omit<StepDecision, 'id' | 'decidedAt'>): StepDecision => {
    const data = readStore();
    const newDec: StepDecision = {
      ...decision,
      id: `dec-${Date.now()}`,
      decidedAt: new Date().toISOString(),
    };
    data.decisions.unshift(newDec);
    
    // Update step status accordingly
    const stepNum = parseInt(decision.stepId.replace('step-', ''), 10);
    if (!isNaN(stepNum)) {
      data.stepStatuses[stepNum] = decision.decision === 'approved' ? 'approved' : 'changes_requested';
    }
    
    writeStore(data);
    return newDec;
  },

  getStepStatus: (stepNumber: number): StepStatus => {
    const data = readStore();
    return data.stepStatuses[stepNumber] || 'not_started';
  },

  updateStepStatus: (stepNumber: number, status: StepStatus): void => {
    const data = readStore();
    data.stepStatuses[stepNumber] = status;
    writeStore(data);
  },
};
