from keybert import KeyBERT
from sklearn.cluster import KMeans
from common.logger import logger
import numpy as np
import os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk
import re

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

class TopicsGenerator:
    """
    A class that handles clustering and topic/keyword extraction.
    """

    def __init__(self, embedder=None, random_state=42):
        """
        :param embedder: A SentenceTransformer or similar model for KeyBERT (optional).
        :param random_state: random seed for clustering.
        """
        self.embedder = embedder
        self.random_state = random_state
        self.num_tags = int(os.getenv('NUM_TAGS', '3'))  # Default to 3 tags if not specified
        logger.info(f"Initialized TopicsGenerator (num_tags={self.num_tags}, random_state={random_state})")
        if embedder:
            logger.info("Using custom embedder for KeyBERT")
        else:
            logger.info("Will use default KeyBERT embedder")

    def _normalize_tag(self, tag):
        """
        Normalize a tag by:
        1. Capitalizing first letter of each word
        2. Making it concise and hashtag-like
        3. Removing unnecessary words
        """
        # Remove any extra whitespace
        tag = ' '.join(tag.split())
        
        # Remove common unnecessary words
        unnecessary_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of']
        words = [word for word in tag.lower().split() if word not in unnecessary_words]
        
        # Capitalize first letter of each word
        tag = ' '.join(word.capitalize() for word in words)
        
        # Handle special cases for spiritual/religious terms
        if "gods" in tag.lower():
            tag = tag.replace("Gods", "God's")
        if "god" in tag.lower() and "god's" not in tag.lower():
            tag = tag.replace("God ", "God's ")
        
        return tag

    def _remove_redundant_tags(self, tags):
        """
        Remove redundant tags by:
        1. Removing exact duplicates
        2. Removing tags that are subsets of other tags
        3. Keeping meaningful, concise tags
        """
        unique_tags = []
        for tag in tags:
            normalized = tag.lower()
            
            # Skip if exact duplicate
            if any(normalized == t.lower() for t in unique_tags):
                continue
                
            # Skip if this tag is a subset of another tag
            if any(normalized in t.lower() and normalized != t.lower() for t in unique_tags):
                continue
                
            # Skip if another tag is a subset of this tag
            if any(t.lower() in normalized and normalized != t.lower() for t in unique_tags):
                continue
            
            # Skip very short tags (less than 3 characters)
            if len(normalized) < 3:
                continue
            
            # Skip common redundant patterns
            skip_patterns = [
                r'^(the|a|an)\s+',
                r'^\d+\s+',
                r'^(very|really|just)\s+',
                r'^(some|many|much)\s+'
            ]
            if any(re.match(pattern, normalized) for pattern in skip_patterns):
                continue
                
            unique_tags.append(tag)
            
        return unique_tags[:self.num_tags]  # Limit to desired number of tags

    def cluster_and_extract_topics(self, file_names, documents, embeddings):
        """
        Performs KMeans clustering on embeddings, then extracts keywords
        from each document and from each cluster's aggregated text.
        Returns a dict mapping filename -> list of combined tags.
        """
        if not documents or len(documents) == 0 or embeddings.size == 0:
            logger.warning("No documents or embeddings provided. Returning empty mapping.")
            return {}

        # Initialize KeyBERT with better parameters
        logger.info("Initializing KeyBERT model...")
        kw_model = KeyBERT(model=self.embedder) if self.embedder else KeyBERT()

        # Extract doc-level keywords with improved parameters
        logger.info("Extracting document-level keywords...")
        doc_keywords = {}
        for idx, text in enumerate(documents):
            if idx > 0 and idx % 10 == 0:
                logger.info(f"Processed {idx}/{len(documents)} documents")
            
            # Extract keywords with more meaningful phrases
            keywords = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 3),  # Allow phrases up to 3 words
                stop_words='english',
                use_maxsum=True,  # Use MaxSum for diversity
                nr_candidates=20,  # Consider more candidates
                top_n=self.num_tags * 2  # Extract more than needed for filtering
            )
            
            # Add common spiritual/religious terms if they appear in the text
            spiritual_terms = [
                "Purpose", "Faith", "Spiritual Growth", "Divine Plan",
                "God's Plan", "Life Purpose", "Personal Growth",
                "Transformation", "Inner Peace", "Worship"
            ]
            
            additional_tags = []
            for term in spiritual_terms:
                if term.lower() in text.lower():
                    additional_tags.append((term, 0.8))  # Add with high confidence
            
            # Combine extracted keywords with spiritual terms
            all_keywords = keywords + additional_tags
            
            # Normalize and clean the keywords
            tags = [self._normalize_tag(kw) for kw, _ in all_keywords]
            tags = self._remove_redundant_tags(tags)
            doc_keywords[file_names[idx]] = tags

        logger.info(f"Topic extraction complete. Generated tags for {len(doc_keywords)} documents")
        return doc_keywords
