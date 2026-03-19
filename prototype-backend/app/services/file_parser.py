"""
File parsers for different network formats.
Supports SIF, JSON, and CSV/TSV formats.
"""

import networkx as nx
import json
import csv
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class FileParser:
    """Parse biological network files in various formats."""
    
    SUPPORTED_FORMATS = {'sif', 'json', 'csv', 'tsv'}
    
    @staticmethod
    def parse(file_path: str, format: str = None) -> Tuple[nx.Graph, dict]:
        """
        Parse network file and return NetworkX graph.
        
        Args:
            file_path: Path to network file
            format: File format ('sif', 'json', 'csv', 'tsv'). Auto-detect if None.
            
        Returns:
            Tuple of (NetworkX Graph, metadata dict)
            
        Raises:
            ValueError: If format not supported or file invalid
        """
        
        # Auto-detect format from file extension if not provided
        if format is None:
            ext = Path(file_path).suffix.lower().lstrip('.')
            format = 'tsv' if ext == 'txt' else ext
        
        if format not in FileParser.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}. "
                           f"Supported: {FileParser.SUPPORTED_FORMATS}")
        
        logger.info(f"Parsing network file: {file_path} (format: {format})")
        
        if format == 'sif':
            return FileParser._parse_sif(file_path)
        elif format == 'json':
            return FileParser._parse_json(file_path)
        elif format in ['csv', 'tsv']:
            return FileParser._parse_csv(file_path, delimiter='\t' if format == 'tsv' else ',')
        
    @staticmethod
    def _parse_sif(file_path: str) -> Tuple[nx.Graph, dict]:
        """
        Parse Simple Interaction Format (SIF).
        Format: NODE1 INTERACTION NODE2
        """
        G = nx.Graph()
        edges_added = 0
        
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) < 3:
                    logger.warning(f"Line {line_num}: Skipping malformed entry: {line}")
                    continue
                
                node1 = parts[0]
                interaction = parts[1]
                targets = parts[2:]
                
                for node2 in targets:
                    G.add_edge(node1, node2, interaction_type=interaction, weight=1.0)
                    edges_added += 1
        
        metadata = {
            'source_format': 'sif',
            'edges_parsed': edges_added,
            'nodes_count': G.number_of_nodes(),
            'edges_count': G.number_of_edges()
        }
        
        logger.info(f"Parsed SIF: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G, metadata
    
    @staticmethod
    def _parse_json(file_path: str) -> Tuple[nx.Graph, dict]:
        """
        Parse JSON format.
        Expected: {nodes: [{id, label, ...}], edges: [{source, target, weight, ...}]}
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        G = nx.Graph()
        
        # Add nodes
        nodes_data = data.get('nodes', [])
        for node in nodes_data:
            node_id = node.get('id') or node.get('name')
            if not node_id:
                logger.warning("Node without ID, skipping")
                continue
            G.add_node(node_id, label=node.get('label', node_id), **node)
        
        # Add edges
        edges_data = data.get('edges', [])
        for edge in edges_data:
            source = edge.get('source')
            target = edge.get('target')
            if not source or not target:
                logger.warning(f"Edge without source/target, skipping: {edge}")
                continue
            weight = float(edge.get('weight', 1.0))
            G.add_edge(source, target, weight=weight, **edge)
        
        metadata = {
            'source_format': 'json',
            'nodes_count': G.number_of_nodes(),
            'edges_count': G.number_of_edges()
        }
        
        logger.info(f"Parsed JSON: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G, metadata
    
    @staticmethod
    def _parse_csv(file_path: str, delimiter: str = ',') -> Tuple[nx.Graph, dict]:
        """
        Parse CSV/TSV format.
        Expected columns: source, target, [weight], [interaction_type]
        """
        G = nx.Graph()
        edges_added = 0
        
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=delimiter)
            
            # Read header
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError("Empty CSV file")
            
            # Normalize header (lowercase, strip whitespace)
            header = [h.strip().lower() for h in header]
            
            if 'source' not in header or 'target' not in header:
                raise ValueError("CSV must have 'source' and 'target' columns")
            
            source_idx = header.index('source')
            target_idx = header.index('target')
            weight_idx = header.index('weight') if 'weight' in header else None
            interaction_idx = header.index('interaction_type') if 'interaction_type' in header else None
            
            for line_num, row in enumerate(reader, 1):
                if len(row) < 2:
                    logger.warning(f"Line {line_num}: Skipping short row")
                    continue
                
                source = row[source_idx].strip()
                target = row[target_idx].strip()
                weight = 1.0
                interaction = None
                
                if weight_idx and weight_idx < len(row):
                    try:
                        weight = float(row[weight_idx])
                    except ValueError:
                        weight = 1.0
                
                if interaction_idx and interaction_idx < len(row):
                    interaction = row[interaction_idx].strip()
                
                G.add_edge(source, target, weight=weight, 
                          interaction_type=interaction)
                edges_added += 1
        
        metadata = {
            'source_format': 'csv',
            'edges_parsed': edges_added,
            'nodes_count': G.number_of_nodes(),
            'edges_count': G.number_of_edges()
        }
        
        logger.info(f"Parsed CSV: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G, metadata
