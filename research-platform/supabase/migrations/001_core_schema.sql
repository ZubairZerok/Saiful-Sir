-- ============================================================
-- AUDITINSYT RESEARCH WORKFLOW REVIEW & AUDIT PLATFORM
-- Supabase PostgreSQL Schema Migration 001
-- ============================================================

-- USER ROLES ENUM
DO $$ BEGIN
  CREATE TYPE user_role AS ENUM ('researcher', 'teacher');
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- STEP STATUS ENUM
DO $$ BEGIN
  CREATE TYPE step_status AS ENUM (
    'not_started',
    'in_progress',
    'review_requested',
    'changes_requested',
    'approved',
    'locked'
  );
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- DECISION ENUM
DO $$ BEGIN
  CREATE TYPE step_decision_type AS ENUM (
    'approved',
    'changes_requested',
    'locked'
  );
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- PROJECTS (Metadata only, filesystem is source of truth)
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  principal_investigator TEXT NOT NULL,
  data_root TEXT NOT NULL,
  analysis_root TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- WORKFLOW STEPS (17 Steps)
CREATE TABLE IF NOT EXISTS workflow_steps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  step_number INTEGER NOT NULL CHECK (step_number BETWEEN 1 AND 17),
  step_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  status step_status NOT NULL DEFAULT 'not_started',
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  approved_at TIMESTAMPTZ,
  approved_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (project_id, step_number)
);

-- ARTIFACTS (Logical file references - NO raw data duplication)
CREATE TABLE IF NOT EXISTS artifacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  step_number INTEGER NOT NULL,
  relative_path TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_type TEXT NOT NULL,
  display_name TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (project_id, relative_path)
);

-- ARTIFACT VERSIONS (Cryptographic hash snapshots)
CREATE TABLE IF NOT EXISTS artifact_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  artifact_id UUID REFERENCES artifacts(id) ON DELETE CASCADE,
  sha256_hash TEXT NOT NULL,
  file_size_bytes BIGINT NOT NULL,
  row_count INTEGER,
  column_count INTEGER,
  is_current BOOLEAN DEFAULT true,
  indexed_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (artifact_id, sha256_hash)
);

-- STEP DECISIONS (Formal teacher reviews with rationale)
CREATE TABLE IF NOT EXISTS step_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  step_number INTEGER NOT NULL,
  decision step_decision_type NOT NULL,
  rationale TEXT NOT NULL,
  decided_by UUID REFERENCES auth.users(id),
  decided_by_name TEXT NOT NULL,
  decided_at TIMESTAMPTZ DEFAULT now()
);

-- COMMENTS (Version-anchored hybrid feedback)
CREATE TABLE IF NOT EXISTS comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- The local-first application uses a SHA-256 digest or stable artifact ID.
  -- Keep this textual so Supabase and .audit_data.json share one contract.
  artifact_version_id TEXT NOT NULL,
  artifact_relative_path TEXT,
  step_number INTEGER,
  author_id TEXT NOT NULL,
  author_name TEXT NOT NULL,
  author_role user_role NOT NULL DEFAULT 'teacher',
  anchor_type TEXT NOT NULL, -- 'markdown_block' | 'csv_cell' | 'csv_row' | 'figure_region' | 'code_line' | 'general'
  anchor_data JSONB NOT NULL DEFAULT '{}'::jsonb,
  body TEXT NOT NULL,
  is_resolved BOOLEAN DEFAULT false,
  resolved_by TEXT,
  resolved_at TIMESTAMPTZ,
  parent_comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- INDEXES FOR FAST QUERYING
CREATE INDEX IF NOT EXISTS idx_workflow_steps_num ON workflow_steps(step_number);
CREATE INDEX IF NOT EXISTS idx_artifacts_step ON artifacts(step_number);
CREATE INDEX IF NOT EXISTS idx_artifact_versions_current ON artifact_versions(artifact_id, is_current);
CREATE INDEX IF NOT EXISTS idx_comments_version ON comments(artifact_version_id);
CREATE INDEX IF NOT EXISTS idx_comments_path ON comments(artifact_relative_path);
CREATE INDEX IF NOT EXISTS idx_comments_step ON comments(step_number);

-- ENABLE ROW LEVEL SECURITY
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflow_steps ENABLE ROW LEVEL SECURITY;
ALTER TABLE artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE artifact_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE step_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- POLICIES: Open read for research workspace
CREATE POLICY "Public Read Projects" ON projects FOR SELECT USING (true);
CREATE POLICY "Public Read Workflow Steps" ON workflow_steps FOR SELECT USING (true);
CREATE POLICY "Public Read Artifacts" ON artifacts FOR SELECT USING (true);
CREATE POLICY "Public Read Artifact Versions" ON artifact_versions FOR SELECT USING (true);
CREATE POLICY "Public Read Step Decisions" ON step_decisions FOR SELECT USING (true);
CREATE POLICY "Public Read Comments" ON comments FOR SELECT USING (true);

-- POLICIES: Insert/Update Comments for authenticated / role-aware users
CREATE POLICY "Auth Insert Comments" ON comments FOR INSERT WITH CHECK (true);
CREATE POLICY "Auth Update Comments" ON comments FOR UPDATE USING (true);
CREATE POLICY "Auth Insert Step Decisions" ON step_decisions FOR INSERT WITH CHECK (true);
CREATE POLICY "Auth Update Workflow Steps" ON workflow_steps FOR ALL USING (true);
