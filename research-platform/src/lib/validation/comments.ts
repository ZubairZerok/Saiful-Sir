import type { CommentAnchor, CommentAnchorType, UserRole } from '@/types';

const ANCHOR_TYPES = new Set<CommentAnchorType>([
  'markdown_block',
  'csv_cell',
  'csv_row',
  'figure_region',
  'code_line',
  'general',
]);

const USER_ROLES = new Set<UserRole>(['researcher', 'teacher']);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value);
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === 'string');
}

export function isCommentAnchor(value: unknown): value is CommentAnchor {
  if (!isRecord(value) || typeof value.type !== 'string' || !ANCHOR_TYPES.has(value.type as CommentAnchorType)) {
    return false;
  }

  switch (value.type) {
    case 'general':
      return true;
    case 'markdown_block':
      return isStringArray(value.headingPath)
        && typeof value.blockHash === 'string'
        && isFiniteNumber(value.blockIndex);
    case 'csv_cell':
      return isRecord(value.rowKey)
        && typeof value.columnName === 'string'
        && isFiniteNumber(value.rowIndex);
    case 'csv_row':
      return isRecord(value.rowKey) && isFiniteNumber(value.rowIndex);
    case 'figure_region':
      return isFiniteNumber(value.normalizedX)
        && isFiniteNumber(value.normalizedY)
        && isFiniteNumber(value.radius);
    case 'code_line':
      return isFiniteNumber(value.lineStart)
        && isFiniteNumber(value.lineEnd)
        && typeof value.contentHash === 'string';
    default:
      return false;
  }
}

export interface ValidCommentInput {
  artifactVersionId: string;
  authorId: string;
  authorName: string;
  authorRole: UserRole;
  anchorType: CommentAnchorType;
  anchorData: CommentAnchor;
  body: string;
  parentCommentId?: string;
}

export function parseCommentInput(value: unknown): ValidCommentInput | null {
  if (!isRecord(value) || !isCommentAnchor(value.anchorData)) return null;

  const artifactVersionId = typeof value.artifactVersionId === 'string' ? value.artifactVersionId.trim() : '';
  const authorName = typeof value.authorName === 'string' ? value.authorName.trim() : '';
  const commentBody = typeof value.body === 'string' ? value.body.trim() : '';
  const anchorType = value.anchorType;
  const authorRole = value.authorRole ?? 'teacher';
  const parentCommentId = typeof value.parentCommentId === 'string' ? value.parentCommentId.trim() : undefined;

  if (
    !artifactVersionId
    || artifactVersionId.length > 512
    || !authorName
    || authorName.length > 120
    || !commentBody
    || commentBody.length > 10_000
    || typeof anchorType !== 'string'
    || anchorType !== value.anchorData.type
    || !ANCHOR_TYPES.has(anchorType as CommentAnchorType)
    || typeof authorRole !== 'string'
    || !USER_ROLES.has(authorRole as UserRole)
    || (parentCommentId !== undefined && (!parentCommentId || parentCommentId.length > 128))
  ) {
    return null;
  }

  return {
    artifactVersionId,
    authorId: typeof value.authorId === 'string' && value.authorId.trim()
      ? value.authorId.trim().slice(0, 128)
      : 'user-default',
    authorName,
    authorRole: authorRole as UserRole,
    anchorType: anchorType as CommentAnchorType,
    anchorData: value.anchorData,
    body: commentBody,
    parentCommentId,
  };
}
