# NetworkInsight Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                              │
│                      (http://localhost:3000)                        │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTP/WebSocket
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Redux)                         │
│                     Port 3000 (Vite Dev Server)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                       React Components                       │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  • App.tsx ──────┐                                          │  │
│  │  • FileUploadPanel.tsx  ───┐                                │  │
│  │  • NetworkDetail.tsx (pending)                              │  │
│  │  • GraphVisualization.tsx (pending)                         │  │
│  │  • MetricsPanel.tsx (pending)                               │  │
│  │  • FilterPanel.tsx (pending)                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                               │                                    │
│                               │ dispatch actions                   │
│                               ▼                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Redux Store                              │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  • networkSlice.ts  ─────────────┐                          │  │
│  │    └─ networks, currentNetworkId  │ State                   │  │
│  │    └─ loading, error             │                         │  │
│  │                                  │                         │  │
│  │  • metricsSlice.ts  ──────────────┼─ Combined              │  │
│  │    └─ byNetworkId metrics         │ reducers               │  │
│  │                                  │                         │  │
│  │  • filtersSlice.ts  ──────────────┤                         │  │
│  │    └─ degree, centrality, etc.    │                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                               │                                    │
│                               │ selectors                          │
│                               ▼                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  API Client (Axios)                         │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  • uploadNetwork()      ├─ POST /networks/upload            │  │
│  │  • getNetwork()         ├─ GET /networks/{id}               │  │
│  │  • getNodes()           ├─ GET /networks/{id}/nodes         │  │
│  │  • getEdges()           ├─ GET /networks/{id}/edges         │  │
│  │  • deleteNetwork()      ├─ DELETE /networks/{id}            │  │
│  │  • analyzeNetwork()     ├─ POST /networks/{id}/analyze      │  │
│  │  • getCommunities()     ├─ GET /networks/{id}/communities   │  │
│  │  • getInsights()        ├─ GET /networks/{id}/insights      │  │
│  │  • healthCheck()        └─ GET /health                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTP REST (JSON)
                               │ http://localhost:5000/api
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  BACKEND (Flask + Python)                           │
│                     Port 5000 (Gunicorn)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   Flask Application                         │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │              API Routes (Blueprints)                │   │  │
│  │  ├─────────────────────────────────────────────────────┤   │  │
│  │  │  • networks.py                                      │   │  │
│  │  │    ├─ POST /upload ──┐                             │   │  │
│  │  │    ├─ GET /{id}      │                             │   │  │
│  │  │    ├─ GET /{id}/nodes│                             │   │  │
│  │  │    ├─ GET /{id}/edges├─ API Layer                  │   │  │
│  │  │    └─ DELETE /{id}   │                             │   │  │
│  │  │                      │                             │   │  │
│  │  │  • analysis.py       │                             │   │  │
│  │  │    ├─ POST /analyze  │                             │   │  │
│  │  │    ├─ GET /communities                             │   │  │
│  │  │    └─ GET /insights  │                             │   │  │
│  │  └───────┬──────────────────────────────────────────────┘   │  │
│  │          │ calls / instantiates                            │  │
│  │          ▼                                                 │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │              Service Layer                         │   │  │
│  │  ├─────────────────────────────────────────────────────┤   │  │
│  │  │  ┌────────────────────────────────────────────┐    │   │  │
│  │  │  │ FileParser                                 │    │   │  │
│  │  │  │  • parse(file_path, format)               │    │   │  │
│  │  │  │  • _parse_sif(), _parse_json(),           │    │   │  │
│  │  │  │    _parse_csv()                           │    │   │  │
│  │  │  │  → returns (NetworkX.Graph, metadata)     │    │   │  │
│  │  │  └─────────────┬──────────────────────────────┘    │   │  │
│  │  │                │                                   │   │  │
│  │  │  ┌─────────────▼──────────────────────────────┐    │   │  │
│  │  │  │ MetricsCalculator                         │    │   │  │
│  │  │  │  • calculate(metric)                      │    │   │  │
│  │  │  │  • get_hub_nodes()                        │    │   │  │
│  │  │  │  • get_bottleneck_nodes()                 │    │   │  │
│  │  │  │  • get_network_stats()                    │    │   │  │
│  │  │  │  → returns centrality scores,                │   │  │
│  │  │  │    bottleneck detection                  │    │   │  │
│  │  │  └─────────────┬──────────────────────────────┘    │   │  │
│  │  │                │                                   │   │  │
│  │  │  ┌─────────────▼──────────────────────────────┐    │   │  │
│  │  │  │ CommunityDetector                         │    │   │  │
│  │  │  │  • detect(graph)                          │    │   │  │
│  │  │  │  • get_community_hierarchy()              │    │   │  │
│  │  │  │  → Louvain algorithm + stats              │    │   │  │
│  │  │  └────────────────────────────────────────────┘    │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                   │                                       │  │
│  │                   │ reads/writes                         │  │
│  │                   ▼                                       │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │              Data Models (SQLAlchemy)             │   │  │
│  │  ├─────────────────────────────────────────────────────┤   │  │
│  │  │  • Network                                        │   │  │
│  │  │    └─ id, name, format, nodes_count,             │   │  │
│  │  │       edges_count, created_at, metadata          │   │  │
│  │  │                                                  │   │  │
│  │  │  • Node ◄──── foreign key relationship           │   │  │
│  │  │    └─ id, network_id (FK), label, attributes,    │   │  │
│  │  │       degree_centrality, betweenness_centrality, │   │  │
│  │  │       closeness_centrality, eigenvector_centrality,│  │
│  │  │       pagerank, community_id, is_hub             │   │  │
│  │  │                                                  │   │  │
│  │  │  • Edge ◄──── foreign key relationship           │   │  │
│  │  │    └─ id, network_id (FK), source, target,       │   │  │
│  │  │       weight, interaction_type, attributes       │   │  │
│  │  │                                                  │   │  │
│  │  │  • AnalysisCache                                 │   │  │
│  │  │    └─ network_id, metric_type, results (JSON),   │   │  │
│  │  │       computed_at, ttl_seconds, is_expired()     │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
         ┌─────────────┐ ┌──────────┐  ┌──────────┐
         │ PostgreSQL  │ │  Redis   │  │File Sys  │
         │ Port 5432   │ │Port 6379 │  │(uploads) │
         ├─────────────┤ ├──────────┤  └──────────┘
         │  networks   │ │ Metrics  │
         │  nodes      │ │ cache    │
         │  edges      │ │(24h TTL) │
         │  analysis   │ │          │
         │  _cache     │ │          │
         └─────────────┘ └──────────┘


