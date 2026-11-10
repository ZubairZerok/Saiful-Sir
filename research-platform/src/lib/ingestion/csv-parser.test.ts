import path from 'node:path';
import { performance } from 'node:perf_hooks';
import { describe, expect, it } from 'vitest';
import { parseCsvFile } from './csv-parser';

const LARGE_CSV = path.resolve(
  process.cwd(),
  '..',
  'DAM_ANALYSIS_READY_2026',
  '07_outputs',
  'FULL_FLAGGED',
  'DAM_ALL_11_FULL_FLAGGED.csv'
);

describe('large CSV query engine', () => {
  it('preserves dimensions, source row identity, and quality-column metadata', () => {
    const result = parseCsvFile(LARGE_CSV, { page: 1, pageSize: 50 });

    expect(result.totalRows).toBe(3348);
    expect(result.totalColumns).toBe(63);
    expect(result.headers.filter((header) => header.startsWith('FLAG_'))).toHaveLength(14);
    expect(result.headers.filter((header) => header.startsWith('ELIGIBLE_')).length).toBeGreaterThan(0);
    expect(result.rowNumbers).toEqual(Array.from({ length: 50 }, (_, index) => index + 1));
  });

  it('performs cached search, sort, and pagination under the 100 ms target', () => {
    parseCsvFile(LARGE_CSV, { page: 1, pageSize: 50 });

    const searchStart = performance.now();
    const searched = parseCsvFile(LARGE_CSV, { search: 'true', pageSize: 50 });
    const searchMs = performance.now() - searchStart;

    const sortableColumn = searched.headers.find((header) => header === 'commodity_id') ?? searched.headers[0];
    const sortStart = performance.now();
    const sorted = parseCsvFile(LARGE_CSV, { sortBy: sortableColumn, sortOrder: 'desc', pageSize: 50 });
    const sortMs = performance.now() - sortStart;

    const pageStart = performance.now();
    const paged = parseCsvFile(LARGE_CSV, { page: 9999, pageSize: 50 });
    const pageMs = performance.now() - pageStart;

    expect(searched.totalRows).toBeGreaterThan(0);
    expect(sorted.rows).toHaveLength(50);
    expect(paged.page).toBe(paged.totalPages);
    expect(searchMs).toBeLessThan(100);
    expect(sortMs).toBeLessThan(100);
    expect(pageMs).toBeLessThan(100);
  });
});