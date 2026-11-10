'use client';

import React, { useState, useEffect, useDeferredValue } from 'react';
import { ArrowDownAZ, ArrowUpAZ, ChevronLeft, ChevronRight, Search, X } from 'lucide-react';
import { useAuditMode } from '@/context/AuditModeContext';

interface CsvViewerProps {
  artifactId: string;
  fileName: string;
}

interface CsvDataState {
  headers: string[];
  rows: string[][];
  rowNumbers: number[];
  totalRows: number;
  totalColumns: number;
  page: number;
  pageSize: number;
  totalPages: number;
  sha256?: string;
}

export function CsvViewer({ artifactId, fileName }: CsvViewerProps) {
  const { isAuditMode, openComposer } = useAuditMode();
  const [data, setData] = useState<CsvDataState | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const deferredSearch = useDeferredValue(search.trim());
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [sortBy, setSortBy] = useState<string>('');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    const controller = new AbortController();
    const params = new URLSearchParams({ page: page.toString(), pageSize: pageSize.toString() });
    if (deferredSearch) params.set('search', deferredSearch);
    if (sortBy) {
      params.set('sortBy', sortBy);
      params.set('sortOrder', sortOrder);
    }

    // Try API first, fallback to client-side static parser
    fetch(`/api/csv/${artifactId}?${params.toString()}`, { signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) throw new Error('API not available, switching to client parser');
        return await res.json();
      })
      .then((json) => {
        setData(json);
        setError(null);
      })
      .catch(async (err) => {
        if (err instanceof DOMException && err.name === 'AbortError') return;
        try {
          // Decode relative path from artifactId
          let rel = '';
          try {
            rel = atob(artifactId.replace(/-/g, '+').replace(/_/g, '/'));
          } catch {
            rel = artifactId;
          }
          const clientData = await import('@/lib/data-client').then((m) =>
            m.fetchAndParseCsvClient(rel, {
              page,
              pageSize,
              search: deferredSearch,
              sortBy,
              sortOrder,
            })
          );
          setData({
            ...clientData,
            rowNumbers: clientData.rows.map((_, i) => (page - 1) * pageSize + i + 1),
          });
          setError(null);
        } catch (clientErr) {
          console.error('Error in client CSV parse', clientErr);
          setError('Unable to load CSV dataset');
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [artifactId, page, pageSize, deferredSearch, sortBy, sortOrder]);

  const handleHeaderClick = (header: string) => {
    setLoading(true);
    setError(null);
    if (sortBy === header) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(header);
      setSortOrder('asc');
    }
    setPage(1);
  };

  const handleCellClick = (
    e: React.MouseEvent,
    row: string[],
    rowIndex: number,
    colName: string
  ) => {
    if (!isAuditMode || !data) return;

    const rowKey: Record<string, string | number> = {};
    const marketIdIdx = data.headers.indexOf('market_id');
    const commIdIdx = data.headers.indexOf('commodity_id');
    const dateIdx = data.headers.indexOf('price_date');
    const rowIdIdx = data.headers.indexOf('row_id');

    if (marketIdIdx >= 0) rowKey.market_id = row[marketIdIdx];
    if (commIdIdx >= 0) rowKey.commodity_id = row[commIdIdx];
    if (dateIdx >= 0) rowKey.price_date = row[dateIdx];
    if (rowIdIdx >= 0) rowKey.row_id = row[rowIdIdx];

    const rect = e.currentTarget.getBoundingClientRect();

    openComposer(
      {
        type: 'csv_cell',
        rowKey,
        columnName: colName,
        rowIndex: data.rowNumbers[rowIndex] ?? (page - 1) * pageSize + rowIndex + 1,
      },
      data.sha256 || artifactId,
      {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        width: rect.width,
        height: rect.height,
      }
    );
  };

  if (!data && loading) {
    return (
      <div className="csv-viewer" style={{ padding: '40px', textAlign: 'center' }}>
        <div style={{ color: 'var(--color-primary)', fontWeight: 600 }}>
          Loading dataset from filesystem source...
        </div>
      </div>
    );
  }

  if (!data) {
    return <div className="empty-state">{error || 'Unable to load dataset.'}</div>;
  }

  return (
    <div className="csv-viewer">
      <div className="csv-viewer__toolbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <strong style={{ color: 'var(--color-text-primary)' }}>{fileName}</strong>
          <span>
            {data.totalRows.toLocaleString()} rows × {data.totalColumns} cols
          </span>
          {data.sha256 && (
            <span
              style={{
                fontSize: '11px',
                background: 'var(--color-bg-tertiary)',
                padding: '2px 6px',
                borderRadius: 'var(--radius-xs)',
                fontFamily: 'var(--font-code)',
              }}
            >
              SHA-256: {data.sha256.substring(0, 8)}...
            </span>
          )}
        </div>

        <div className="csv-viewer__actions">
          {isAuditMode && (
            <span
              style={{
                color: 'var(--color-primary)',
                fontSize: '11px',
                fontWeight: 600,
              }}
            >
              Cell anchoring enabled
            </span>
          )}

          <label className="csv-viewer__search">
            <Search size={14} aria-hidden="true" />
            <span className="sr-only">Search in table</span>
            <input
              type="search"
              placeholder="Search in table"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); setLoading(true); setError(null); }}
            />
            {search && <button type="button" onClick={() => { setSearch(''); setPage(1); setLoading(true); setError(null); }} aria-label="Clear search" title="Clear search"><X size={14} /></button>}
          </label>
        </div>
      </div>

      {error && <div className="csv-viewer__error" role="alert">{error}</div>}

      <div className={`csv-viewer__table-wrap ${loading ? 'is-loading' : ''}`} aria-busy={loading}>
        <table>
          <thead>
            <tr>
              <th className="csv-viewer__row-number">#</th>
              {data.headers.map((h) => (
                <th
                  key={h}
                  onClick={() => handleHeaderClick(h)}
                  title={`Sort by ${h}`}
                >
                  <div className="csv-viewer__column-heading">
                    <span>{h}</span>
                    {sortBy === h && (
                      sortOrder === 'asc' ? <ArrowDownAZ size={13} aria-label="Sorted ascending" /> : <ArrowUpAZ size={13} aria-label="Sorted descending" />
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.rows.map((row, rowIdx) => {
              const actualRowIdx = data.rowNumbers[rowIdx] ?? (data.page - 1) * data.pageSize + rowIdx + 1;
              return (
                <tr key={rowIdx}>
                  <td
                    className="csv-viewer__row-number"
                    style={{
                      textAlign: 'center',
                      color: 'var(--color-text-muted)',
                      fontSize: '11px',
                    }}
                  >
                    {actualRowIdx}
                  </td>
                  {row.map((cell, colIdx) => {
                    const colName = data.headers[colIdx];
                    let cellCls = '';

                    if (colName.startsWith('FLAG_')) {
                      cellCls =
                        cell.toLowerCase() === 'true'
                          ? 'csv-viewer__flag-true'
                          : 'csv-viewer__flag-false';
                    } else if (colName.startsWith('ELIGIBLE_')) {
                      cellCls =
                        cell.toLowerCase() === 'true'
                          ? 'csv-viewer__eligible-true'
                          : 'csv-viewer__eligible-false';
                    }

                    return (
                      <td
                        key={colIdx}
                        className={cellCls}
                        onClick={(e) => handleCellClick(e, row, rowIdx, colName)}
                        style={{
                          cursor: isAuditMode ? 'crosshair' : 'default',
                        }}
                        title={isAuditMode ? `Click to comment on ${colName}` : cell}
                      >
                        {cell}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="csv-viewer__footer">
        <div>
          {data.totalRows === 0 ? 'No matching rows' : <>Showing {(data.page - 1) * data.pageSize + 1}-{Math.min(data.page * data.pageSize, data.totalRows)} of {data.totalRows}</>}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
              setPage(1);
              setLoading(true);
              setError(null);
            }}
            style={{
              background: 'var(--color-bg-primary)',
              border: '1px solid var(--color-border)',
              color: 'var(--color-text-primary)',
              borderRadius: 'var(--radius-sm)',
              padding: '2px 6px',
              fontSize: '11px',
            }}
          >
            <option value={25}>25 rows</option>
            <option value={50}>50 rows</option>
            <option value={100}>100 rows</option>
            <option value={200}>200 rows</option>
          </select>

          <button
            onClick={() => { setPage((p) => Math.max(1, p - 1)); setLoading(true); setError(null); }}
            disabled={data.page <= 1}
            className="btn btn--icon"
            aria-label="Previous page"
            title="Previous page"
          >
            <ChevronLeft size={15} />
          </button>

          <span>
            Page {data.page} of {data.totalPages || 1}
          </span>

          <button
            onClick={() => { setPage((p) => Math.min(data.totalPages, p + 1)); setLoading(true); setError(null); }}
            disabled={data.page >= data.totalPages}
            className="btn btn--icon"
            aria-label="Next page"
            title="Next page"
          >
            <ChevronRight size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}
