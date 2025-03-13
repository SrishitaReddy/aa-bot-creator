#!/usr/bin/env python3
"""
AA Bot Creator - Main Entry Point

This script serves as the main entry point for the AA Bot Creator application,
which analyzes Business Requirements Documents (BRDs) and generates
Automation Anywhere bots based on the extracted requirements.
"""

import os
import sys
import argparse
import logging
import json
from typing import List, Dict, Any, Optional

# Import modules
from brd_analyzer.brd_analyzer import BRDAnalyzer
from brd_analyzer.document_generator import DocumentGenerator
from bot_builder.bot_builder import BotBuilder
from bot_builder.utils import enrich_requirements, update_requirements_with_dependencies

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='AA Bot Creator - Generate Automation Anywhere bots from BRDs')
    
    # Main arguments
    parser.add_argument('--input', '-i', required=True, help='Input BRD file or directory')
    parser.add_argument('--output-dir', '-o', default='output', help='Output directory for generated files')
    parser.add_argument('--config', '-c', default='config.json', help='Configuration file')
    
    # Processing options
    parser.add_argument('--skip-analysis', action='store_true', help='Skip BRD analysis (use existing requirements)')
    parser.add_argument('--skip-docs', action='store_true', help='Skip document generation')
    parser.add_argument('--skip-bots', action='store_true', help='Skip bot generation')
    parser.add_argument('--deploy', '-d', action='store_true', help='Deploy bots to Control Room')
    
    # Control Room options
    parser.add_argument('--control-room', help='Control Room URL')
    parser.add_argument('--api-key', help='API key for Control Room')
    
    return parser.parse_args()

def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Configuration file {config_file} not found. Using defaults.")
            return {}
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return {}

def main():
    """Main entry point for the AA Bot Creator."""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set up paths
    requirements_dir = os.path.join(args.output_dir, 'requirements')
    docs_dir = os.path.join(args.output_dir, 'docs')
    bots_dir = os.path.join(args.output_dir, 'bots')
    
    os.makedirs(requirements_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(bots_dir, exist_ok=True)
    
    requirements_file = os.path.join(requirements_dir, 'requirements.json')
    
    # Step 1: Analyze BRD and extract requirements
    requirements = []
    
    if not args.skip_analysis:
        logger.info(f"Analyzing BRD: {args.input}")
        
        analyzer = BRDAnalyzer(
            input_path=args.input,
            output_dir=requirements_dir,
            config=config.get('brd_analyzer', {})
        )
        
        requirements = analyzer.analyze()
        
        # Save requirements to file
        with open(requirements_file, 'w') as f:
            json.dump({"requirements": requirements}, f, indent=2)
            
        logger.info(f"Extracted {len(requirements)} requirements from BRD")
    else:
        # Load existing requirements
        try:
            with open(requirements_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'requirements' in data:
                    requirements = data['requirements']
                elif isinstance(data, list):
                    requirements = data
                    
            logger.info(f"Loaded {len(requirements)} existing requirements")
        except Exception as e:
            logger.error(f"Error loading existing requirements: {str(e)}")
            return 1
    
    # Enrich requirements with additional information
    requirements = enrich_requirements(requirements)
    requirements = update_requirements_with_dependencies(requirements)
    
    # Step 2: Generate documentation
    if not args.skip_docs:
        logger.info("Generating documentation")
        
        doc_generator = DocumentGenerator(
            requirements=requirements,
            output_dir=docs_dir
        )
        
        # Generate Solution Design Document
        sdd_path = doc_generator.generate_solution_design_document()
        logger.info(f"Generated Solution Design Document: {sdd_path}")
        
        # Generate User Story Document
        usd_path = doc_generator.generate_user_story_document()
        logger.info(f"Generated User Story Document: {usd_path}")
        
        # Generate Flow Diagram
        flow_diagram_path = doc_generator.generate_flow_diagram()
        logger.info(f"Generated Flow Diagram: {flow_diagram_path}")
    
    # Step 3: Generate bots
    if not args.skip_bots:
        logger.info("Generating bots")
        
        # Get Control Room credentials
        control_room_url = args.control_room or config.get('control_room', {}).get('url')
        api_key = args.api_key or config.get('control_room', {}).get('api_key')
        
        bot_builder = BotBuilder(
            requirements=requirements,
            control_room_url=control_room_url if args.deploy else None,
            api_key=api_key if args.deploy else None,
            output_dir=bots_dir
        )
        
        bot_packages = bot_builder.generate_all_bots()
        logger.info(f"Generated {len(bot_packages)} bot packages")
        
        # Deploy bots if requested
        if args.deploy:
            if control_room_url and api_key:
                logger.info(f"Deploying bots to Control Room: {control_room_url}")
                results = bot_builder.deploy_bots_to_control_room(bot_packages)
                report = bot_builder.generate_deployment_report(results)
                
                logger.info(f"Deployment complete. Success rate: {report['success_rate'] * 100:.2f}%")
            else:
                logger.error("Control Room URL and API key are required for deployment")
                return 1
    
    logger.info("AA Bot Creator process completed successfully")
    return 0

if __name__ == '__main__':
    sys.exit(main())