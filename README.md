# AA Bot Creator

AA Bot Creator is a comprehensive tool for automating the creation of Automation Anywhere bots from Business Requirements Documents (BRDs). It streamlines the process of analyzing requirements, generating documentation, and building bots.

## Features

- **BRD Analysis**: Extract and classify requirements from Business Requirements Documents
- **Documentation Generation**: Create Solution Design Documents and User Story Documents
- **Bot Building**: Generate Automation Anywhere bot structures based on requirements
- **Deployment**: Deploy bots directly to Automation Anywhere Control Room

## Installation

```bash
# Clone the repository
git clone https://github.com/SrishitaReddy/aa-bot-creator.git
cd aa-bot-creator

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit the `config.json` file to customize the behavior of the tool:

```json
{
  "brd_analyzer": {
    "extraction_method": "rule_based",
    "requirement_types": ["data_extraction", "data_processing", "system_integration", "process_automation"]
  },
  "document_generator": {
    "template_folder": "templates",
    "company_info": {
      "name": "Your Company",
      "logo_path": "path/to/logo.png"
    }
  },
  "bot_builder": {
    "default_folder": "bots",
    "error_handling": true,
    "logging": true
  },
  "control_room": {
    "url": "https://your-control-room-url.com",
    "api_key": "your-api-key"
  }
}
```

## Usage

### Command Line Interface

```bash
# Analyze a BRD and extract requirements
python -m aa_bot_creator analyze --input path/to/brd.pdf --output requirements.json

# Generate documentation from requirements
python -m aa_bot_creator document --input requirements.json --output docs/ --type sdd

# Build bots from requirements
python -m aa_bot_creator build --input requirements.json --output bots/

# Full pipeline: analyze, document, and build
python -m aa_bot_creator run --input path/to/brd.pdf --output project/
```

### Python API

```python
from aa_bot_creator.brd_analyzer import BRDAnalyzer
from aa_bot_creator.document_generator import DocumentGenerator
from aa_bot_creator.bot_builder import BotBuilder

# Analyze BRD
analyzer = BRDAnalyzer("path/to/brd.pdf")
requirements = analyzer.extract_requirements()

# Generate documentation
doc_gen = DocumentGenerator(requirements, "docs/")
doc_gen.generate_solution_design_document()
doc_gen.generate_user_story_document()

# Build bots
bot_builder = BotBuilder(requirements, "bots/")
bot_builder.generate_bots()
bot_builder.deploy_to_control_room()
```

## Module Structure

- **brd_analyzer**: Extracts and classifies requirements from BRDs
- **document_generator**: Creates documentation based on requirements
- **bot_builder**: Generates Automation Anywhere bot structures
- **utils**: Common utility functions
- **cli**: Command-line interface

## Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=aa_bot_creator
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Automation Anywhere for their RPA platform
- All contributors who have helped shape this project