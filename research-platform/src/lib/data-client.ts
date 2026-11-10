import Papa from 'papaparse';
import type { CsvData } from '@/types';

export interface ClientCsvResponse extends CsvData {
  page: number;
  pageSize: number;
  totalPages: number;
  sha256?: string;
  columnsMeta: {
    name: string;
    type: 'string' | 'number' | 'boolean' | 'date';
  }[];
}

/**
 * Fetch and parse a CSV file directly in the browser from /research_data/...
 */
export async function fetchAndParseCsvClient(
  relativePath: string,
  options: {
    page?: number;
    pageSize?: number;
    search?: string;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  } = {}
): Promise<ClientCsvResponse> {
  const url = `/research_data/${relativePath.replace(/^(\.\/|\/)/, '')}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to load CSV: ${res.statusText}`);
  }

  const csvText = await res.text();
  const parsed = Papa.parse<string[]>(csvText, {
    skipEmptyLines: true,
  });

  const allRows = parsed.data || [];
  if (allRows.length === 0) {
    return {
      headers: [],
      rows: [],
      totalRows: 0,
      totalColumns: 0,
      fileName: relativePath.split('/').pop() || '',
      page: 1,
      pageSize: 50,
      totalPages: 0,
      columnsMeta: [],
    };
  }

  const headers = allRows[0];
  let dataRows = allRows.slice(1);

  // Type inference
  const columnsMeta = headers.map((header, colIndex) => {
    let numCount = 0;
    let boolCount = 0;
    const checkLimit = Math.min(dataRows.length, 40);

    for (let r = 0; r < checkLimit; r++) {
      const val = dataRows[r][colIndex]?.trim();
      if (val !== undefined && val !== '') {
        if (!isNaN(Number(val))) numCount++;
        if (val.toLowerCase() === 'true' || val.toLowerCase() === 'false') boolCount++;
      }
    }

    let type: 'string' | 'number' | 'boolean' | 'date' = 'string';
    if (boolCount > checkLimit * 0.7) type = 'boolean';
    else if (numCount > checkLimit * 0.7) type = 'number';
    else if (header.includes('date') || header.includes('_at')) type = 'date';

    return { name: header, type };
  });

  // Global search filter
  if (options.search) {
    const q = options.search.toLowerCase();
    dataRows = dataRows.filter((row) =>
      row.some((cell) => cell && cell.toLowerCase().includes(q))
    );
  }

  // Sorting
  if (options.sortBy) {
    const sortIdx = headers.indexOf(options.sortBy);
    if (sortIdx >= 0) {
      const isNum = columnsMeta[sortIdx]?.type === 'number';
      const dir = options.sortOrder === 'desc' ? -1 : 1;
      dataRows.sort((a, b) => {
        const valA = a[sortIdx] || '';
        const valB = b[sortIdx] || '';
        if (isNum) {
          return (Number(valA) - Number(valB)) * dir;
        }
        return valA.localeCompare(valB) * dir;
      });
    }
  }

  const totalRows = dataRows.length;
  const page = Math.max(1, options.page || 1);
  const pageSize = Math.max(1, Math.min(options.pageSize || 50, 500));
  const totalPages = Math.ceil(totalRows / pageSize);

  const startIndex = (page - 1) * pageSize;
  const paginatedRows = dataRows.slice(startIndex, startIndex + pageSize);

  return {
    headers,
    rows: paginatedRows,
    totalRows,
    totalColumns: headers.length,
    fileName: relativePath.split('/').pop() || '',
    page,
    pageSize,
    totalPages,
    columnsMeta,
  };
}

/**
 * Fetch raw text / markdown / code file directly in the browser from /research_data/...
 */
export async function fetchTextArtifactClient(relativePath: string): Promise<string> {
  const url = `/research_data/${relativePath.replace(/^(\.\/|\/)/, '')}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to load file: ${res.statusText}`);
  }
  return await res.text();
}
