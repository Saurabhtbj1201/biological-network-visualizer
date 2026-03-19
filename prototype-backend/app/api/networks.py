"""
Network API routes - handle file upload, retrieval, and basic network operations.
"""

from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Network, Node, Edge
from app.services.file_parser import FileParser
from app.services.metrics_calculator import MetricsCalculator
from app.services.community_detector import CommunityDetector
import uuid
import os
import logging

bp = Blueprint('networks', __name__, url_prefix='/api/networks')
logger = logging.getLogger(__name__)


@bp.route('/upload', methods=['POST'])
def upload_network():
    """
    Upload and parse a network file.
    
    Expected form data:
    - file: Network file (SIF, JSON, CSV/TSV)
    - name: Network name (optional, defaults to filename)
    - metadata: JSON metadata (optional)
    """
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'missing_file', 'message': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'empty_filename', 'message': 'File has no name'}), 400
        
        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
        if ext not in ['sif', 'json', 'csv', 'tsv', 'txt']:
            return jsonify({
                'error': 'invalid_format',
                'message': 'Supported formats: SIF, JSON, CSV, TSV'
            }), 400
        
        # Save uploaded file temporarily
        upload_dir = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_dir, exist_ok=True)
        temp_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_path = os.path.join(upload_dir, temp_filename)
        file.save(temp_path)
        
        # Parse network file
        graph, metadata = FileParser.parse(temp_path, format=ext)
        
        # Create network record
        network = Network(
            name=request.form.get('name', os.path.splitext(file.filename)[0]),
            format=ext,
            nodes_count=graph.number_of_nodes(),
            edges_count=graph.number_of_edges(),
            file_path=temp_path,
            metadata=request.form.get('metadata', {})
        )
        db.session.add(network)
        db.session.flush()  # Get the network ID without committing
        
        # Add nodes to database
        for node in graph.nodes():
            node_obj = Node(
                id=str(node),
                network_id=network.id,
                label=str(node),
                attributes=dict(graph.nodes[node])
            )
            db.session.add(node_obj)
        
        # Add edges to database
        for source, target in graph.edges():
            edge_data = graph[source][target]
            edge_id = f"{source}--{target}"
            edge_obj = Edge(
                id=edge_id,
                network_id=network.id,
                source=str(source),
                target=str(target),
                weight=edge_data.get('weight', 1.0),
                interaction_type=edge_data.get('interaction_type'),
                attributes={k: v for k, v in edge_data.items() 
                           if k not in ['weight', 'interaction_type']}
            )
            db.session.add(edge_obj)
        
        db.session.commit()
        logger.info(f"Uploaded network {network.id}: {network.name}")
        
        return jsonify({
            'network_id': str(network.id),
            'name': network.name,
            'nodes_count': network.nodes_count,
            'edges_count': network.edges_count,
            'status': 'parsed',
            'created_at': network.created_at.isoformat()
        }), 201
        
    except Exception as e:
        logger.error(f"Error uploading network: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'upload_failed',
            'message': str(e)
        }), 500


@bp.route('/<network_id>', methods=['GET'])
def get_network(network_id):
    """Get network metadata and statistics."""
    
    try:
        network = Network.query.get(network_id)
        if not network:
            return jsonify({'error': 'not_found', 'message': 'Network not found'}), 404
        
        return jsonify(network.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error fetching network: {str(e)}")
        return jsonify({'error': 'fetch_failed', 'message': str(e)}), 500


@bp.route('/<network_id>/nodes', methods=['GET'])
def get_nodes(network_id):
    """
    Get nodes with optional filtering and pagination.
    
    Query parameters:
    - limit: int (default 100)
    - offset: int (default 0)
    - min_degree: int (optional)
    - max_degree: int (optional)
    - community_id: int (optional)
    - sort_by: str (default 'label')
    """
    
    try:
        # Parse query parameters
        limit = min(int(request.args.get('limit', 100)), 1000)
        offset = int(request.args.get('offset', 0))
        min_degree = request.args.get('min_degree', type=float)
        max_degree = request.args.get('max_degree', type=float)
        community_id = request.args.get('community_id', type=int)
        sort_by = request.args.get('sort_by', 'id')
        
        # Build query
        query = Node.query.filter_by(network_id=network_id)
        
        # Apply filters
        if min_degree is not None:
            query = query.filter(Node.degree_centrality >= min_degree)
        if max_degree is not None:
            query = query.filter(Node.degree_centrality <= max_degree)
        if community_id is not None:
            query = query.filter_by(community_id=community_id)
        
        # Count total
        total_count = query.count()
        
        # Apply sorting
        if sort_by == 'degree':
            query = query.order_by(Node.degree_centrality.desc())
        elif sort_by == 'betweenness':
            query = query.order_by(Node.betweenness_centrality.desc())
        else:
            query = query.order_by(Node.id)
        
        # Apply pagination
        nodes = query.limit(limit).offset(offset).all()
        
        return jsonify({
            'total_count': total_count,
            'limit': limit,
            'offset': offset,
            'nodes': [node.to_dict() for node in nodes]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching nodes: {str(e)}")
        return jsonify({'error': 'fetch_failed', 'message': str(e)}), 500


@bp.route('/<network_id>/edges', methods=['GET'])
def get_edges(network_id):
    """Get edges with optional filtering."""
    
    try:
        limit = min(int(request.args.get('limit', 100)), 1000)
        offset = int(request.args.get('offset', 0))
        
        query = Edge.query.filter_by(network_id=network_id)
        total_count = query.count()
        
        edges = query.limit(limit).offset(offset).all()
        
        return jsonify({
            'total_count': total_count,
            'edges': [edge.to_dict() for edge in edges]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching edges: {str(e)}")
        return jsonify({'error': 'fetch_failed', 'message': str(e)}), 500


@bp.route('/<network_id>', methods=['DELETE'])
def delete_network(network_id):
    """Delete a network and all associated data."""
    
    try:
        network = Network.query.get(network_id)
        if not network:
            return jsonify({'error': 'not_found', 'message': 'Network not found'}), 404
        
        db.session.delete(network)
        db.session.commit()
        logger.info(f"Deleted network {network_id}")
        
        return '', 204
        
    except Exception as e:
        logger.error(f"Error deleting network: {str(e)}")
        return jsonify({'error': 'delete_failed', 'message': str(e)}), 500