```

---

## Data Flow Diagram

### User Upload → Analysis Complete

```
User Browser                                   Backend                          Database
    │                                            │                                │
    │  1. Select file + name                    │                                │
    ├──────────────────────────────────────────►│                                │
    │                                            │                                │
    │                                            │  2. Validate & Parse file      │
    │                                            │  (FileParser service)          │
    │                                            │                                │
    │                                            │  3. Create Network record      │
    │                                            ├───────────────────────────────►│
    │                                            │                                │
    │                                            │  4. Insert Nodes               │
    │                                            ├───────────────────────────────►│
    │                                            │                                │
    │                                            │  5. Insert Edges               │
    │                                            ├───────────────────────────────►│
    │                                            │                                │
    │  6. Return network_id                     │                                │
    │◄──────────────────────────────────────────┤                                │
    │                                            │                                │
    │  7. Call /analyze endpoint                │                                │
    ├──────────────────────────────────────────►│                                │
    │                                            │                                │
    │                                            │  8. Load graph from DB         │
    │                                            ├───────────────────────────────►│
    │                                            │◄───────────────────────────────┤
    │                                            │  (Nodes + Edges)               │
    │                                            │                                │
    │                                            │  9. Calculate Centralities     │
    │                                            │     (MetricsCalculator)        │
    │                                            │                                │
    │                                            │  10. Detect Communities        │
    │                                            │      (CommunityDetector)       │
    │                                            │                                │
    │                                            │  11. Update Node metrics       │
    │                                            ├───────────────────────────────►│
    │                                            │                                │
    │                                            │  12. Cache results             │
    │                                            ├───────────────────────────────►│
    │                                            │  (Redis, 24h TTL)             │
    │                                            │                                │
    │  13. Return analysis results              │                                │
    │◄──────────────────────────────────────────┤                                │
    │                                            │                                │
    │  14. Store in Redux                       │                                │
    │  15. Render graph + metrics               │                                │
    │                                            │                                │
