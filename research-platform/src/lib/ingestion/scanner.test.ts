import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { getArtifactById, resolveArtifactPath, scanStepArtifacts } from './scanner';

describe('artifact scanner containment and DOCX discovery', () => {
  it('rejects traversal and paths outside configured artifact roots', () => {
    expect(resolveArtifactPath('../requirements.txt')).toBeNull();
    expect(resolveArtifactPath('research-platform/package.json')).toBeNull();
    expect(getArtifactById(Buffer.from('../requirements.txt').toString('base64url'))).toBeNull();
  });

  it('discovers the three first-class Step 1 DOCX documents without duplicates', () => {
    const artifacts = scanStepArtifacts(1);
    const docxNames = artifacts
      .filter((artifact) => artifact.fileType === 'docx')
      .map((artifact) => artifact.fileName)
      .sort();

    expect(docxNames).toEqual(['Overall_P2.docx', 'Overall_p1.docx', 'Overall_p3.docx']);
    expect(new Set(artifacts.map((artifact) => artifact.relativePath.toLowerCase())).size).toBe(artifacts.length);
    expect(artifacts.every((artifact) => !path.isAbsolute(artifact.relativePath))).toBe(true);
  });
});