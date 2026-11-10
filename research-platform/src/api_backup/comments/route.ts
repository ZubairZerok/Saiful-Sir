import { NextRequest, NextResponse } from 'next/server';
import { localStore } from '@/lib/store/local-store';
import { parseCommentInput } from '@/lib/validation/comments';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const versionId = searchParams.get('versionId') || undefined;
    const comments = versionId
      ? localStore.getComments(versionId)
      : localStore.getAllComments();

    return NextResponse.json({ comments });
  } catch (error) {
    console.error('Error getting comments', error);
    return NextResponse.json({ error: 'Failed to fetch comments' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const input = parseCommentInput(await request.json());
    if (!input) {
      return NextResponse.json({ error: 'Invalid comment payload' }, { status: 400 });
    }

    const newComment = localStore.addComment(input);

    return NextResponse.json({ comment: newComment }, { status: 201 });
  } catch (error) {
    console.error('Error adding comment', error);
    const message = error instanceof Error ? error.message : 'Failed to create comment';
    const status = message.includes('Parent comment') ? 400 : 500;
    return NextResponse.json({ error: message }, { status });
  }
}