```

---

## Technology Stack

### Frontend
```
React 18
  ├─ Components (JSX)
  ├─ Hooks (useState, useEffect, useSelector, useDispatch)
  └─ Rendering

Redux Toolkit
  ├─ Store
  ├─ Slices (networkSlice, metricsSlice, filtersSlice)
  └─ Async Thunks (future)

Cytoscape.js
  └─ Graph visualization (planned)

Tailwind CSS
  └─ Styling

Axios
  └─ HTTP Client

Vite
  └─ Build tool & dev server

TypeScript
  └─ Type safety
```

### Backend
```
Flask 3.0
  ├─ Application factory
  ├─ Blueprints (networks, analysis)
  ├─ Error handlers
  └─ Middleware (CORS, logging)

SQLAlchemy 2.0
  ├─ ORM models
  ├─ Relationships
  └─ Query API

NetworkX 3.2
  ├─ Graph algorithms
  ├─ Centrality measures
  ├─ Community detection (skeleton)
  └─ Network statistics

python-louvain
  └─ Community detection (Louvain method)

PostgreSQL / SQLite
  └─ Persistent data storage

Redis
  └─ Caching layer

Gunicorn
  └─ WSGI application server
```

---

## Component Hierarchy

```
App
├── Header
├── Main Content (conditional rendering)
│   ├── FileUploadPanel (if no current network)
│   │   └── Input field + drag-drop zone
│   └── NetworkDetail (if current network selected)
│       ├── GraphVisualization (pending)
│       ├── FilterPanel (pending)
│       │   ├── DegreeFilter
│       │   ├── CentralityFilter
│       │   ├── CommunityFilter
│       │   └── WeightFilter
│       ├── MetricsPanel (pending)
│       │   ├── NodeTable
│       │   ├── StatsCard
│       │   └── ChartContainer
│       └── CommunityPanel (pending)
├── NetworkGrid
│   └── NetworkCard (for each network)
└── Footer
```

---

## API Endpoints Reference

### Network Management
```
POST   /api/networks/upload          → Create network from file
GET    /api/networks/{id}            → Get network metadata
GET    /api/networks/{id}/nodes      → List nodes with metrics
GET    /api/networks/{id}/edges      → List edges
DELETE /api/networks/{id}            → Delete network
```

### Analysis
```
POST   /api/networks/{id}/analyze    → Calculate all metrics + communities
GET    /api/networks/{id}/communities → Get community structure
GET    /api/networks/{id}/insights   → AI-assisted insights
```

### System
```
GET    /health                       → Health check
```

---

## Database Schema

### Networks Table
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| name | String | User-provided name |
| format | String | SIF, JSON, CSV |
| nodes_count | Integer | Computed |
| edges_count | Integer | Computed |
| created_at | DateTime | Auto-filled |
| metadata | JSON | Format-specific data |

### Nodes Table
| Column | Type | Notes |
|--------|------|-------|
| id | String | Primary key |
| network_id | UUID | Foreign key → Networks |
| label | String | Node name/identifier |
| attributes | JSON | User-defined attributes |
| degree_centrality | Float | 0.0-1.0 |
| betweenness_centrality | Float | 0.0-1.0 |
| closeness_centrality | Float | 0.0-1.0 |
| eigenvector_centrality | Float | 0.0-1.0 |
| pagerank | Float | Varies |
| community_id | Integer | Louvain result |
| is_hub | Boolean | Top 10% degree nodes |

### Edges Table
| Column | Type | Notes |
|--------|------|-------|
| id | String | "source--target" |
| network_id | UUID | Foreign key → Networks |
| source | String | Node ID |
| target | String | Node ID |
| weight | Float | Optional, default 1.0 |
| interaction_type | String | Optional, e.g., "protein_interaction" |
| attributes | JSON | User-defined |

### Analysis Cache Table
| Column | Type | Notes |
|--------|------|-------|
| network_id | UUID | Primary key (part 1) |
| metric_type | String | Primary key (part 2), e.g., "centrality" |
| results | JSON | Cached computation results |
| computed_at | DateTime | When computed |
| ttl_seconds | Integer | Cache validity (86400 = 1 day) |

---

## Redux State Shape

```
{
  networks: {
    networks: {
      "net-1": {id, name, nodeCount, edgeCount, createdAt},
      "net-2": {...}
    },
    currentNetworkId: "net-1",
    loading: false,
    error: null
  },
  
  metrics: {
    byNetworkId: {
      "net-1": {
        "node1": {degree: 0.5, betweenness: 0.3, ...},
        "node2": {...}
      }
    },
    loading: false | "net-1",  // false or network ID
    cache: {
      "net-1": {timestamp: 1234567890, ttl: 86400}
    }
  },
  
  filters: {
    byNetworkId: {
      "net-1": {
        degree: {min: 0, max: 100},
        centrality: {metric: "degree", threshold: 0.5},
        communities: {selected: [1, 2, 3]},
        weight: {min: 0, max: 1},
        activeFilters: ["degree", "community"]
      }
    }
  }
}
```

---

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────┐
│          Internet / Users                   │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│      Load Balancer (Nginx)                  │
└─────────────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
┌──────────────┐   ┌──────────────┐
│ Frontend     │   │ Backend      │
│ Container    │   │ Container    │
│ (Node 20)    │   │ (Python 3.11)│
└──────────────┘   └──────────────┘
    │                   │
    └─────────┬─────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│    PostgreSQL RDS / managed database        │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│    Redis ElastiCache / managed cache        │
└─────────────────────────────────────────────┘
```

