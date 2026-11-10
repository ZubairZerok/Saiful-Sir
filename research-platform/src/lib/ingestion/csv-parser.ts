import fs from 'node:fs';
import Papa from 'papaparse';
import type { CsvData } from '@/types';

export interface CsvQueryOptions {
  page?: number;
  pageSize?: number;
  search?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  filterColumn?: string;
  filterValue?: string;
}

export interface CsvResponse extends CsvData {
  page: number;
  pageSize: number;
  totalPages: number;
  columnsMeta: {
    name: string;
    type: 'string' | 'number' | 'boolean' | 'date';
    sampleValues: (string | number | boolean)[];
  }[];
  /** One-based source row numbers, excluding the CSV header. */
  rowNumbers: number[];
}

interface IndexedRow {
  values: string[];
  sourceRowNumber: number;
}

interface ParsedCsvCacheEntry {
  signature: string;
  headers: string[];
  rows: IndexedRow[];
  columnsMeta: CsvResponse['columnsMeta'];
  fileName: string;
}

const MAX_CACHE_ENTRIES = 4;
const parsedCsvCache = new Map<string, ParsedCsvCacheEntry>();

function emptyResponse(fileName = ''): CsvResponse {
  return {
    headers: [],
    rows: [],
    rowNumbers: [],
    totalRows: 0,
    totalColumns: 0,
    fileName,
    page: 1,
    pageSize: 50,
    totalPages: 0,
    columnsMeta: [],
  };
}

function inferColumns(headers: string[], rows: IndexedRow[]): CsvResponse['columnsMeta'] {
  return headers.map((header, colIndex) => {
    let populatedCount = 0;
    let numCount = 0;
    let boolCount = 0;
    const samples: (string | number | boolean)[] = [];

    const checkLimit = Math.min(rows.length, 50);
    for (let r = 0; r < checkLimit; r++) {
      const val = rows[r].values[colIndex]?.trim();
      if (val) {
        populatedCount++;
        if (samples.length < 5) samples.push(val);
        if (Number.isFinite(Number(val))) numCount++;
        if (val.toLowerCase() === 'true' || val.toLowerCase() === 'false') boolCount++;
      }
    }

    let type: 'string' | 'number' | 'boolean' | 'date' = 'string';
    if (populatedCount > 0 && boolCount / populatedCount >= 0.7) {
      type = 'boolean';
    } else if (populatedCount > 0 && numCount / populatedCount >= 0.7) {
      type = 'number';
    } else if (header.toLowerCase().includes('date') || header.toLowerCase().includes('_at')) {
      type = 'date';
    }

    return { name: header, type, sampleValues: samples };
  });
}

function getParsedCsv(filePath: string): ParsedCsvCacheEntry | null {
  const stat = fs.statSync(filePath);
  const signature = `${stat.size}:${stat.mtimeMs}`;
  const cached = parsedCsvCache.get(filePath);
  if (cached?.signature === signature) {
    // Refresh insertion order so the map behaves as a small LRU cache.
    parsedCsvCache.delete(filePath);
    parsedCsvCache.set(filePath, cached);
    return cached;
  }

  const parsed = Papa.parse<string[]>(fs.readFileSync(filePath, 'utf-8'), {
    skipEmptyLines: true,
  });
  if (parsed.errors.length > 0) {
    const fatal = parsed.errors.find((error) => error.type === 'Quotes');
    if (fatal) throw new Error(`Malformed CSV at row ${fatal.row ?? 'unknown'}: ${fatal.message}`);
  }

  const allRows = parsed.data;
  if (!allRows?.length) return null;

  const headers = allRows[0].map((header) => header.trim());
  const rows = allRows.slice(1).map((values, index) => ({
    values,
    sourceRowNumber: index + 1,
  }));
  const entry: ParsedCsvCacheEntry = {
    signature,
    headers,
    rows,
    columnsMeta: inferColumns(headers, rows),
    fileName: filePath.split(/[\\/]/).pop() || '',
  };

  parsedCsvCache.delete(filePath);
  parsedCsvCache.set(filePath, entry);
  while (parsedCsvCache.size > MAX_CACHE_ENTRIES) {
    const oldestKey = parsedCsvCache.keys().next().value;
    if (oldestKey === undefined) break;
    parsedCsvCache.delete(oldestKey);
  }
  return entry;
}

/**
 * Stream & parse CSV file with server-side pagination, sorting, search, and type inference.
 */
export function parseCsvFile(filePath: string, options: CsvQueryOptions = {}): CsvResponse {
  if (!fs.existsSync(filePath)) {
    return emptyResponse();
  }

  const parsed = getParsedCsv(filePath);
  if (!parsed) return emptyResponse(filePath.split(/[\\/]/).pop() || '');
  const { headers, columnsMeta, fileName } = parsed;
  let dataRows = parsed.rows;

  // Global Search Filter
  if (options.search) {
    const q = options.search.toLowerCase();
    dataRows = dataRows.filter((row) =>
      row.values.some((cell) => cell && cell.toLowerCase().includes(q))
    );
  }

  // Specific Column Filter
  if (options.filterColumn && options.filterValue !== undefined && options.filterValue !== '') {
    const colIdx = headers.indexOf(options.filterColumn);
    if (colIdx >= 0) {
      const target = options.filterValue.toLowerCase();
      dataRows = dataRows.filter((row) =>
        row.values[colIdx] && row.values[colIdx].toLowerCase() === target
      );
    }
  }

  // Sorting
  if (options.sortBy) {
    const sortIdx = headers.indexOf(options.sortBy);
    if (sortIdx >= 0) {
      const isNum = columnsMeta[sortIdx]?.type === 'number';
      const dir = options.sortOrder === 'desc' ? -1 : 1;
      dataRows = [...dataRows].sort((a, b) => {
        const valA = a.values[sortIdx] || '';
        const valB = b.values[sortIdx] || '';
        if (isNum) {
          const numericComparison = Number(valA) - Number(valB);
          return (numericComparison || a.sourceRowNumber - b.sourceRowNumber) * dir;
        }
        return (valA.localeCompare(valB) || a.sourceRowNumber - b.sourceRowNumber) * dir;
      });
    }
  }

  const totalRows = dataRows.length;
  const requestedPage = Math.max(1, options.page || 1);
  const pageSize = Math.max(1, Math.min(options.pageSize || 100, 1000));
  const totalPages = Math.ceil(totalRows / pageSize);
  const page = totalPages > 0 ? Math.min(requestedPage, totalPages) : 1;

  const startIndex = (page - 1) * pageSize;
  const paginatedRows = dataRows.slice(startIndex, startIndex + pageSize);

  return {
    headers,
    rows: paginatedRows.map((row) => row.values),
    rowNumbers: paginatedRows.map((row) => row.sourceRowNumber),
    totalRows,
    totalColumns: headers.length,
    fileName,
    page,
    pageSize,
    totalPages,
    columnsMeta,
  };
}
