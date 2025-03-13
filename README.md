# AA Bot Creator

AA Bot Creator is an AI-powered tool that automates the process of creating Automation Anywhere A360 bots from Business Requirements Documents (BRDs). It analyzes BRDs, extracts requirements, generates documentation, and creates bot packages that can be deployed to Automation Anywhere Control Room.

## Features

- **BRD Analysis**: Extract requirements from Business Requirements Documents using AI
- **Documentation Generation**: Create Solution Design Documents, User Story Documents, and Flow Diagrams
- **Bot Generation**: Generate Automation Anywhere A360 bot packages based on requirements
- **Deployment**: Deploy bots directly to Automation Anywhere Control Room
- **Dependency Management**: Automatically detect and manage dependencies between bots

## Components

The AA Bot Creator consists of the following main components:

1. **BRD Analyzer**: Extracts requirements from Business Requirements Documents
2. **Document Generator**: Creates documentation based on the extracted requirements
3. **Bot Builder**: Generates Automation Anywhere bot packages based on requirements

## Installation

### Prerequisites

- Python 3.6+
- Automation Anywhere A360 Control Room (for deployment)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SrishitaReddy/aa-bot-creator.git
   cd aa-bot-creator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
   ```bash
   # Edit the configuration file
   nano config.json
   ```

## Usage

### Basic Usage

```bash
python main.py --input path/to/brd.pdf --output-dir output
```

This will:
1. Analyze the BRD and extract requirements
2. Generate documentation (SDD, USD, Flow Diagram)
3. Generate bot packages

### Command-Line Options

```
usage: main.py [-h] --input INPUT [--output-dir OUTPUT_DIR] [--config CONFIG]
               [--skip-analysis] [--skip-docs] [--skip-bots] [--deploy]
               [--control-room CONTROL_ROOM] [--api-key API_KEY]

AA Bot Creator - Generate Automation Anywhere bots from BRDs

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input BRD file or directory
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory for generated files
  --config CONFIG, -c CONFIG
                        Configuration file
  --skip-analysis       Skip BRD analysis (use existing requirements)
  --skip-docs           Skip document generation
  --skip-bots           Skip bot generation
  --deploy, -d          Deploy bots to Control Room
  --control-room CONTROL_ROOM
                        Control Room URL
  --api-key API_KEY     API key for Control Room
```

### Examples

#### Generate Only Documentation

```bash
python main.py --input path/to/brd.pdf --output-dir output --skip-bots
```

#### Use Existing Requirements

```bash
python main.py --input path/to/brd.pdf --output-dir output --skip-analysis
```

#### Deploy Bots to Control Room

```bash
python main.py --input path/to/brd.pdf --output-dir output --deploy --control-room https://your-control-room.com --api-key YOUR_API_KEY
```

## Configuration

The `config.json` file contains configuration options for all components of the AA Bot Creator:

```json
{
  "brd_analyzer": {
    "extraction_method": "ai",
    "ai_model": "gpt-4",
    "min_confidence_score": 0.7
  },
  "document_generator": {
    "template_dir": "templates",
    "company_name": "Your Company"
  },
  "bot_builder": {
    "default_folder": "My Bots",
    "include_error_handling": true
  },
  "control_room": {
    "url": "https://your-control-room.example.com",
    "api_key": ""
  }
}
```

## Module-Specific Usage

Each module can also be used independently:

### BRD Analyzer

```python
from brd_analyzer.brd_analyzer import BRDAnalyzer

analyzer = BRDAnalyzer(input_path="path/to/brd.pdf", output_dir="output/requirements")
requirements = analyzer.analyze()
```

### Document Generator

```python
from brd_analyzer.document_generator import DocumentGenerator

doc_generator = DocumentGenerator(requirements=requirements, output_dir="output/docs")
sdd_path = doc_generator.generate_solution_design_document()
usd_path = doc_generator.generate_user_story_document()
flow_diagram_path = doc_generator.generate_flow_diagram()
```

### Bot Builder

```python
from bot_builder.bot_builder import BotBuilder
from bot_builder.utils import enrich_requirements

enriched_requirements = enrich_requirements(requirements)
bot_builder = BotBuilder(requirements=enriched_requirements, output_dir="output/bots")
bot_packages = bot_builder.generate_all_bots()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Automation Anywhere for their RPA platform
- OpenAI for their language models used in the BRD analysis