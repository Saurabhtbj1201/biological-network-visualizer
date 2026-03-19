"""
Network metrics calculator using NetworkX.
Implements centrality measures and network analysis.
"""

import networkx as nx
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Calculate centrality measures for biological networks."""
    
    AVAILABLE_METRICS = ['degree', 'betweenness', 'closeness', 'eigenvector', 'pagerank']
    
    def __init__(self, graph: nx.Graph):
        """Initialize with a NetworkX graph."""
        self.graph = graph
        self._metrics_cache = {}
    
    def calculate_all(self) -> Dict[str, Dict[str, float]]:
        """Calculate all available centrality measures."""
        logger.info(f"Calculating all metrics for graph with {self.graph.number_of_nodes()} nodes")
        
        results = {}
        for metric in self.AVAILABLE_METRICS:
            results[metric] = self.calculate(metric)
        
        return results
    
    def calculate(self, metric: str) -> Dict[str, float]:
        """
        Calculate a specific centrality metric.
        
        Args:
            metric: One of 'degree', 'betweenness', 'closeness', 'eigenvector', 'pagerank'
            
        Returns:
            Dictionary with node IDs as keys and centrality scores as values
        """
        
        if metric not in self.AVAILABLE_METRICS:
            raise ValueError(f"Unknown metric: {metric}. Available: {self.AVAILABLE_METRICS}")
        
        # Return cached result if available
        if metric in self._metrics_cache:
            logger.debug(f"Returning cached {metric} metric")
            return self._metrics_cache[metric]
        
        logger.info(f"Computing {metric} centrality for {self.graph.number_of_nodes()} nodes")
        
        if metric == 'degree':
            result = nx.degree_centrality(self.graph)
        elif metric == 'betweenness':
            result = nx.betweenness_centrality(self.graph)
        elif metric == 'closeness':
            result = nx.closeness_centrality(self.graph)
        elif metric == 'eigenvector':
            try:
                result = nx.eigenvector_centrality(self.graph, max_iter=1000)
            except nx.NetworkXError:
                # Fallback for disconnected graphs
                logger.warning("Eigenvector centrality failed, using fallback")
                result = {node: 0.0 for node in self.graph.nodes()}
        elif metric == 'pagerank':
            result = nx.pagerank(self.graph)
        
        # Cache the result
        self._metrics_cache[metric] = result
        return result
    
    def get_hub_nodes(self, percentile: float = 90) -> Dict[str, Any]:
        """
        Identify hub nodes based on degree centrality.
        
        Args:
            percentile: Top percentile threshold (default: 90 = top 10%)
            
        Returns:
            Dictionary with hub information
        """
        degree_cent = self.calculate('degree')
        
        # Calculate threshold
        sorted_values = sorted(degree_cent.values(), reverse=True)
        threshold_idx = max(0, int(len(sorted_values) * (100 - percentile) / 100))
        threshold = sorted_values[threshold_idx] if threshold_idx < len(sorted_values) else 0
        
        hubs = {node: score for node, score in degree_cent.items() if score >= threshold}
        hubs_sorted = sorted(hubs.items(), key=lambda x: x[1], reverse=True)
        
        logger.info(f"Identified {len(hubs)} hub nodes at {percentile}th percentile "
                   f"(threshold: {threshold:.4f})")
        
        return {
            'count': len(hubs),
            'threshold': threshold,
            'percentile': percentile,
            'hubs': [{'node': node, 'score': score} for node, score in hubs_sorted[:20]]
        }
    
    def get_bottleneck_nodes(self, percentile: float = 90) -> Dict[str, Any]:
        """
        Identify bottleneck nodes based on betweenness centrality.
        These are nodes critical for network connectivity.
        
        Args:
            percentile: Top percentile threshold (default: 90 = top 10%)
            
        Returns:
            Dictionary with bottleneck information
        """
        between_cent = self.calculate('betweenness')
        
        # Calculate threshold
        sorted_values = sorted(between_cent.values(), reverse=True)
        threshold_idx = max(0, int(len(sorted_values) * (100 - percentile) / 100))
        threshold = sorted_values[threshold_idx] if threshold_idx < len(sorted_values) else 0
        
        bottlenecks = {node: score for node, score in between_cent.items() 
                      if score >= threshold}
        bottlenecks_sorted = sorted(bottlenecks.items(), key=lambda x: x[1], reverse=True)
        
        logger.info(f"Identified {len(bottlenecks)} bottleneck nodes at {percentile}th percentile")
        
        return {
            'count': len(bottlenecks),
            'threshold': threshold,
            'percentile': percentile,
            'bottlenecks': [{'node': node, 'score': score} 
                          for node, score in bottlenecks_sorted[:20]]
        }
    
    def get_network_stats(self) -> Dict[str, Any]:
        """
        Get basic network statistics.
        
        Returns:
            Dictionary with network properties
        """
        
        if self.graph.number_of_nodes() == 0:
            return {
                'nodes': 0,
                'edges': 0,
                'density': 0,
                'diameter': 0,
                'is_connected': False,
                'components': 0
            }
        
        # Calculate average degree
        avg_degree = 2 * self.graph.number_of_edges() / self.graph.number_of_nodes()
        
        # Calculate density
        density = nx.density(self.graph)
        
        # Calculate diameter (for largest connected component)
        if nx.is_connected(self.graph):
            diameter = nx.diameter(self.graph)
            components = 1
        else:
            largest_cc = max(nx.connected_components(self.graph), key=len)
            subgraph = self.graph.subgraph(largest_cc)
            diameter = nx.diameter(subgraph) if subgraph.number_of_nodes() > 1 else 0
            components = nx.number_connected_components(self.graph)
        
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'avg_degree': avg_degree,
            'density': density,
            'diameter': diameter if diameter > 0 else None,
            'is_connected': nx.is_connected(self.graph),
            'components': components
        }
