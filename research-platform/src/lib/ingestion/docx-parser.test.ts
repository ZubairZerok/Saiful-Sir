import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { parseDocxFile } from './docx-parser';

describe('DOCX conversion', () => {
  for (const fileName of ['Overall_p1.docx', 'Overall_P2.docx', 'Overall_p3.docx']) {
    it(`converts and sanitizes ${fileName} into auditable blocks`, async () => {
      const document = await parseDocxFile(path.join(process.cwd(), 'Step123', fileName));

      expect(document.blocks.length).toBeGreaterThan(5);
      expect(document.blocks.every((block, index) => block.index === index && block.id.startsWith('doc-block-'))).toBe(true);
      expect(document.blocks.some((block) => block.text.length > 0)).toBe(true);
      const html = document.blocks.map((block) => block.html).join('');
      expect(html).not.toMatch(/<script|javascript:|onerror=|onclick=/i);
    });
  }
});