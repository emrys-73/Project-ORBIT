import os
from dotenv import load_dotenv
from embeddings.embeddings import EmbeddingsGenerator
from topics.topics import TopicsGenerator
from common.utils import save_json
from common.logger import logger

def main():
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    vault_dir = os.getenv('VAULT_DIR')
    model_name = os.getenv('MODEL_NAME', 'all-mpnet-base-v2')  # Using a more powerful model by default
    output_file = os.getenv('OUTPUT_FILE')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    num_tags = os.getenv('NUM_TAGS', '3')  # Number of tags per document
    
    # Validate required environment variables
    if not all([vault_dir, output_file]):
        logger.error("Missing required environment variables. Please check your .env file.")
        return
    
    # Test directory access
    if debug:
        logger.debug("=== Testing Directory Access ===")
        logger.debug(f"Normalized vault directory path: {os.path.abspath(vault_dir)}")
        if os.path.exists(vault_dir):
            logger.debug("Directory exists")
            contents = os.listdir(vault_dir)
            logger.debug(f"Directory contents: {contents}")
            md_files = [f for f in contents if f.endswith('.md')]
            logger.debug(f"Markdown files in directory: {md_files}")
        else:
            logger.error(f"Directory does not exist: {vault_dir}")
            return
    
    logger.info("=== Starting Tag Generation Process ===")
    logger.info(f"Configuration:")
    logger.info(f"- Vault directory: {vault_dir}")
    logger.info(f"- Model: {model_name}")
    logger.info(f"- Output file: {output_file}")
    logger.info(f"- Number of tags per document: {num_tags}")
    
    # 1. Generate embeddings
    logger.info("\n=== Step 1: Generating Embeddings ===")
    embeddings_gen = EmbeddingsGenerator(model_name=model_name, vault_dir=vault_dir)
    file_names, documents, embeddings = embeddings_gen.generate_embeddings(debug=debug)

    if not file_names:
        logger.error("No data to process. Exiting.")
        return

    # 2. Extract Topics
    logger.info("\n=== Step 2: Topic Extraction ===")
    topics_gen = TopicsGenerator(embedder=embeddings_gen.model)
    tags_mapping = topics_gen.cluster_and_extract_topics(file_names, documents, embeddings)

    # 3. Print or Save Results
    logger.info("\n=== Step 3: Saving Results ===")
    logger.info("Sample of generated tags:")
    for fname, tags in list(tags_mapping.items())[:3]:  # Show first 3 files as sample
        logger.info(f"{fname}:")
        logger.info(f"  Tags: {', '.join(tags)}")

    # Save to JSON for later
    save_json(tags_mapping, output_file)
    logger.info(f"Successfully saved tags mapping to: {output_file}")
    logger.info("=== Process Complete ===")

if __name__ == "__main__":
    main()
