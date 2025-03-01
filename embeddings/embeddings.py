import numpy as np
from sentence_transformers import SentenceTransformer
from common.utils import read_markdown_files
from common.logger import logger
from tqdm import tqdm

class EmbeddingsGenerator:
    """
    A class responsible for generating embeddings from Obsidian notes.
    """

    def __init__(self, model_name: str, vault_dir: str):
        """
        :param model_name: Name of the Hugging Face or local SentenceTransformer model
        :param vault_dir:  Directory containing markdown files
        """
        self.model_name = model_name
        self.vault_dir = vault_dir
        self.model = None
        logger.info(f"Initialized EmbeddingsGenerator with model '{model_name}' for vault: {vault_dir}")

    def load_model(self):
        """
        Loads the SentenceTransformer model if not already loaded
        """
        if self.model is None:
            logger.info("Loading embedding model...")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")

    def generate_embeddings(self, debug=False):
        """
        Generates embeddings for all markdown files in the vault directory
        Returns:
        - file_names: list of file names
        - documents: list of document contents
        - embeddings: numpy array of embeddings
        """
        # Load model if needed
        self.load_model()

        # Read markdown files
        file_names, documents = read_markdown_files(self.vault_dir, debug)
        logger.info(f"Found {len(file_names)} markdown files")
        
        if not documents:
            return [], [], np.array([])

        if debug:
            logger.debug(f"Average document length: {sum(len(d) for d in documents) // len(documents)} characters")
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = []
        
        # Use tqdm for progress bar
        for doc in tqdm(documents, desc="Batches", unit="batch"):
            embedding = self.model.encode(doc)
            embeddings.append(embedding)
            
        embeddings = np.array(embeddings)
        
        if debug:
            logger.debug(f"Embeddings shape: {embeddings.shape}")
            logger.debug(f"First few files: {', '.join(file_names[:3])}")
        
        return file_names, documents, embeddings
