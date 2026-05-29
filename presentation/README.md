# Vector Search & Embeddings — Presentation Slide Deck Outline

This folder contains a premium, Google-branded interactive presentation deck covering **Vector Search**, **Embeddings**, **Retrieval Augmented Generation (RAG)**, and **Hybrid Search**.

* **Interactive Slide Deck:** Open the [index.html](index.html) in any browser to present!
  * 🖥️ **Full-Screen Support:** Toggle standard browser fullscreen mode.
  * 📝 **Speaker Notes Sidebar:** Dynamic speaker transcripts pulled directly from lesson recordings.
  * ⌨️ **Keyboard Navigation:** Use `Right Arrow` / `Space` to go forward and `Left Arrow` to go backward.

---

## 📁 Slide Deck Outline

### Session 00: Course Introduction
* **Slide 1: Course Cover Slide**
  * **Title:** Vector Search & Embeddings
  * **Subtitle:** Building the Next Generation of AI-Powered Semantic Search
* **Slide 2: Beyond Keywords: Modern Search**
  * **Content:** Multimodal capabilities, semantic context matching, RAG facts integration, and AI action agents (logistics, booking).
* **Slide 3: Course Roadmap**
  * **Content:** Two-part timeline (Core Technologies vs. Practical Cloud Deployments).

### Session 01: Vector Search Basics
* **Slide 4: Section Cover — Vector Search**
* **Slide 5: Semantic Value in Business**
  * **Content:** Customer experiences (vague visual cues, song descriptions) vs. Internal operations (knowledge management, semantic references).
* **Slide 6: Keyword vs. Semantic Search**
  * **Content:** Keyword matching pitfalls vs. Contextual dense embedding advantages.
* **Slide 7: High-Level Process Flow**
  * **Content:** Step 1: Encode $\rightarrow$ Step 2: Index $\rightarrow$ Step 3: Search.
* **Slide 8: Development vs. Serving Phases**
  * **Content:** Build-Time steps (generate vectors, compile index, deploy) vs. Run-Time steps (query encoding, nearest neighbors search, response).
* **Slide 9: The Book Index Analogy**
  * **Content:** Conceptual mapping of encoding, indexing, and searching to standard publishing indices.

### Session 02: Embeddings & Representation
* **Slide 10: Section Cover — Embeddings**
* **Slide 11: The Challenge of Representation**
  * **Content:** Quantitative capturing of text meanings and denser formatting requirements for ML models.
* **Slide 12: One-Hot Encoding**
  * **Content:** Basic word vectorization mechanics, extreme zero-filled sparsity issues, and contextual limitations.
* **Slide 13: Vector Space Arithmetic**
  * **Content:** The intuition of word mappings (`King - Man + Woman = Queen`) and analogous relative distances.
* **Slide 14: Dense vs. Sparse Embeddings**
  * **Content:** Dimensional comparisons and semantic understanding alignment.
* **Slide 15: Pre-trained Embedding APIs**
  * **Content:** Offloading massive training costs and using simple Google Cloud APIs (`text-embedding-004`).

### Session 03: Retrieval Augmented Generation (RAG)
* **Slide 16: Section Cover — RAG**
* **Slide 17: The Grounding Problem**
  * **Content:** LLM frozen knowledge constraints and the root causes of AI hallucinations.
* **Slide 18: Solutions to Hallucination**
  * **Content:** Tradeoffs of Fine-Tuning, Human Review, Prompt Engineering, and RAG.
* **Slide 19: The "Open-Book Exam" Analogy**
  * **Content:** Conceptual understanding of standalone LLMs vs. RAG-enabled databases.
* **Slide 20: RAG Technical Architecture**
  * **Content:** Technical steps from user prompts to vector search KNN lookups, contextual prompts compilation, and final grounded LLM generation.

### Session 04: Hybrid Search Optimization
* **Slide 21: Section Cover — Hybrid Search**
* **Slide 22: Why Hybrid is Crucial**
  * **Content:** Combining the semantic intuition of dense spaces with the exact string/SKU matching of sparse tokens.
* **Slide 23: Keyword Vector Mechanics**
  * **Content:** Tokenization, TF-IDF importance weighting, and sparse space indexing.
* **Slide 24: Reciprocal Rank Fusion (RRF)**
  * **Content:** Merging and prioritizing lists using rank reciprocals ($1 / \text{rank}$).
* **Slide 25: Vertex AI Hybrid Search Implementation**
  * **Content:** Single call execution combining dense and sparse parameters.
* **Slide 26: Interpreting Hybrid Results**
  * **Content:** Examples showing how RRF ranks items aligning on both parameters at the top, followed by conceptual semantic fits.
