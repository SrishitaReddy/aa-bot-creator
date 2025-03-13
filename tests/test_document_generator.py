#!/usr/bin/env python3
"""
Test suite for the document generator module.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add parent directory to path to import module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aa_bot_creator.document_generator import DocumentGenerator

class TestDocumentGenerator(unittest.TestCase):
    """Test cases for the DocumentGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Sample requirements for testing
        self.sample_requirements = {
            "project_info": {
                "name": "Test Project",
                "description": "A test project for unit testing",
                "version": "1.0.0"
            },
            "requirements": [
                {
                    "id": "REQ-001",
                    "type": "data_extraction",
                    "description": "Extract data from test source",
                    "details": "The bot should extract data from the test source",
                    "priority": "high",
                    "dependencies": []
                },
                {
                    "id": "REQ-002",
                    "type": "data_processing",
                    "description": "Process extracted data",
                    "details": "The bot should process the extracted data",
                    "priority": "medium",
                    "dependencies": ["REQ-001"]
                }
            ]
        }
        
        # Initialize document generator
        self.doc_gen = DocumentGenerator(self.sample_requirements, self.temp_dir)

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test initialization of DocumentGenerator."""
        self.assertEqual(self.doc_gen.requirements, self.sample_requirements)
        self.assertEqual(self.doc_gen.output_dir, self.temp_dir)
        self.assertIsNotNone(self.doc_gen.logger)

    @patch('docx.Document')
    def test_generate_solution_design_document(self, mock_document):
        """Test generation of solution design document."""
        # Mock Document class and its methods
        mock_doc_instance = MagicMock()
        mock_document.return_value = mock_doc_instance
        
        # Call the method
        result = self.doc_gen.generate_solution_design_document()
        
        # Verify the document was created and saved
        self.assertTrue(result)
        mock_doc_instance.save.assert_called_once()
        
        # Verify document sections were added
        self.assertGreaterEqual(mock_doc_instance.add_heading.call_count, 5)
        self.assertGreaterEqual(mock_doc_instance.add_paragraph.call_count, 5)

    @patch('docx.Document')
    def test_generate_user_story_document(self, mock_document):
        """Test generation of user story document."""
        # Mock Document class and its methods
        mock_doc_instance = MagicMock()
        mock_document.return_value = mock_doc_instance
        
        # Call the method
        result = self.doc_gen.generate_user_story_document()
        
        # Verify the document was created and saved
        self.assertTrue(result)
        mock_doc_instance.save.assert_called_once()
        
        # Verify document sections were added
        self.assertGreaterEqual(mock_doc_instance.add_heading.call_count, 3)
        self.assertGreaterEqual(mock_doc_instance.add_paragraph.call_count, 3)

    @patch('matplotlib.pyplot.savefig')
    @patch('networkx.draw_networkx')
    def test_generate_flow_diagram(self, mock_draw_networkx, mock_savefig):
        """Test generation of flow diagram."""
        # Call the method
        result = self.doc_gen.generate_flow_diagram()
        
        # Verify the diagram was created
        self.assertTrue(result)
        mock_draw_networkx.assert_called_once()
        mock_savefig.assert_called_once()

    def test_get_requirements_by_type(self):
        """Test filtering requirements by type."""
        data_extraction_reqs = self.doc_gen._get_requirements_by_type("data_extraction")
        self.assertEqual(len(data_extraction_reqs), 1)
        self.assertEqual(data_extraction_reqs[0]["id"], "REQ-001")
        
        data_processing_reqs = self.doc_gen._get_requirements_by_type("data_processing")
        self.assertEqual(len(data_processing_reqs), 1)
        self.assertEqual(data_processing_reqs[0]["id"], "REQ-002")

if __name__ == '__main__':
    unittest.main()