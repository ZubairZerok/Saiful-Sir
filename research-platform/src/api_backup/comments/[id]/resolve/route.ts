import { NextRequest, NextResponse } from 'next/server';
import { localStore } from '@/lib/store/local-store';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json().catch(() => ({}));
    const resolvedBy = body.resolvedBy || 'Reviewer';

    const updated = localStore.resolveComment(id, resolvedBy);
    if (!updated) {
      return NextResponse.json({ error: 'Comment not found' }, { status: 404 });
    }

    return NextResponse.json({ comment: updated });
  } catch (error) {
    console.error('Error resolving comment', error);
    return NextResponse.json({ error: 'Failed to resolve comment' }, { status: 500 });
  }
}
