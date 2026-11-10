import { describe, expect, it } from 'vitest';
import { isCommentAnchor, parseCommentInput } from './comments';

describe('comment input validation', () => {
  it('accepts a matching, trimmed anchored comment', () => {
    const parsed = parseCommentInput({
      artifactVersionId: ' sha256-version ',
      authorName: ' Reviewer ',
      authorRole: 'teacher',
      anchorType: 'csv_cell',
      anchorData: {
        type: 'csv_cell',
        rowKey: { sourceRow: 42 },
        columnName: 'FLAG_DUPLICATE',
        rowIndex: 42,
      },
      body: ' Check this observation. ',
    });

    expect(parsed).toMatchObject({
      artifactVersionId: 'sha256-version',
      authorName: 'Reviewer',
      authorId: 'user-default',
      body: 'Check this observation.',
    });
  });

  it('rejects mismatched anchor types and malformed numeric anchors', () => {
    expect(parseCommentInput({
      artifactVersionId: 'version',
      authorName: 'Reviewer',
      anchorType: 'general',
      anchorData: { type: 'csv_row', rowKey: {}, rowIndex: 1 },
      body: 'Mismatch',
    })).toBeNull();

    expect(isCommentAnchor({
      type: 'code_line',
      lineStart: Number.NaN,
      lineEnd: 3,
      contentHash: 'hash',
    })).toBe(false);
  });
});