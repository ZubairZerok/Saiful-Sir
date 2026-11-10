import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { loadProjectConfig, loadStepRegistry } from '@/lib/config';
import type { Artifact, ArtifactFileType, FileTreeNode } from '@/types';

function getFileType(filePath: string): ArtifactFileType {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case '.csv':
      return 'csv';
    case '.md':
      return 'md';
    case '.docx':
      return 'docx';
    case '.py':
      return 'py';
    case '.json':
      return 'json';
    case '.txt':
      return 'txt';
    case '.png':
      return 'png';
    case '.jpg':
    case '.jpeg':
      return 'jpg';
    default:
      return 'unknown';
  }
}

export function computeFileSha256(filePath: string): string {
  const fileBuffer = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(fileBuffer).digest('hex');
}

function canonicalPath(filePath: string): string {
  return fs.realpathSync.native(path.resolve(filePath));
}

function isPathInside(rootPath: string, candidatePath: string): boolean {
  const relative = path.relative(rootPath, candidatePath);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function getAllowedRoots(): string[] {
  const config = loadProjectConfig();
  return [
    config.project.rawOutputRoot,
    config.project.analysisRoot,
    path.join(process.cwd(), 'Step123'),
  ]
    .filter((root) => fs.existsSync(root))
    .map(canonicalPath);
}

export function resolveArtifactPath(relativePath: string): string | null {
  const config = loadProjectConfig();
  if (!relativePath || path.isAbsolute(relativePath) || relativePath.includes('\0')) return null;

  const candidate = path.resolve(config.project.dataRoot, relativePath);
  if (!fs.existsSync(candidate)) return null;

  const resolvedCandidate = canonicalPath(candidate);
  return getAllowedRoots().some((root) => isPathInside(root, resolvedCandidate))
    ? resolvedCandidate
    : null;
}

/**
 * Scan a specific step directory or matching patterns and return list of Artifact objects.
 */
export function scanStepArtifacts(stepNumber: number): Artifact[] {
  const config = loadProjectConfig();
  const steps = loadStepRegistry();
  const step = steps.find((s) => s.number === stepNumber);
  if (!step) return [];

  const artifacts = new Map<string, Artifact>();
  const projectRoot = config.project.dataRoot;

  // Search patterns / directories
  const searchPaths: string[] = [];
  if (step.artifactRoot) {
    const configuredRoot = path.isAbsolute(step.artifactRoot)
      ? step.artifactRoot
      : path.resolve(projectRoot, step.artifactRoot);
    if (fs.existsSync(configuredRoot)) searchPaths.push(configuredRoot);
  }

  // Fallback / standard mappings for the 17 steps
  if (stepNumber === 1) {
    searchPaths.push(path.join(projectRoot, 'research-platform', 'Step123', 'step1_research_questions_and_hypotheses.md'));
    searchPaths.push(path.join(projectRoot, 'research-platform', 'Step123', 'Overall_p1.docx'));
    searchPaths.push(path.join(projectRoot, 'research-platform', 'Step123', 'Overall_P2.docx'));
    searchPaths.push(path.join(projectRoot, 'research-platform', 'Step123', 'Overall_p3.docx'));
  } else if (stepNumber === 2) {
    searchPaths.push(path.join(projectRoot, 'research-platform', 'Step123', 'step2_literature_review_and_matrix.md'));
  } else if (stepNumber === 3) {
    searchPaths.push(path.join(projectRoot, 'research-platform', 'Step123', 'step3_data_sources_and_registry.md'));
  } else if (stepNumber === 4) {
    searchPaths.push(path.join(projectRoot, 'dam_output'));
  } else if (stepNumber === 5) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '01_inventory'));
  } else if (stepNumber === 6) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '02_price_semantics'));
  } else if (stepNumber === 7) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '03_quality_audit'));
  } else if (stepNumber === 8) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '04_geography'));
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '05_temporal'));
  } else if (stepNumber === 9) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '06_cleaning_rules'));
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '07_outputs'));
  } else if (stepNumber === 10) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '08_panel_readiness'));
  } else if (stepNumber === 11) {
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '09_research_readiness'));
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '10_code'));
    searchPaths.push(path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', '11_manifest'));
    const auditGuide = path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', 'STEPS_4_TO_11_AI_AUDIT_GUIDE.md');
    if (fs.existsSync(auditGuide)) searchPaths.push(auditGuide);
    const reportPath = path.join(projectRoot, 'DAM_ANALYSIS_READY_2026', 'FINAL_DATA_READINESS_REPORT.md');
    if (fs.existsSync(reportPath)) searchPaths.push(reportPath);
  }

  function walkDir(currentPath: string) {
    if (!fs.existsSync(currentPath)) return;
    const stat = fs.statSync(currentPath);
    if (!stat.isDirectory()) {
      const rel = path.relative(projectRoot, currentPath).replace(/\\/g, '/');
      const ext = getFileType(currentPath);
      const id = Buffer.from(rel).toString('base64url');
      artifacts.set(rel.toLowerCase(), {
        id,
        stepNumber,
        relativePath: rel,
        fileName: path.basename(currentPath),
        fileType: ext,
        displayName: path.basename(currentPath),
        sizeBytes: stat.size,
        isDirectory: false,
      });
      return;
    }

    const entries = fs.readdirSync(currentPath);
    for (const entry of entries) {
      // Skip cache or massive raw json dumps unless directly requested
      if (entry === '__pycache__' || entry === '.git' || entry === 'node_modules' || entry === '.next') continue;
      const full = path.join(currentPath, entry);
      const itemStat = fs.statSync(full);
      const rel = path.relative(projectRoot, full).replace(/\\/g, '/');
      const id = Buffer.from(rel).toString('base64url');

      if (itemStat.isDirectory()) {
        walkDir(full);
      } else {
        artifacts.set(rel.toLowerCase(), {
          id,
          stepNumber,
          relativePath: rel,
          fileName: entry,
          fileType: getFileType(full),
          displayName: entry,
          sizeBytes: itemStat.size,
          isDirectory: false,
        });
      }
    }
  }

  for (const p of searchPaths) {
    walkDir(p);
  }

  return Array.from(artifacts.values()).sort((a, b) =>
    a.relativePath.localeCompare(b.relativePath, undefined, { numeric: true })
  );
}

