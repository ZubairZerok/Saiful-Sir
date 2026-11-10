import crypto from 'node:crypto';
import mammoth from 'mammoth';
import sanitizeHtml from 'sanitize-html';
import type { DocumentBlock, DocumentContent } from '@/types';

const STYLE_MAP = [
  "p[style-name='Title'] => h1:fresh",
  "p[style-name='Subtitle'] => p.docx-subtitle:fresh",
  "p[style-name='Heading 1'] => h1:fresh",
  "p[style-name='Heading 2'] => h2:fresh",
  "p[style-name='Heading 3'] => h3:fresh",
  "p[style-name='Heading 4'] => h4:fresh",
];

const SANITIZE_OPTIONS: sanitizeHtml.IOptions = {
  allowedTags: [
    'p', 'div', 'span', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'sub', 'sup',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'thead',
    'tbody', 'tfoot', 'tr', 'th', 'td', 'a', 'blockquote', 'pre', 'code', 'hr',
  ],
  allowedAttributes: {
    a: ['href', 'title'],
    td: ['colspan', 'rowspan'],
    th: ['colspan', 'rowspan', 'scope'],
    span: ['class'],
    p: ['class'],
  },
  allowedClasses: {
    p: ['docx-subtitle'],
    span: ['small-caps', 'underline'],
  },
  allowedSchemes: ['http', 'https', 'mailto'],
};

function decodeEntities(value: string): string {
  return value
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

function splitIntoBlocks(html: string): DocumentBlock[] {
  const blockPattern = /<(h[1-6]|p|ul|ol|table|blockquote|pre|hr)(?:\s[^>]*)?>[\s\S]*?<\/\1>|<hr(?:\s[^>]*)?\s*\/?>/gi;
  const headingPath: string[] = [];

  return (html.match(blockPattern) ?? []).map((blockHtml, index) => {
    const tagName = blockHtml.match(/^<([a-z0-9]+)/i)?.[1].toLowerCase() ?? 'p';
    const text = decodeEntities(blockHtml);
    const headingMatch = tagName.match(/^h([1-6])$/);
    if (headingMatch) {
      const level = Number(headingMatch[1]);
      headingPath.splice(level - 1);
      headingPath[level - 1] = text;
    }
    const digest = crypto.createHash('sha256').update(`${tagName}\0${text}`).digest('hex').slice(0, 16);
    return {
      id: `doc-block-${index}-${digest}`,
      index,
      tagName,
      headingPath: headingPath.filter(Boolean),
      html: blockHtml,
      text,
    };
  });
}

export async function parseDocxFile(filePath: string): Promise<DocumentContent> {
  const result = await mammoth.convertToHtml(
    { path: filePath },
    {
      styleMap: STYLE_MAP,
      includeDefaultStyleMap: true,
      convertImage: mammoth.images.imgElement(() => Promise.resolve({ src: '' })),
    }
  );
  const cleanHtml = sanitizeHtml(result.value, SANITIZE_OPTIONS);
  return {
    blocks: splitIntoBlocks(cleanHtml),
    warnings: result.messages.map((message) => message.message),
  };
}