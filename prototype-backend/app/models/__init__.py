"""
Database models for NetworkInsight.
"""

from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
import json

class Network(db.Model):
    """Network entity - represents a biological network."""
    
    __tablename__ = 'networks'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, index=True)
    format = db.Column(db.String(50), nullable=False)  # 'sif', 'json', 'csv'
    nodes_count = db.Column(db.Integer, default=0)
    edges_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    file_path = db.Column(db.String(512))
    network_metadata = db.Column(JSON, default={})
    
    # Relationships
    nodes = db.relationship('Node', backref='network', lazy=True, cascade='all, delete-orphan')
    edges = db.relationship('Edge', backref='network', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': str(self.id),
            'name': self.name,
            'format': self.format,
            'nodes_count': self.nodes_count,
            'edges_count': self.edges_count,
            'created_at': self.created_at.isoformat(),
            'metadata': self.network_metadata,
            'status': 'ready'
        }


class Node(db.Model):
    """Node entity - represents a node in a network."""
    
    __tablename__ = 'nodes'
    
    id = db.Column(db.String(255), primary_key=True)  # Gene/protein ID
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('networks.id'), 
                          primary_key=True, index=True)
    label = db.Column(db.String(255))
    attributes = db.Column(JSON, default={})
    
    # Computed metrics (cached)
    degree_centrality = db.Column(db.Float)
    betweenness_centrality = db.Column(db.Float)
    closeness_centrality = db.Column(db.Float)
    eigenvector_centrality = db.Column(db.Float)
    pagerank = db.Column(db.Float)
    community_id = db.Column(db.Integer)
    is_hub = db.Column(db.Boolean, default=False, index=True)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'label': self.label or self.id,
            'degree': self.degree_centrality or 0,
            'degree_centrality': self.degree_centrality,
            'betweenness_centrality': self.betweenness_centrality,
            'closeness_centrality': self.closeness_centrality,
            'eigenvector_centrality': self.eigenvector_centrality,
            'pagerank': self.pagerank,
            'community_id': self.community_id,
            'is_hub': self.is_hub,
            'attributes': self.attributes
        }


class Edge(db.Model):
    """Edge entity - represents an edge in a network."""
    
    __tablename__ = 'edges'
    
    id = db.Column(db.String(511), primary_key=True)  # "source--target"
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('networks.id'), 
                          primary_key=True, index=True)
    source = db.Column(db.String(255), nullable=False, index=True)
    target = db.Column(db.String(255), nullable=False, index=True)
    weight = db.Column(db.Float, default=1.0)
    interaction_type = db.Column(db.String(100))
    attributes = db.Column(JSON, default={})
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'source': self.source,
            'target': self.target,
            'weight': self.weight,
            'interaction_type': self.interaction_type,
            'attributes': self.attributes
        }


class AnalysisCache(db.Model):
    """Cache for computed analysis results."""
    
    __tablename__ = 'analysis_cache'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    network_id = db.Column(UUID(as_uuid=True), db.ForeignKey('networks.id'), 
                          index=True)
    metric_type = db.Column(db.String(100), index=True)  # 'centrality', 'communities', etc.
    results = db.Column(JSON)
    computed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ttl_seconds = db.Column(db.Integer, default=86400)  # 24 hours
    
    def is_expired(self):
        """Check if cache entry has expired."""
        elapsed = (datetime.utcnow() - self.computed_at).total_seconds()
        return elapsed > self.ttl_seconds