---

## Performance Characteristics

| Metric | Target | Notes |
|--------|--------|-------|
| File upload | <1s | Direct file I/O |
| Network parsing | <500ms | Depends on file size |
| Centrality calc (1000 nodes) | <2s | NetworkX optimized |
| Community detection (1000 nodes) | <1s | Louvain algorithm |
| API response time | <200ms | Cached metrics |
| Frontend render | <100ms | React reconciliation |
| Graph visualization | <1s | Cytoscape.js rendering |

---

## Error Handling Strategy

```
Client Request
    │
    ▼
API Validation (400 Bad Request)
    │
    ▼
Authentication (401 Unauthorized)
    │
    ▼
Authorization (403 Forbidden)
    │
    ▼
Business Logic (422 Unprocessable Entity)
    │
    ├─→ File parsing error
    ├─→ Invalid network format
    ├─→ Missing required field
    │
    ▼
Database Operation (500 Internal Server Error)
    │
    ├─→ Connection failure
    ├─→ Constraint violation
    │
    ▼
Success (200 OK) with JSON response
    │
    ▼
Frontend Redux dispatch
    │
    ▼
Component re-render with new data
```

---

## Security Considerations

✅ **Implemented**:
- CORS headers (restrict to frontend origin)
- File type validation (whitelist SIF, JSON, CSV)
- Max file size limit (10MB)
- Input sanitization (file names, node labels)
- UUID for network IDs (not sequential)

🟡 **Pending**:
- Authentication (JWT tokens)
- Rate limiting (prevent brute force)
- SQL injection protection (SQLAlchemy parameterized queries ✅)
- XSS prevention (React escaping ✅)
- HTTPS in production
- Database encryption at rest

---

**End of Architecture Documentation**
