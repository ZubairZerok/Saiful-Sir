import { NextRequest, NextResponse } from 'next/server';
import { getArtifactById } from '@/lib/ingestion/scanner';
import { parseCsvFile } from '@/lib/ingestion/csv-parser';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const lookup = getArtifactById(id);

    if (!lookup) {
      return NextResponse.json({ error: 'CSV Artifact not found' }, { status: 404 });
    }

    const { artifact, fullPath, sha256 } = lookup;
    if (artifact.fileType !== 'csv') {
      return NextResponse.json({ error: 'Artifact is not a CSV file' }, { status: 415 });
    }
    const searchParams = request.nextUrl.searchParams;

    const parseBoundedInteger = (value: string | null, fallback: number, min: number, max: number) => {
      const parsed = Number(value);
      return Number.isInteger(parsed) ? Math.min(max, Math.max(min, parsed)) : fallback;
    };
    const page = parseBoundedInteger(searchParams.get('page'), 1, 1, Number.MAX_SAFE_INTEGER);
    const pageSize = parseBoundedInteger(searchParams.get('pageSize'), 50, 1, 1000);
    const search = searchParams.get('search')?.trim().slice(0, 200) || undefined;
    const sortBy = searchParams.get('sortBy') || undefined;
    const requestedSortOrder = searchParams.get('sortOrder');
    const sortOrder = requestedSortOrder === 'desc' ? 'desc' : 'asc';
    const filterColumn = searchParams.get('filterColumn') || undefined;
    const filterValue = searchParams.get('filterValue') || undefined;

    const startedAt = performance.now();
    const parsed = parseCsvFile(fullPath, {
      page,
      pageSize,
      search,
      sortBy,
      sortOrder,
      filterColumn,
      filterValue,
    });

    return NextResponse.json({
      ...parsed,
      sha256,
    }, {
      headers: {
        'Cache-Control': 'private, no-store',
        'Server-Timing': `csv;dur=${(performance.now() - startedAt).toFixed(1)}`,
      },
    });
  } catch (error) {
    console.error('Error querying CSV', error);
    return NextResponse.json({ error: 'Failed to process CSV file' }, { status: 500 });
  }
}
