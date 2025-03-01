# Project ORBIT

Hey, this is O.R.B.I.T. (Obsidian Research & Behavioral Intelligence Toolkit). Now you may forget the fancy name cos this is just a bunch of AI tools I coded while bored trying to bring some cool AI funcitonalities to Obsidian. 

TL;DR:
If it breaks, use Cursor or sth to fix it yourself cos I will most likely not do any maintainance to this as long as it works on my machine.



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

4. Set up your environment variables:
   - Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` with your specific configuration:
   ```env
   VAULT_DIR="/path/to/your/obsidian/vault"  # Path to your Obsidian vault
   MODEL_NAME="all-MiniLM-L6-v2"            # The embedding model to use
   OUTPUT_FILE="outputs/tags_mapping.json"   # Where to save the generated tags
   ```

## Usage

### Tag Generator

1. Make sure your `.env` file is properly configured with your vault directory and preferences.

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

## Warnings

If your vault is on iCloud (as mine so I save the couple bucks of obsidian sync lmao), then you want to make sure all the files are donwloaded and are selected as "Keep downloaded". You can do this easily within finder. I implemented a safety mechanism that tries to force donwload the files but of course this will make the program run much slower or might not even work or require extra permission.


## Contributing

Contributions are welcome! Even though I might ghost you for a while

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Open a pull request

Please ensure your code follows the existing style and includes appropriate documentation.

## Future Plans

- [ ] Add more AI-powered tools for Obsidian
- [ ] Improve tag generation accuracy
- [ ] Add a sick ahh logo
- [ ] Add customization options for tag generation
- [ ] Create additional utilities for Obsidian vault management
- [ ] Much deeper integration with obsidian itself
- [ ] Plug in (?) idk
- [ ] Making changes on the actual files so tags are added to them and they can be automatically linked in Obsidian
- [ ] Connection with LLMs (Grok, DeepSeek, Claude, etc)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is not officially associated with Obsidian. Use these tools at your own risk, and always back up your vault before using any third-party tools.

## Acknowledgments

- [Obsidian](https://obsidian.md/) for creating an amazing knowledge management tool
- [sentence-transformers](https://www.sbert.net/) for providing excellent embedding models
- You. Fr, how cool that you here. Enjoy