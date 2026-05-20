-- ==========================================
-- STEP 2: Cross-Modal Discovery
-- ==========================================

-- ----------------------------------------------------
-- Scene A: Text-to-Video Search
-- ----------------------------------------------------
-- Search for a video matching a natural language text query using standard VECTOR_SEARCH.
-- Queries the searchable table mapped to our autonomous embedding base.

WITH text_query AS (
  SELECT ml_generate_embedding_result AS vector
  FROM ML.GENERATE_EMBEDDING(
    MODEL `your_dataset_id.multimodal_model`,
    (SELECT 'historical political speech given at night in a stadium' AS content)
  )
)
SELECT base.asset_id, distance
FROM VECTOR_SEARCH(
  TABLE `your_dataset_id.assets_searchable`,
  'embedding',
  (SELECT vector FROM text_query),
  top_k => 5,
  distance_type => 'COSINE'
);


-- ----------------------------------------------------
-- Scene B: Audio-to-Video Search
-- ----------------------------------------------------
-- Match a query audio clip snippet against matching video footage using VECTOR_SEARCH.
-- Replace 'your-bucket-name' with your actual Cloud Storage bucket name containing the queries.

WITH audio_query AS (
  SELECT ml_generate_embedding_result AS vector
  FROM ML.GENERATE_EMBEDDING(
    MODEL `your_dataset_id.multimodal_model`,
    (SELECT 'gs://your-bucket-name/media_archive/queries/1-MLK-Dream_clipped.mp3' AS content)
  )
)
SELECT base.asset_id, distance
FROM VECTOR_SEARCH(
  TABLE `your_dataset_id.assets_searchable`,
  'embedding',
  (SELECT vector FROM audio_query),
  top_k => 5,
  distance_type => 'COSINE'
);
