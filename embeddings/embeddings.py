from sentence_transformers import SentenceTransformer
from common.utils import read_markdown_files
from common.logger import logger

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
        Loads the SentenceTransformer model.
        """
        logger.info(f"Starting to load embedding model: {self.model_name}")
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {str(e)}")
            raise

    def generate_embeddings(self):
        """
        Reads markdown files, encodes them with the model, and returns:
          - file_names: list of filenames
          - documents:  list of text contents
          - embeddings: list of embedding vectors
        """
        if self.model is None:
            logger.info("No model loaded yet, loading now...")
            self.load_model()

        logger.info(f"Reading markdown files from directory: {self.vault_dir}")
        file_names, documents = read_markdown_files(self.vault_dir)
        
        logger.info(f"Found {len(file_names)} markdown files")
        if len(documents) > 0:
            logger.info(f"Average document length: {sum(len(d) for d in documents) / len(documents):.0f} characters")

        if not documents:
            logger.warning("No markdown files found or they are empty")
            return [], [], []

        logger.info(f"Starting embedding generation for {len(documents)} documents...")
        try:
            embeddings = self.model.encode(documents, show_progress_bar=True)
            logger.info(f"Successfully created embeddings. Shape: {embeddings.shape}")
            logger.info(f"First few files processed: {', '.join(file_names[:3])}")
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

        return file_names, documents, embeddings
