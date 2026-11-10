import fs from 'node:fs';
import path from 'node:path';
import { load } from 'js-yaml';
import type { WorkflowStep, Paper, ProjectConfig } from '@/types';

const PROJECT_ROOT = path.resolve(/*turbopackIgnore: true*/ process.cwd());

/**
 * Load project.yaml from the platform root.
 */
export function loadProjectConfig(): ProjectConfig {
  const configPath = path.join(PROJECT_ROOT, 'project.yaml');
  const raw = fs.readFileSync(configPath, 'utf-8');
  const parsed = load(raw) as Record<string, unknown>;

  const proj = parsed.project as Record<string, string>;
  const papers = (parsed.papers as Record<string, string>[]).map((p) => ({
    id: p.id,
    title: p.title,
    subtitle: p.subtitle,
    status: p.status,
    primaryPriceVar: p.primary_price_var ?? '',
    targetSample: p.target_sample ?? '',
  }));

  const metrics = parsed.dataset_metrics as Record<string, unknown>;

  return {
    project: {
      name: proj.name,
      principalInvestigator: proj.principal_investigator,
      dataRoot: proj.data_root,
      analysisRoot: proj.analysis_root,
      rawOutputRoot: proj.raw_output_root,
    },
    papers,
    datasetMetrics: {
      totalObservations: metrics.total_observations as number,
      uniqueMarkets: metrics.unique_markets as number,
      commodityVarieties: metrics.commodity_varieties as number,
      temporalSpan: metrics.temporal_span as string,
      divisions: metrics.divisions as number,
      primaryAnalysisObs: metrics.primary_analysis_obs as number,
      strictSensitivityObs: metrics.strict_sensitivity_obs as number,
    },
  };
}

/**
 * Load step-registry.yaml and return typed WorkflowStep[].
 */
export function loadStepRegistry(): WorkflowStep[] {
  const registryPath = path.join(PROJECT_ROOT, 'step-registry.yaml');
  const raw = fs.readFileSync(registryPath, 'utf-8');
  const parsed = load(raw) as { steps: Record<string, unknown>[] };

  return parsed.steps.map((s) => ({
    number: s.number as number,
    id: s.id as string,
    name: s.name as string,
    description: s.description as string,
    status: (s.status as string) as WorkflowStep['status'],
    papers: (s.papers as string[]) ?? [],
    dependsOn: (s.depends_on as number[]) ?? [],
    artifactPatterns: (s.artifact_patterns as string[]) ?? [],
    artifactRoot: s.artifact_root as string | undefined,
  }));
}

/**
 * Load papers from project config.
 */
export function loadPapers(): Paper[] {
  return loadProjectConfig().papers;
}
