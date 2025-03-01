# Obsidian AI Tools Collection

A collection of AI-powered tools designed to enhance your Obsidian vault experience. Currently in development, with more tools being added as they are created.

## Current Tools

### 1. Automatic Tag Generator
Automatically generates relevant tags for your Obsidian notes using advanced NLP and clustering techniques. This tool:
- Processes all markdown files in a specified vault directory
- Generates semantic embeddings using state-of-the-art language models
- Clusters similar content and extracts relevant topics
- Creates a mapping of files to appropriate tags

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/obsidian-ai-tools.git
cd obsidian-ai-tools
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Tag Generator

1. Open `main.py` and configure the following variables:
```python
vault_dir = "path/to/your/obsidian/vault"  # Path to your Obsidian vault or specific folder
model_name = "all-MiniLM-L6-v2"           # The embedding model to use
output_file = "outputs/tags_mapping.json"  # Where to save the generated tags
```

2. Run the script:
```bash
python main.py
```

The tool will:
- Process all markdown files in the specified directory
- Generate embeddings for each file
- Cluster similar content
- Extract relevant topics as tags
- Save the results in a JSON file

## Configuration

### Available Models
The tag generator uses the `sentence-transformers` library. By default, it uses the `all-MiniLM-L6-v2` model, which offers a good balance between performance and resource usage. You can use other models from the [sentence-transformers collection](https://www.sbert.net/docs/pretrained_models.html).

## Requirements
- Python 3.8+
- sentence-transformers
- Other dependencies listed in requirements.txt

## Support and Troubleshooting

This is a personal project shared with the community. While I aim to maintain and improve these tools, please note:

- There is no official support
- For troubleshooting, I recommend using [Cursor](https://cursor.sh/) or similar AI-powered development tools
- Feel free to open issues on GitHub, but response times may vary
- Pull requests are welcome!

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Open a pull request

Please ensure your code follows the existing style and includes appropriate documentation.

## Future Plans

- [ ] Add more AI-powered tools for Obsidian
- [ ] Improve tag generation accuracy
- [ ] Add customization options for tag generation
- [ ] Create additional utilities for Obsidian vault management

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is not officially associated with Obsidian. Use these tools at your own risk, and always back up your vault before using any third-party tools.

## Acknowledgments

- [Obsidian](https://obsidian.md/) for creating an amazing knowledge management tool
- [sentence-transformers](https://www.sbert.net/) for providing excellent embedding models
- The open-source community for inspiration and support 