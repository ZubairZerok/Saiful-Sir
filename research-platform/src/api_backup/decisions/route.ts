import { NextRequest, NextResponse } from 'next/server';
import { localStore } from '@/lib/store/local-store';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const stepId = searchParams.get('stepId') || undefined;

    const decisions = localStore.getDecisions(stepId);
    return NextResponse.json({ decisions });
  } catch (error) {
    console.error('Error fetching decisions', error);
    return NextResponse.json({ error: 'Failed to fetch decisions' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { stepId, decision, rationale, decidedBy } = body;

    if (!stepId || !decision || !rationale) {
      return NextResponse.json({ error: 'Missing stepId, decision or rationale' }, { status: 400 });
    }

    const newDecision = localStore.addDecision({
      stepId,
      decision,
      rationale,
      decidedBy: decidedBy || 'Supervisor / Lead Auditor',
    });

    return NextResponse.json({ decision: newDecision }, { status: 201 });
  } catch (error) {
    console.error('Error recording decision', error);
    return NextResponse.json({ error: 'Failed to save decision' }, { status: 500 });
  }
}
