-- ==========================================
-- STEP 1: Ingest and Automate (Setup)
-- ==========================================

-- 1. Create a remote model pointing to Vertex AI Multimodal Embeddings (US Multi-region)
-- Replace 'your-project-id.us.your-connection-id' with your actual Cloud Resource connection.
CREATE OR REPLACE MODEL `your_dataset_id.multimodal_model`
REMOTE WITH CONNECTION `your-project-id.us.your-connection-id`
OPTIONS (ENDPOINT = 'gemini-embedding-2-preview');

-- 2. Create the External GCS Object Table
-- This table points directly to GCS and autonomously indexes files as they are uploaded or deleted.
-- Replace 'your-bucket-name' with your actual Cloud Storage bucket name.
CREATE OR REPLACE EXTERNAL TABLE `your_dataset_id.assets_metadata`
WITH CONNECTION `your-project-id.us.your-connection-id`
OPTIONS (
  object_metadata = 'SIMPLE',
  uris = ['gs://your-bucket-name/media_archive/speeches/*']
);

-- 3. Create the Speeches Assets Table with Autonomous Embedding Enabled
-- Using the native 'AI.EMBED' function inside a 'GENERATED ALWAYS AS' clause.
-- Storing options 'asynchronous = TRUE' tells BigQuery to generate embeddings in the background autonomously.
CREATE OR REPLACE TABLE `your_dataset_id.assets` (
  asset_id STRING,
  uri STRING,
  asset_embedding STRUCT<result ARRAY<FLOAT64>, status STRING>
    GENERATED ALWAYS AS (
      AI.EMBED(
        uri,
        connection_id => 'your-project-id.us.your-connection-id',
        endpoint => 'gemini-embedding-2-preview'
      )
    ) STORED OPTIONS (asynchronous = TRUE)
);

-- 4. Autonomously Ingest Assets from GCS Object Table (Synchronization)
-- We synchronize all speech video files from our external GCS Object Table into our base standard table.
INSERT INTO `your_dataset_id.assets` (asset_id, uri)
SELECT
  REGEXP_EXTRACT(uri, r'([^/]+)\.[^.]+$') AS asset_id, -- Extract file name
  uri
FROM
  `your_dataset_id.assets_metadata`
WHERE
  uri NOT IN (SELECT uri FROM `your_dataset_id.assets`);

-- 5. Query to monitor autonomous embedding generation progress
SELECT
  COUNT(*) AS total_num_rows,
  COUNTIF(asset_embedding IS NOT NULL AND asset_embedding.status = '') AS total_num_generated_embeddings,
  COUNTIF(asset_embedding IS NOT NULL AND asset_embedding.status != '') AS total_num_failed_embeddings
FROM
  `your_dataset_id.assets`;

-- 6. Sandbox materialization step (Required for VECTOR_SEARCH when rows < 5000)
-- Flattens the structural generated column into a flat table for quick similarity queries.
-- Note: For production scale (>5000 rows), you would instead create a VECTOR INDEX directly on 'asset_embedding'.
CREATE OR REPLACE TABLE `your_dataset_id.assets_searchable` AS
SELECT
  asset_id,
  uri,
  asset_embedding.result AS embedding
FROM
  `your_dataset_id.assets`;
