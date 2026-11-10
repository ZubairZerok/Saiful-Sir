import { NextRequest, NextResponse } from 'next/server';
import fs from 'node:fs';
import { getArtifactById } from '@/lib/ingestion/scanner';
import { parseDocxFile } from '@/lib/ingestion/docx-parser';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const lookup = getArtifactById(id);

    if (!lookup) {
      return NextResponse.json({ error: 'Artifact not found' }, { status: 404 });
    }

    const { artifact, fullPath, sha256 } = lookup;
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      return NextResponse.json({
        artifact,
        sha256,
        isDirectory: true,
      });
    }

    if (artifact.fileType === 'docx') {
      const document = await parseDocxFile(fullPath);
      return NextResponse.json({ artifact, sha256, document });
    }

    // For text-based artifacts, return string content
    if (['md', 'py', 'json', 'txt', 'csv'].includes(artifact.fileType)) {
      const content = fs.readFileSync(fullPath, 'utf-8');
      return NextResponse.json({
        artifact,
        sha256,
        content,
      });
    }

    if (!['png', 'jpg'].includes(artifact.fileType)) {
      return NextResponse.json({ error: 'Unsupported artifact type' }, { status: 415 });
    }

    // For supported images
    const buffer = fs.readFileSync(fullPath);
    return new NextResponse(buffer, {
      headers: {
        'Content-Type': artifact.fileType === 'png' ? 'image/png' : 'image/jpeg',
        'X-Artifact-Sha256': sha256,
      },
    });
  } catch (error) {
    console.error('Error fetching artifact', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
