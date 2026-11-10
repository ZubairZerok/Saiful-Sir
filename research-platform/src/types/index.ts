/* ============================================================
// Core TypeScript types for Auditinsyt.
   ============================================================ */

// ---------- Step Status ----------
export type StepStatus =
  | 'not_started'
  | 'in_progress'
  | 'review_requested'
  | 'changes_requested'
  | 'approved'
  | 'locked';

// ---------- User Roles ----------
export type UserRole = 'researcher' | 'teacher';

// ---------- Workflow Step ----------
export interface WorkflowStep {
  number: number;
  id: string;
  name: string;
  description: string;
  status: StepStatus;
  papers: string[];
  dependsOn: number[];
  artifactPatterns: string[];
  artifactRoot?: string;
  artifactCount?: number;
}

// ---------- Paper ----------
export interface Paper {
  id: string;
  title: string;
  subtitle: string;
  status: string;
  primaryPriceVar: string;
  targetSample: string;
}

// ---------- Project Config ----------
export interface ProjectConfig {
  project: {
    name: string;
    principalInvestigator: string;
    dataRoot: string;
    analysisRoot: string;
    rawOutputRoot: string;
  };
  papers: Paper[];
  datasetMetrics: {
    totalObservations: number;
    uniqueMarkets: number;
    commodityVarieties: number;
    temporalSpan: string;
    divisions: number;
    primaryAnalysisObs: number;
    strictSensitivityObs: number;
  };
}

// ---------- Artifact (file reference, not content) ----------
export interface Artifact {
  id: string;
  stepNumber: number;
  relativePath: string;
  fileName: string;
  fileType: ArtifactFileType;
  displayName: string;
  sizeBytes: number;
  isDirectory: boolean;
  children?: Artifact[];
}

export type ArtifactFileType = 'csv' | 'docx' | 'md' | 'py' | 'json' | 'txt' | 'png' | 'jpg' | 'unknown';

// ---------- Artifact Version ----------
export interface ArtifactVersion {
  id: string;
  artifactId: string;
  sha256Hash: string;
  fileSizeBytes: number;
  indexedAt: string;
  rowCount?: number;
  columnCount?: number;
  isCurrent: boolean;
}

// ---------- Comment Anchor Types ----------
export type CommentAnchorType =
  | 'markdown_block'
  | 'csv_cell'
  | 'csv_row'
  | 'figure_region'
  | 'code_line'
  | 'general';

export interface MarkdownBlockAnchor {
  type: 'markdown_block';
  headingPath: string[];
  blockHash: string;
  blockIndex: number;
}

export interface DocumentBlock {
  id: string;
  index: number;
  tagName: string;
  headingPath: string[];
  html: string;
  text: string;
}

export interface DocumentContent {
  blocks: DocumentBlock[];
  warnings: string[];
}

export interface CsvCellAnchor {
  type: 'csv_cell';
  rowKey: Record<string, string | number>;
  columnName: string;
  rowIndex: number;
}

export interface CsvRowAnchor {
  type: 'csv_row';
  rowKey: Record<string, string | number>;
  rowIndex: number;
}

export interface FigureRegionAnchor {
  type: 'figure_region';
  normalizedX: number;
  normalizedY: number;
  radius: number;
}

export interface CodeLineAnchor {
  type: 'code_line';
  lineStart: number;
  lineEnd: number;
  contentHash: string;
}

export interface GeneralAnchor {
  type: 'general';
}

export type CommentAnchor =
  | MarkdownBlockAnchor
  | CsvCellAnchor
  | CsvRowAnchor
  | FigureRegionAnchor
  | CodeLineAnchor
  | GeneralAnchor;

// ---------- Comment ----------
export interface Comment {
  id: string;
  artifactVersionId: string;
  authorId: string;
  authorName: string;
  authorRole: UserRole;
  anchorType: CommentAnchorType;
  anchorData: CommentAnchor;
  body: string;
  isResolved: boolean;
  resolvedBy?: string;
  resolvedAt?: string;
  parentCommentId?: string;
  createdAt: string;
  updatedAt: string;
  isStale?: boolean;
}

// ---------- Step Decision ----------
export interface StepDecision {
  id: string;
  stepId: string;
  decision: 'approved' | 'changes_requested' | 'locked';
  rationale: string;
  decidedBy: string;
  decidedAt: string;
}

// ---------- CSV Data for Viewer ----------
export interface CsvData {
  headers: string[];
  rows: string[][];
  totalRows: number;
  totalColumns: number;
  fileName: string;
}

// ---------- File Tree Node ----------
export interface FileTreeNode {
  name: string;
  path: string;
  isDirectory: boolean;
  sizeBytes?: number;
  children?: FileTreeNode[];
  fileType?: ArtifactFileType;
}

// ---------- Dashboard Metrics ----------
export interface DashboardMetrics {
  totalArtifacts: number;
  totalComments: number;
  pendingComments: number;
  stepsApproved: number;
  stepsTotal: number;
  lastActivity?: string;
}
