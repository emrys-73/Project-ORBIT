import os
from embeddings.embeddings import EmbeddingsGenerator
from topics.topics import TopicsGenerator
from common.utils import save_json
from common.logger import logger

def main():
    # Example user-configurable values
    vault_dir = "/Users/adrian/Library/Mobile Documents/iCloud~md~obsidian/Documents/2.0/Aboi-Core/40 Days of Transformation"
    model_name = "all-MiniLM-L6-v2"
    output_file = "outputs/tags_mapping.json"
    
    logger.info("=== Starting Tag Generation Process ===")
    logger.info(f"Configuration:")
    logger.info(f"- Vault directory: {vault_dir}")
    logger.info(f"- Model: {model_name}")
    logger.info(f"- Output file: {output_file}")
    
    # 1. Generate embeddings
    logger.info("\n=== Step 1: Generating Embeddings ===")
    embeddings_gen = EmbeddingsGenerator(model_name=model_name, vault_dir=vault_dir)
    file_names, documents, embeddings = embeddings_gen.generate_embeddings()

    if not file_names:
        logger.error("No data to process. Exiting.")
        return

    # 2. Cluster & Extract Topics
    logger.info("\n=== Step 2: Clustering and Topic Extraction ===")
    topics_gen = TopicsGenerator(embedder=embeddings_gen.model, top_n=10)
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
