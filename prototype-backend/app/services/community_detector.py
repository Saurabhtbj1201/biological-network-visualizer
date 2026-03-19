"""
Community detection for biological networks.
Uses Louvain algorithm for modularity optimization.
"""

import networkx as nx
from community import community_louvain
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class CommunityDetector:
    """Detect communities in biological networks using Louvain algorithm."""
    
    @staticmethod
    def detect(graph: nx.Graph, **kwargs) -> Dict[str, Any]:
        """
        Detect communities using Louvain method.
        
        Args:
            graph: NetworkX graph
            **kwargs: Additional arguments for Louvain algorithm
                - randomize: bool (default: False)
                - seed: int (default: None)
                
        Returns:
            Dictionary with community structure and statistics
        """
        
        logger.info(f"Detecting communities in graph with {graph.number_of_nodes()} nodes")
        
        # Run Louvain algorithm
        partition = community_louvain.best_partition(graph, **kwargs)
        
        # Calculate modularity
        modularity = community_louvain.modularity(partition, graph)
        
        # Organize communities
        communities = {}
        for node, comm_id in partition.items():
            if comm_id not in communities:
                communities[comm_id] = []
            communities[comm_id].append(node)
        
        # Calculate community statistics
        community_stats = []
        for comm_id, nodes in sorted(communities.items()):
            subgraph = graph.subgraph(nodes)
            internal_edges = subgraph.number_of_edges()
            
            # Count external edges
            external_edges = 0
            for node in nodes:
                for neighbor in graph.neighbors(node):
                    if partition[neighbor] != comm_id:
                        external_edges += 1
            external_edges = external_edges // 2  # Each edge counted twice
            
            community_stats.append({
                'id': comm_id,
                'size': len(nodes),
                'internal_edges': internal_edges,
                'external_edges': external_edges,
                'density': nx.density(subgraph) if len(nodes) > 1 else 0
            })
        
        logger.info(f"Detected {len(communities)} communities with modularity Q={modularity:.4f}")
        
        return {
            'partition': partition,
            'modularity_q': modularity,
            'num_communities': len(communities),
            'communities': community_stats
        }
    
    @staticmethod
    def get_community_hierarchy(partition: Dict[str, int], 
                               graph: nx.Graph = None) -> Dict[str, Any]:
        """
        Analyze community structure hierarchy.
        
        Args:
            partition: Node to community ID mapping from detect()
            graph: Optional NetworkX graph for additional stats
            
        Returns:
            Dictionary with community structure analysis
        """
        
        # Group nodes by community
        communities = {}
        for node, comm_id in partition.items():
            if comm_id not in communities:
                communities[comm_id] = []
            communities[comm_id].append(node)
        
        # Sort by size
        community_sizes = sorted(
            [(cid, len(nodes)) for cid, nodes in communities.items()],
            key=lambda x: x[1], reverse=True
        )
        
        return {
            'community_count': len(communities),
            'communities_by_size': [
                {'id': cid, 'size': size, 'nodes': communities[cid][:10]}
                for cid, size in community_sizes
            ]
        }