/**
 * Build a nested file tree from flat list of artifacts.
 */
export function buildFileTree(artifacts: Artifact[]): FileTreeNode[] {
  const root: FileTreeNode[] = [];

  for (const art of artifacts) {
    const parts = art.relativePath.split('/');
    let currentLevel = root;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      const isFile = i === parts.length - 1;
      const subPath = parts.slice(0, i + 1).join('/');

      let existing = currentLevel.find((node) => node.name === part);
      if (!existing) {
        existing = {
          name: part,
          path: subPath,
          isDirectory: !isFile,
          sizeBytes: isFile ? art.sizeBytes : undefined,
          fileType: isFile ? art.fileType : undefined,
          children: isFile ? undefined : [],
        };
        currentLevel.push(existing);
      }

      if (!isFile && existing.children) {
        currentLevel = existing.children;
      }
    }
  }

  return root;
}

/**
 * Get all artifacts across all 17 steps with count summaries.
 */
export function getAllArtifacts(): { artifacts: Artifact[]; totalCount: number; totalSizeBytes: number } {
  let all: Artifact[] = [];
  for (let s = 1; s <= 17; s++) {
    const stepArts = scanStepArtifacts(s);
    all = all.concat(stepArts);
  }

  const totalSizeBytes = all.reduce((sum, a) => sum + a.sizeBytes, 0);
  return {
    artifacts: all,
    totalCount: all.length,
    totalSizeBytes,
  };
}

/**
 * Locate single artifact by ID or relative path.
 */
export function getArtifactById(artifactId: string): { artifact: Artifact; fullPath: string; sha256: string } | null {
  let relPath: string;
  try {
    relPath = Buffer.from(artifactId, 'base64url').toString('utf-8');
  } catch {
    return null;
  }

  const fullPath = resolveArtifactPath(relPath);
  if (!fullPath) return null;

  const stat = fs.statSync(fullPath);
  if (!stat.isFile()) return null;
  const sha256 = computeFileSha256(fullPath);

  return {
    artifact: {
      id: artifactId,
      stepNumber: 0, // determined by caller
      relativePath: relPath.replace(/\\/g, '/'),
      fileName: path.basename(fullPath),
      fileType: getFileType(fullPath),
      displayName: path.basename(fullPath),
      sizeBytes: stat.size,
      isDirectory: stat.isDirectory(),
    },
    fullPath,
    sha256,
  };
}
