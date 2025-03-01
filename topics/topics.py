from keybert import KeyBERT
from sklearn.cluster import KMeans
from common.logger import logger

class TopicsGenerator:
    """
    A class that handles clustering and topic/keyword extraction.
    """

    def __init__(self, embedder=None, top_n=10, random_state=42):
        """
        :param embedder: A SentenceTransformer or similar model for KeyBERT (optional).
        :param top_n:    Maximum number of keywords per file or cluster.
        :param random_state: random seed for clustering.
        """
        self.embedder = embedder
        self.top_n = top_n
        self.random_state = random_state
        logger.info(f"Initialized TopicsGenerator (top_n={top_n}, random_state={random_state})")
        if embedder:
            logger.info("Using custom embedder for KeyBERT")
        else:
            logger.info("Will use default KeyBERT embedder")

    def cluster_and_extract_topics(self, file_names, documents, embeddings):
        """
        Performs KMeans clustering on embeddings, then extracts up to top_n keywords 
        from each document and from each cluster's aggregated text.
        Returns a dict mapping filename -> list of combined tags.
        """
        if not documents or not embeddings:
            logger.warning("No documents or embeddings provided. Returning empty mapping.")
            return {}

        # 1. KMeans Clustering
        num_clusters = max(2, int(len(documents) ** 0.5))
        logger.info(f"Starting KMeans clustering with {num_clusters} clusters...")
        
        kmeans = KMeans(n_clusters=num_clusters, random_state=self.random_state)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        # Log cluster distribution
        cluster_sizes = {}
        for label in cluster_labels:
            cluster_sizes[label] = cluster_sizes.get(label, 0) + 1
        logger.info("Cluster sizes: " + ", ".join(f"Cluster {k}: {v} docs" for k, v in cluster_sizes.items()))

        # 2. KeyBERT for Keyword Extraction
        logger.info("Initializing KeyBERT model...")
        if self.embedder:
            kw_model = KeyBERT(model=self.embedder)
            logger.info("Using custom embedder for keyword extraction")
        else:
            kw_model = KeyBERT()
            logger.info("Using default KeyBERT embedder")

        # Extract doc-level keywords
        logger.info("Extracting document-level keywords...")
        doc_keywords = {}
        for idx, text in enumerate(documents):
            if idx > 0 and idx % 10 == 0:
                logger.info(f"Processed {idx}/{len(documents)} documents")
            
            keywords = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=self.top_n
            )
            doc_keywords[file_names[idx]] = [kw for kw, score in keywords]

        # Extract cluster-level keywords
        logger.info("Grouping documents by cluster...")
        cluster_to_indices = {}
        for idx, label in enumerate(cluster_labels):
            cluster_to_indices.setdefault(label, []).append(idx)

        logger.info("Extracting cluster-level keywords...")
        cluster_keywords = {}
        for cluster_id, indices in cluster_to_indices.items():
            logger.info(f"Processing cluster {cluster_id} with {len(indices)} documents")
            aggregated_text = " ".join(documents[i] for i in indices)
            keywords = kw_model.extract_keywords(
                aggregated_text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=self.top_n
            )
            cluster_keywords[cluster_id] = [kw for kw, score in keywords]
            logger.info(f"Cluster {cluster_id} keywords: {', '.join(cluster_keywords[cluster_id])}")

        # Combine doc-level and cluster-level keywords
        logger.info("Combining document and cluster keywords...")
        final_tags = {}
        for idx, filename in enumerate(file_names):
            c_id = cluster_labels[idx]
            combined = list(set(doc_keywords[filename] + cluster_keywords[c_id]))
            final_tags[filename] = combined

        logger.info(f"Topic extraction complete. Generated tags for {len(final_tags)} documents")
        return final_tags
