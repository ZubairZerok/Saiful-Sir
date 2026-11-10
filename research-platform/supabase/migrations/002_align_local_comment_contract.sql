-- Align existing Supabase installations with Auditinsyt's local-first
-- SHA-256/stable-ID comment contract introduced in migration 001.

ALTER TABLE comments
  DROP CONSTRAINT IF EXISTS comments_artifact_version_id_fkey,
  DROP CONSTRAINT IF EXISTS comments_author_id_fkey,
  DROP CONSTRAINT IF EXISTS comments_resolved_by_fkey;

ALTER TABLE comments
  ALTER COLUMN artifact_version_id TYPE TEXT USING artifact_version_id::text,
  ALTER COLUMN author_id TYPE TEXT USING author_id::text,
  ALTER COLUMN resolved_by TYPE TEXT USING resolved_by::text,
  ALTER COLUMN artifact_relative_path DROP NOT NULL;
