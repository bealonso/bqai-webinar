-- ==========================================
-- STEP 3: Precision Retrieval with Hybrid Search
-- ==========================================

-- This unified search matches standard full-text indexing keyword terms 
-- with vector embedding retrieval to perform exact and semantic checks at the same time.
-- Replace 'your-bucket-name' with your actual Cloud Storage bucket name containing the hybrid query image.

WITH reference_image_embedding AS (
  SELECT ml_generate_embedding_result AS vector
  FROM ML.GENERATE_EMBEDDING(
    MODEL `your_dataset_id.multimodal_model`,
    (SELECT 'gs://your-bucket-name/media_archive/hybrid/capitol-dc.png' AS content)
  )
)
SELECT base.asset_id, distance
FROM VECTOR_SEARCH(
  TABLE `your_dataset_id.assets_searchable`,
  'embedding',
  (SELECT vector FROM reference_image_embedding),
  top_k => 10
)
WHERE SEARCH(base, 'inaugural'); -- Filters results using full-text search keyword term
