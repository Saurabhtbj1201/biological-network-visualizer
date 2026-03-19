"""
Analysis API routes - handle network analysis requests (metrics, communities, insights).
"""

from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Network, Node as NodeModel, Edge as EdgeModel, AnalysisCache
from app.services.metrics_calculator import MetricsCalculator
from app.services.community_detector import CommunityDetector
import networkx as nx
from datetime import datetime
import json
import logging

bp = Blueprint('analysis', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)


def load_graph_from_db(network_id: str) -> nx.Graph:
    """Load a network graph from database."""
    
    network = Network.query.get(network_id)
    if not network:
        raise ValueError(f"Network {network_id} not found")
    
    G = nx.Graph()
    
    # Add nodes
    nodes = NodeModel.query.filter_by(network_id=network_id).all()
    for node in nodes:
        G.add_node(node.id, label=node.label or node.id, **node.attributes)
    
    # Add edges
    edges = EdgeModel.query.filter_by(network_id=network_id).all()
    for edge in edges:
        G.add_edge(edge.source, edge.target, 
                  weight=edge.weight,
                  interaction_type=edge.interaction_type,
                  **edge.attributes)
    
    logger.info(f"Loaded graph from DB: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


@bp.route('/networks/<network_id>/analyze', methods=['POST'])
def analyze_network(network_id):
    """
    Calculate network metrics.
    
    Request JSON:
    {
        "metrics": ["degree", "betweenness", "closeness", "eigenvector", "pagerank"],
        "detect_communities": true,
        "cache": true
    }
    """
    
    try:
        data = request.get_json() or {}
        metrics_list = data.get('metrics', ['degree', 'betweenness'])
        detect_communities = data.get('detect_communities', True)
        use_cache = data.get('cache', True)
        
        network = Network.query.get(network_id)
        if not network:
            return jsonify({'error': 'not_found'}), 404
        
        # Load graph
        graph = load_graph_from_db(network_id)
        calculator = MetricsCalculator(graph)
        
        # Calculate metrics
        logger.info(f"Calculating metrics: {metrics_list}")
        metrics_results = {}
        for metric in metrics_list:
            if metric in MetricsCalculator.AVAILABLE_METRICS:
                metrics_results[metric] = calculator.calculate(metric)
        
        # Update nodes with metrics in database
        for metric, values in metrics_results.items():
            for node_id, value in values.items():
                node = NodeModel.query.get((node_id, network_id))
                if node:
                    if metric == 'degree':
                        node.degree_centrality = value
                    elif metric == 'betweenness':
                        node.betweenness_centrality = value
                    elif metric == 'closeness':
                        node.closeness_centrality = value
                    elif metric == 'eigenvector':
                        node.eigenvector_centrality = value
                    elif metric == 'pagerank':
                        node.pagerank = value
        
        # Detect communities
        communities_data = None
        if detect_communities:
            logger.info("Detecting communities...")
            communities_result = CommunityDetector.detect(graph)
            communities_data = communities_result
            
            # Update nodes with community assignments
            for node_id, comm_id in communities_result['partition'].items():
                node = NodeModel.query.get((node_id, network_id))
                if node:
                    node.community_id = comm_id
        
        # Identify hubs
        hub_result = calculator.get_hub_nodes(percentile=90)
        for hub_info in hub_result.get('hubs', []):
            node = NodeModel.query.get((hub_info['node'], network_id))
            if node:
                node.is_hub = True
        
        db.session.commit()
        
        # Cache results
        cache_entry = AnalysisCache(
            network_id=network_id,
            metric_type='all_analysis',
            results={
                'metrics': {k: dict(v) for k, v in metrics_results.items()},
                'communities': communities_data,
                'hubs': hub_result,
                'stats': calculator.get_network_stats()
            }
        )
        db.session.add(cache_entry)
        db.session.commit()
        
        return jsonify({
            'network_id': str(network_id),
            'status': 'completed',
            'computed_at': datetime.utcnow().isoformat(),
            'results': {
                'metrics': {k: dict(v) for k, v in metrics_results.items()},
                'communities': communities_data,
                'hubs': hub_result,
                'stats': calculator.get_network_stats()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing network: {str(e)}", exc_info=True)
        return jsonify({'error': 'analysis_failed', 'message': str(e)}), 500


@bp.route('/networks/<network_id>/communities', methods=['GET'])
def get_communities(network_id):
    """Get detected community structure."""
    
    try:
        network = Network.query.get(network_id)
        if not network:
            return jsonify({'error': 'not_found'}), 404
        
        # Load graph
        graph = load_graph_from_db(network_id)
        
        # Detect communities
        result = CommunityDetector.detect(graph)
        
        return jsonify({
            'modularity_q': result['modularity_q'],
            'num_communities': result['num_communities'],
            'communities': result['communities']
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting communities: {str(e)}")
        return jsonify({'error': 'fetch_failed', 'message': str(e)}), 500


@bp.route('/networks/<network_id>/insights', methods=['GET'])
def get_insights(network_id):
    """Get AI-assisted insights about the network."""
    
    try:
        network = Network.query.get(network_id)
        if not network:
            return jsonify({'error': 'not_found'}), 404
        
        # Load graph
        graph = load_graph_from_db(network_id)
        calculator = MetricsCalculator(graph)
        
        insights = []
        
        # Network statistics
        stats = calculator.get_network_stats()
        if stats['nodes'] > 0:
            insights.append({
                'type': 'network_summary',
                'message': f"Network contains {stats['nodes']} nodes and {stats['edges']} edges. "
                          f"Average degree: {stats['avg_degree']:.2f}",
                'severity': 'info'
            })
        
        # Hub nodes
        hubs = calculator.get_hub_nodes(percentile=90)
        if hubs['count'] > 0:
            top_hub = hubs['hubs'][0] if hubs['hubs'] else None
            insights.append({
                'type': 'hub_detection',
                'message': f"Network contains {hubs['count']} hub nodes. "
                          f"Top hub: {top_hub['node']} with score {top_hub['score']:.4f}",
                'severity': 'info'
            })
        
        # Bottleneck nodes
        bottlenecks = calculator.get_bottleneck_nodes(percentile=90)
        if bottlenecks['count'] > 0:
            insights.append({
                'type': 'bottleneck_warning',
                'message': f"Identified {bottlenecks['count']} bottleneck nodes. "
                          f"These are critical for network connectivity.",
                'severity': 'warning'
            })
        
        # Communities
        try:
            communities = CommunityDetector.detect(graph)
            if communities['num_communities'] > 1:
                insights.append({
                    'type': 'community_structure',
                    'message': f"Detected {communities['num_communities']} communities "
                              f"with modularity Q={communities['modularity_q']:.3f}",
                    'severity': 'info'
                })
        except:
            pass
        
        return jsonify({
            'network_id': str(network_id),
            'insights': insights
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return jsonify({'error': 'insights_failed', 'message': str(e)}), 500


# Blueprint __init__ requirement
from app.api import networks
