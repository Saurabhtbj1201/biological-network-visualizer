# GSoC 2026 Proposal: AI-Assisted Analysis and Visualization of Biological Networks

## Personal Information

| Field | Details |
|-------|---------|
| **Name** | Saurabh Kumar |
| **GitHub** | [@SaurabhtBJ1201](https://github.com/Saurabhtbj1201) |
| **Email** | Saurabhtbj143@gmail.com |
| **Phone** | +91 9798024301 |
| **LinkedIn** | https://www.linkedin.com/in/saurabhtbj1201/ |
| **Portfolio** | https://projects.gu-saurabh.site/about |
| **Location** | Noida, Gautam Buddha Nagar, Uttar Pradesh, India |
| **Education** | Bachelor of Computer Applications (BCA), Galgotias University |
| **Availability** | 40 hours/week, May–August 2026; No conflicting commitments |

---

## Executive Summary

This proposal aims to develop **NetworkInsight**, an open-source web-based platform for interactive visualization and AI-assisted analysis of biological networks. The project will integrate with NRNB's ecosystem (particularly Cytoscape) to provide researchers with an accessible entry point for network exploration, featuring real-time graph rendering, centrality-based node analysis, community detection, and intelligent pattern identification—dramatically reducing the learning curve for non-computational biologists.

**Key Innovation**: Combine interactive visualization with automated network insights (centrality measures, community clusters, hub identification) to enable domain experts—not just bioinformaticians—to extract biological meaning from complex network data.

---

## Section 1: Personal Background & Motivation

### Why This Project?

Network-driven research is fundamental to modern biology: understanding gene interactions, protein pathways, disease mechanisms, and drug targets all depend on analyzing complex relational data. However, despite tools like Cytoscape being powerful, they have steeper learning curves that exclude many wet-lab biologists and early-career researchers.

**My motivation**: I'm fascinated by the intersection of data visualization and scientific discovery. Through projects like my personal portfolio site and e-commerce dashboards, I've learned how thoughtful interface design makes complex data accessible. I want to apply this lens to biological networks—making network analysis less intimidating and more intuitive.

### Relevant Project Experience

1. **Admin Dashboard for E-Commerce** (`My Projects/MegaBasket e-commerce/`)
   - Built React-based dashboard with interactive data visualizations
   - Implemented real-time filtering, sorting, and chart rendering
   - *Relevance*: Front-end architecture patterns, state management, user experience design

2. **Email Spam Detection System** (`My Projects/email_spam_detection (ML)/`)
   - Python backend: data preprocessing, feature extraction, ML model training
   - Achieved 92% classification accuracy using scikit-learn + logistic regression
   - *Relevance*: Python ecosystem familiarity, data pipeline design, model evaluation

3. **Personal Portfolio Website** (`https://projects.gu-saurabh.site/about`)
   - Full-stack React application with TypeScript
   - Responsive design, API integration, performance optimization
   - *Relevance*: Production-ready code quality, deployment experience, modern web standards

### Current Skill Inventory

| Category | Skills | Proficiency |
|----------|--------|-------------|
| **Languages** | JavaScript (ES6+), Python (3.9+), TypeScript | Strong |
| **Frontend** | React, HTML5, CSS3, Tailwind CSS, REST APIs | Strong |
| **Visualization** | Basic D3.js, data charts (Chart.js) | Intermediate |
| **Backend** | Flask, Python data processing | Intermediate |
| **Data** | CSV/JSON parsing, pandas, NumPy | Intermediate |
| **DevOps** | Git, GitHub, GitHub Actions, deployment | Intermediate |
| **Graph Concepts** | Basic understanding; committed to rapid deep-dive | Beginner→Intermediate |

### Learning Commitment for GSoC

I acknowledge that biological networks and bioinformatics are new domains for me. **My learning plan**:

**Before GSoC Start**: 
- Study NRNB tools, Cytoscape plugins, and network data formats (SIF, JSON, GraphML)
- Complete online courses: graph algorithms, network analysis fundamentals
- Review biological network literature (gene interactions, protein networks, pathway analysis)
- Engage with NRNB community forums and documentation

**During Community Bonding**:
- 1-on-1 with mentors: architecture review, tool selection validation
- Set up development environment with NRNB tools
- Create detailed technical specification based on mentor input
- Identify 2–3 real biological datasets for testing

**Throughout GSoC**:
- Weekly mentor check-ins to validate domain understanding
- Document learning in blog posts for the NRNB community
- Engage with mentors early when uncertain about biological concepts

---

## Section 2: Project Overview

### Problem Statement

**The Challenge**: Biological network analysis is increasingly central to biomedical research, yet existing tools have barriers to adoption:

- **Complexity**: Tools like Cytoscape are feature-rich but intimidating for researchers without computational backgrounds
- **Data Accessibility**: Network data exists in multiple formats (SIF, GraphML, JSON, CSV); manual parsing is error-prone
- **Insight Generation**: Manual calculation of network metrics (centrality, clustering, hubs) is tedious; automating these insights is non-standard across platforms
- **Interactivity Gap**: Most tools optimize for static analysis; real-time filtering and exploration are underutilized
- **Mobile/Web Accessibility**: Many researchers prefer quick web-based exploration before diving into heavyweight desktop software

### Solution Overview

**NetworkInsight** will be a modern, web-based platform providing:

1. **Zero-Friction Visualization**: Drag-and-drop network file upload; immediate interactive visualization
2. **Automated Network Analysis**: One-click calculation and visualization of:
   - Centrality measures (degree, betweenness, closeness, eigenvector)
   - Community detection (using modularity optimization)
   - Hub identification and outlier nodes
3. **Smart Filtering & Exploration**: Highlight important nodes by centrality; filter by edge weight, node degree, or custom criteria
4. **Integration-Ready Design**: Export results to Cytoscape, download as publication-ready graphics, API for downstream tools
5. **Educational Value**: Embedded explanations of network metrics help users understand—not just view—their data

### Success Definition

By end of GSoC, NetworkInsight will:
- ✅ Load and visualize biological networks (1000+ nodes) in <2 seconds
- ✅ Calculate 5+ network metrics accurately and display interactively
- ✅ Support import from 3+ standard formats (SIF, JSON, GraphML, TSV)
- ✅ Provide REST API for programmatic access
- ✅ Include comprehensive documentation and 2–3 example datasets
- ✅ Achieve >70% test coverage and pass accessibility audit (WCAG 2.1 AA)

---

## Section 3: Project Scope & Deliverables

### Detailed Deliverables (12 Weeks)

#### **Phase 1: Foundation (Weeks 1–4)**

**Deliverable 1a: Project Architecture & Setup**
- [x] Repository created with branching strategy (main/develop/feature-*)
- [x] Docker Compose environment: React frontend + Flask backend
- [x] CI/CD pipeline (GitHub Actions) for automated testing
- [x] Dev documentation: local setup, coding standards, contribution guidelines
- **Acceptance Criteria**: New developer can clone, run `docker-compose up`, see working app in 15 minutes

**Deliverable 1b: Core Visualization Engine**
- [x] React component for graph rendering using Cytoscape.js
- [x] Support for node/edge rendering with customizable styles
- [x] Basic interactions: zoom, pan, node selection
- [x] Performance: Handle 1000+ nodes with smooth rendering (>30 FPS)
- **Acceptance Criteria**: Load `test_network.json` (500 nodes); zoom and pan are responsive; no lag

**Deliverable 1c: Data Import Pipeline**
- [x] Parser for 3 input formats:
  - SIF (Simple Interaction Format): `geneA geneB`
  - JSON: `{nodes: [...], edges: [...]}`
  - TSV/CSV: Convert tabular data to network format
- [x] Validation: Detect & report malformed data
- [x] Error handling: Graceful degradation for incomplete datasets
- **Acceptance Criteria**: Successfully import 5 test files; validation catches missing mandatory fields

**Deliverable 1d: Backend Foundation**
- [x] Flask REST API with endpoints:
  - `POST /api/upload` – Ingest network file
  - `GET /api/networks/<id>` – Retrieve network data
  - `POST /api/analyze` – Trigger network analysis
- [x] Database schema for storing networks (PostgreSQL or SQLite)
- [x] Authentication layer (optional for MVP; nice-to-have for multi-user)
- **Acceptance Criteria**: All endpoints tested and documented with cURL examples

---

#### **Phase 2: Analysis & Interaction (Weeks 5–8) [MIDTERM]**

**Deliverable 2a: Network Metrics Engine**
- [x] Implement 5 centrality measures using NetworkX:
  - **Degree Centrality**: Node importance by edge count
  - **Betweenness Centrality**: Node importance as pathway hub
  - **Closeness Centrality**: Node proximity to others
  - **Eigenvector Centrality**: Influence through connected high-influence nodes
  - **PageRank**: Graph-wide importance ranking
- [x] Unit tests: Validate against published benchmarks (Karate Club network, etc.)
- [x] Performance: Calculate metrics for 5000-node graph in <5 seconds
- **Acceptance Criteria**: All metrics tested; consistent with NetworkX reference implementation

**Deliverable 2b: Community Detection**
- [x] Implement Louvain algorithm (modularity-based community detection)
- [x] Assign community IDs to nodes
- [x] Visualize communities with color-coding and edge grouping
- [x] Extract community statistics (size, internal edge density)
- **Acceptance Criteria**: Detect clusters in test networks; output community report with statistics

**Deliverable 2c: Interactive UI Enhancements**
- [x] Filter dashboard:
  - By centrality threshold (show top 10% nodes)
  - By node degree range (degree ≥ 5)
  - By community membership
  - By edge weight/confidence
- [x] Node highlighting: Select node → show incoming/outgoing edges, connected subgraph
- [x] Tooltips: Hover over node → display metrics (degree, centrality scores, community ID)
- [x] Legend: Explain visual encoding (color = community, size = betweenness, etc.)
- **Acceptance Criteria**: All filters work correctly; no UI lag with 1000+ nodes

**Deliverable 2d: API Expansion**
- [x] New endpoints:
  - `POST /api/networks/<id>/metrics` – Calculate and return centrality measures
  - `POST /api/networks/<id>/communities` – Return community structure
  - `GET /api/networks/<id>/subgraph?nodes=X,Y,Z` – Extract subgraph
  - `POST /api/networks/<id>/export?format=cytoscape|json|svg` – Export in multiple formats
- [x] Rate limiting and request validation
- **Acceptance Criteria**: All endpoints functional and documented

---

#### **Phase 3: Polish, Optimization & Documentation (Weeks 9–12)**

**Deliverable 3a: Performance & Scalability**
- [x] Profile frontend rendering; optimize for 5000+ nodes (lazy loading, virtualization)
- [x] Backend optimization: Caching of computed metrics, database indexing
- [x] Load testing: Simulate 100+ concurrent API requests; ensure <500ms response time
- [x] Memory profiling: Ensure no memory leaks during long sessions
- **Acceptance Criteria**: Handle 5000-node network smoothly; API response times capped at 500ms

**Deliverable 3b: Testing & Quality Assurance**
- [x] Unit tests: >70% code coverage (frontend + backend)
  - Test data parsers, metrics calculations, API endpoints
- [x] Integration tests: End-to-end workflows (upload → parse → analyze → visualize)
- [x] Accessibility audit: WCAG 2.1 AA compliance
  - Keyboard navigation, screen reader support, color contrast
- [x] Bug fixes and edge case handling
- **Acceptance Criteria**: All tests pass; test coverage reported; accessibility issues resolved

**Deliverable 3c: Documentation**
- [x] **User Guide** (`docs/USER_GUIDE.md`):
  - Step-by-step walkthrough: Import network → view metrics → filter/explore
  - Glossary of network terms (centrality, community, hub, etc.)
  - FAQ: Common patterns and troubleshooting
- [x] **API Documentation** (`docs/API.md`):
  - OpenAPI spec (Swagger) with interactive explorer
  - cURL examples, response schemas, error codes
- [x] **Developer Guide** (`docs/DEVELOPER.md`):
  - Architecture overview and design decisions
  - How to extend metrics, add new formats, contribute
- [x] **Demo & Example Datasets**:
  - 3 real biological networks (e.g., yeast protein interaction, human disease network, pathway)
  - Jupyter Notebook walkthrough
- **Acceptance Criteria**: All docs peer-reviewed by mentors; at least one external user can follow guide independently

**Deliverable 3d: AI-Assisted Insights (Optional Enhancement)**
- [x] Heuristic-based pattern identification:
  - "Hub nodes" detected by degree >90th percentile
  - "Bottleneck nodes" identified by betweenness centrality
  - "Potential drug targets" flagged (high degree + high betweenness)
- [x] Automated insights summary: "Your network contains X communities; the largest hub is node Y with Z connections"
- [x] Suggestions: "Try filtering by community ID=3 to see coexpressed genes"
- **Acceptance Criteria**: Insights generated automatically and displayed on dashboard; at least 1 mentor validation

**Deliverable 3e: Community Handoff**
- [x] Contribute feature branch to NRNB organization (if applicable)
- [x] Prepare transition documentation for future maintainers
- [x] Record 10-minute demo video walkthrough
- [x] Write GSoC final report with lessons learned
- **Acceptance Criteria**: Code merged/ready for review; demo available; report completed

---

### Out of Scope (Explicitly)

To maintain focus, the following are **NOT** included:

- ❌ Multi-user collaboration / real-time co-editing
- ❌ Integration with specific external databases (e.g., String DB, BioGRID) — API contracts defined but not implemented
- ❌ Advanced ML-based clustering or anomaly detection (simple heuristics only)
- ❌ Mobile app (web-responsive design only)
- ❌ Publication-grade figure export (SVG export; polishing left to user)

---

## Section 4: Technical Approach

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ UI Components                                            │  │
│  │ ├─ FileUpload (drag-and-drop)                           │  │
│  │ ├─ NetworkVisualization (Cytoscape.js + custom styling)│  │
│  │ ├─ FilterPanel (centrality, degree, community, weight) │  │
│  │ ├─ MetricsDisplay (table + legend)                     │  │
│  │ └─ ExportModal (JSON, SVG, Cytoscape format)           │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ State Management (Redux Toolkit)                        │  │
│  │ ├─ networkSlice (loaded network, parsed nodes/edges)   │  │
│  │ ├─ metricsSlice (cached centrality calculations)       │  │
│  │ ├─ filterSlice (active filters)                        │  │
│  │ └─ uiSlice (selected nodes, tooltips, theme)           │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ API Client (Axios + React Query)                        │  │
│  │ └─ Handles requests, caching, retry logic              │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────┬───────────────────────┘
                                           │ REST API
┌──────────────────────────────────────────┴───────────────────────┐
│                   Backend (Flask + Python)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ API Routes (Flask Blueprints)                           │  │
│  │ ├─ /api/upload (POST)                                  │  │
│  │ ├─ /api/networks (GET/DELETE)                          │  │
│  │ ├─ /api/metrics (POST)                                 │  │
│  │ ├─ /api/communities (POST)                             │  │
│  │ └─ /api/export (POST)                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Core Services (Python modules)                          │  │
│  │ ├─ FileParser (SIF, JSON, TSV/CSV → NetworkX Graph)    │  │
│  │ ├─ MetricsCalc (NetworkX-based centrality engine)      │  │
│  │ ├─ CommunityDetector (Louvain algorithm)               │  │
│  │ ├─ Exporter (to Cytoscape, SVG, JSON)                 │  │
│  │ └─ InsightGenerator (heuristic-based analysis)         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Data Layer (SQLAlchemy ORM)                             │  │
│  │ └─ Models: Network, Node, Edge (caching for performance)│  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
   ┌────────────────┐                      ┌────────────────┐
   │ PostgreSQL     │                      │ Redis (Cache)  │
   │ (Storage)      │                      │ (Metrics)      │
   └────────────────┘                      └────────────────┘
```

### Technology Stack

| Layer | Technology | Justification |
|-------|-----------|--------------|
| **Frontend Framework** | React 18 + TypeScript | Type safety, component reusability, large ecosystem |
| **Visualization** | Cytoscape.js | Purpose-built for biological networks, Cytoscape ecosystem integration |
| **State Management** | Redux Toolkit | Centralized state, easy testing, DevTools integration |
| **Backend Framework** | Flask + Blueprints | Lightweight, pythonic, easy to extend with scientific libraries |
| **Graph Processing** | NetworkX | Industry standard for network analysis, well-documented |
| **Community Detection** | python-louvain | Efficient modularity optimization, proven accuracy |
| **Database** | PostgreSQL (prod) / SQLite (dev) | Reliable, ACID compliance, relationship modeling |
| **Caching** | Redis | Fast metric lookup, session management |
| **API Documentation** | FastAPI/Swagger (or Flask-RESTX) | Auto-generated OpenAPI spec, interactive explorer |
| **Testing** | pytest (backend), Jest + React Testing Library (frontend) | Industry standard, good coverage reporting |
| **Deployment** | Docker + Docker Compose (dev); TBD with mentors (prod) | Reproducibility, easy collaboration, cloud-ready |

### Data Flow Example: "Calculate Betweenness Centrality"

```
1. User uploads network file (.sif)
   ↓
2. Frontend sends: POST /api/upload { file: <binary> }
   ↓
3. Backend:
   ├─ Receives file in /tmp/
   ├─ FileParser.parse_sif() → NetworkX Graph object
   ├─ Validate: Check for isolated nodes, self-loops
   ├─ Store in database: INSERT INTO networks; INSERT INTO nodes/edges
   └─ Return: { network_id: "abc123", node_count: 512, edge_count: 1024 }
   ↓
4. Frontend displays network with default layout (force-directed)
   ↓
5. User clicks "Calculate Metrics" button
   ↓
6. Frontend sends: POST /api/networks/abc123/metrics { metrics: ["betweenness", "degree"] }
   ↓
7. Backend:
   ├─ Check Redis cache: if metrics already calculated → skip, return cached
   ├─ Load Graph from database
   ├─ MetricsCalc.calculate_betweenness() using NetworkX
   ├─ Store results in Redis with 24h TTL
   ├─ Return: { nodes: [{id: "geneA", betweenness: 0.45, degree: 12}, ...] }
   ↓
8. Frontend:
   ├─ Redux: update metricsSlice with returned data
   ├─ Re-render: Node sizes scale by betweenness; colors by degree
   ├─ Display legend and tooltip info
   ↓
9. User sees updated visualization in <1s
```

### Algorithm Details

**Centrality Calculations** (all via NetworkX):
```python
# Pseudo-code
def calculate_centrality(graph: nx.Graph, measure: str) -> dict:
    if measure == "degree":
        return nx.degree_centrality(graph)  # O(V + E)
    elif measure == "betweenness":
        return nx.betweenness_centrality(graph)  # O(V * (V + E))
    elif measure == "closeness":
        return nx.closeness_centrality(graph)  # O(V^2)
    elif measure == "eigenvector":
        return nx.eigenvector_centrality(graph)  # O(V) iterations
    elif measure == "pagerank":
        return nx.pagerank(graph)  # Custom damping factor = 0.85
```

**Community Detection** (Louvain):
```python
# python-louvain library wraps C implementation
from community import community_louvain

communities = community_louvain.best_partition(graph, randomize=False)
# Returns: {node_id: community_id, ...}
# Modularity Q typically 0.4–0.6 for biological networks
```

### Performance Considerations

- **Frontend Optimization**:
  - Virtual scrolling for large metrics tables (1000+ rows)
  - Cytoscape.js GPU acceleration for rendering
  - Lazy-load edge data (fetch on demand if 10k+ edges)

- **Backend Optimization**:
  - Pre-compute and cache metrics on upload
  - Use NetworkX SparseGraph for 5000+ node networks
  - Connection pooling for database queries
  - Batch processing for bulk metric calculations

- **Scalability Target**: 
  - Support networks up to 10,000 nodes
  - API response time: <500ms for metric calculation
  - Memory: <1GB per 5000-node network

---

## Section 5: Timeline & Milestones

### Community Bonding Period (May 1–24, 2026) — 3 Weeks

**Week 1: Environment & Discovery**
- [ ] Set up local development environment (Docker, VSCode, Git workflow)
- [ ] Read NRNB documentation: Cytoscape plugins, NDEx, existing network tools
- [ ] Complete 1-2 online courses: Graph algorithms (Coursera), Network analysis fundamentals
- [ ] Schedule 1st mentor meeting: Confirm technical approach, tool selections, timeline adjustments

**Week 2: Domain Learning & Planning**
- [ ] Study 3 real biological networks (structure, sizes, use cases)
- [ ] Read 2–3 key papers on network analysis in biology (_e.g._, centrality in PPI networks)
- [ ] Create detailed technical specification with mentors (data models, API contracts)
- [ ] Set up Git repository structure and CI/CD pipeline skeleton

**Week 3: Preparation & Kickoff**
- [ ] Prepare development environment documentation
- [ ] Create project management board (GitHub Projects / Trello)
- [ ] Identify 5 test datasets (varying sizes: 50, 500, 1000, 5000, 10000 nodes)
- [ ] Hold kick-off meeting with mentors + project team (if multi-mentor)

---

### Coding Phase: Weeks 1–12 (May 27 – August 15, 2026)

#### **Phase 1: Foundation (Weeks 1–4)** ← Code Freeze Date: June 23

| Week | Frontend | Backend | DevOps / Docs | Milestones |
|------|----------|---------|---------------|-----------|
| **W1** | React + Redux setup; FileUpload component | Flask app skeleton; PostgreSQL schema design | GitHub Actions CI/CD | 🎯 Repo ready; basic app structure running |
| **W2** | Cytoscape.js integration; basic node/edge rendering | FileParser (SIF + JSON formats); API /upload + /networks | Docker Compose working | 🎯 Can load test network; visualization works |
| **W3** | Pan/zoom/selection interactions; styling | Database ORM setup; validate & store parsed networks | Unit tests start | 🎯 Interactive canvas; basic filtering |
| **W4** | Metrics display component (table); legend | Endpoint tests; API documentation (Swagger stub) | Accessibility review | 🎯 **MIDPOINT 1**: Visualize + parse + API working |

**Phase 1 Code Review**: Mentor review of architecture; confirm design patterns

---

#### **Phase 2: Analysis & Interaction (Weeks 5–8)** ← Midterm Evaluation Date: July 21, 2026

| Week | Frontend | Backend | DevOps / Docs | Milestones |
|------|----------|---------|---------------|-----------|
| **W5** | Filter UI Panel (centrality, degree sliders) | MetricsCalc (degree, betweenness, closeness) | Performance profiling start | 🎯 Centrality calculations working |
| **W6** | Implement filtering logic; highlight filtered nodes | Eigenvector + PageRank; metrics caching (Redis) | API endpoint tests; cURL examples | 🎯 All 5 metrics calculated |
| **W7** | Community color coding; node tooltips | CommunityDetector (Louvain); community export | Load testing (100 concurrent requests) | 🎯 Communities detected & visualized |
| **W8** | Subgraph extraction UI; export buttons | Export service (JSON, Cytoscape, SVG); API endpoints | **MIDTERM REPORT**; docs review | 🎯 **MIDTERM COMPLETE**: Full analysis pipeline |

**Midterm Evaluation**: Demo to mentors; performance metrics reviewed; feedback incorporated

---

#### **Phase 3: Polish & Optimization (Weeks 9–12)** ← Final Submission Date: August 15, 2026

| Week | Frontend | Backend | Testing & Docs | Milestones |
|------|----------|---------|----------------|-----------|
| **W9** | Performance optimization (virtual scrolling; lazy-load) | Backend optimization (caching; DB indexing) | Unit test coverage audit (70%+ goal) | 🎯 Performance target: <2s for 1000 nodes |
| **W10** | Accessibility fixes (keyboard nav; WCAG AA) | InsightGenerator (hub detection heuristics) | Integration tests; accessibility audit | 🎯 WCAG 2.1 AA compliant |
| **W11** | Bug fixes; user feedback iteration | API finalization; rate limiting | Comprehensive docs (User guide, API, Developer) | 🎯 All tests passing; >70% coverage |
| **W12** | Final polish; demo prep | Code cleanup; transition docs | Demo video; final report; community handoff | 🎯 **PROJECT COMPLETE**: Ready for release |

**Final Evaluation** (August 22, 2026): Demo to mentors, code review, final feedback

---

### Risk Mitigation & Contingencies

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Underestimating biological domain knowledge | Medium | Medium | Start domain learning in bonding period; weekly mentor check-ins |
| Performance bottlenecks with large networks | Medium | High | Early load testing (week 4); consider GraphQL if REST proves slow |
| Cytoscape.js rendering limits on 10k nodes | Low | High | Fall back to canvas-based rendering or WebGL if needed; pre-identify threshold |
| Scope creep (adding too many features) | Medium | High | Strict scope review at midterm; defer "nice-to-haves" to post-GSoC |
| Mentor availability conflicts | Low | Medium | Establish async communication channel (Slack/Discord); record meetings |

---

## Section 6: Success Metrics & Evaluation

### Code Quality Metrics

- [ ] **Test Coverage**: ≥70% (backend + frontend combined)
  - Measured with: pytest-cov (backend), Jest coverage (frontend)
  - Acceptance: Report visible in CI/CD; no regression

- [ ] **Performance Benchmarks**:
  - Graph rendering: 1000-node network in <2 seconds
  - Centrality calculation: 5000-node network in <5 seconds
  - API response time: <500ms for 95th percentile
  - Memory usage: <1GB per 5000-node session

- [ ] **Code Standards**:
  - ESLint passes (frontend); pylint score >8/10 (backend)
  - Type coverage: 100% for new Python code; TS strict mode enabled
  - No high-severity security vulnerabilities (OWASP Top 10)

### User Experience Metrics

- [ ] **Accessibility**:
  - WCAG 2.1 AA compliance verified by axe-core audit
  - Keyboard navigation fully functional
  - Screen reader tested with NVDA/JAWS

- [ ] **Usability**:
  - New user can import network and view metrics in <5 minutes
  - Documentation is clear: 3+ external users successfully follow guide (beta testers)
  - No more than 2 bug reports from mentors during testing phase

### Domain-Specific Metrics

- [ ] **Biological Accuracy**:
  - Centrality scores match reference implementations (NetworkAnalyzer benchmark)
  - Community detection Q-score: >0.4 on standard test networks
  - Insights align with known biological properties (hubs ↔ essential genes)

- [ ] **Data Compatibility**:
  - Successfully import 5+ real biological networks (varying formats)
  - No data loss or corruption during parsing/export
  - Support for weighted edges and node attributes

### Community Contribution Metrics

- [ ] **Documentation**:
  - User guide + API reference + Developer onboarding doc
  - At least 10 code comments explaining non-obvious logic
  - One blog post or community writeup published

- [ ] **Open Source Readiness**:
  - README with clear setup instructions
  - Contributing guidelines and code of conduct
  - Feature branch ready for NRNB integration (if applicable)

---

## Section 7: Community Impact & Long-Term Vision

### Immediate Impact (GSoC '26)

1. **Onboarding New Researchers**: Reduce entry barrier for network analysis; enable wet-lab biologists to explore their own data
2. **NRNB Ecosystem Enhancement**: Complement Cytoscape with lightweight browser-based alternative; potential gateway to desktop tool
3. **Research Acceleration**: Researchers save hours on manual metric calculation; focus on biological interpretation
4. **Education**: Tool + documentation serve as teaching resource for network analysis courses

### Long-Term Vision (Post-GSoC)

- **Multi-user Collaboration**: Add shared workspaces for research teams
- **External Database Integration**: Connect to BioGRID, String DB, GeneMANIA for live data
- **Advanced ML Analytics**: Anomaly detection, predictive modeling for network perturbations
- **Publication Integration**: Direct export to journals with supplemental figure formatting
- **Mobile App**: Native iOS/Android app for field researchers
- **NRNB Tool Integration**: Formal plugin for Cytoscape; integration with NDEx platform

---

## Section 8: Why NRNB? Why Me?

### Alignment with NRNB Mission

NRNB's goal is to **democratize network-driven biomedical discovery**. NetworkInsight directly advances this mission by:
- Making network analysis accessible to non-computational researchers
- Providing modern, user-friendly interface to network concepts
- Integrating with existing NRNB tools (Cytoscape, NDEx) rather than replacing them
- Contributing open-source tools to the research community

### Why I Am a Good Fit

1. **Technical Foundation**: Full-stack development experience (React, Flask, Python); proven ability to ship features
2. **Domain Hunger**: New to bioinformatics, but have demonstrated self-teaching ability in ML, data visualization, and web development
3. **Communication**: Not afraid to ask questions and engage with mentors; documented learning path
4. **Commitment**: Dedicated 40 hours/week; no conflicting internships; located in India for timezone alignment with many mentors
5. **Open Source Mindset**: Active GitHub user; comfortable with collaborative development, code review, and iteration

---

## Section 9: Availability & Logistics

- **Time Commitment**: 40 hours/week (May 26 – August 22, 2026)
  - Breakdown: 25h coding, 10h learning/documentation, 5h communication with mentors
- **Timezone**: IST (UTC+5:30) – suitable overlap with US-based NRNB mentors
- **Holiday/Conflict**: No conflicting internships, courses, or commitments
- **Backup Communication**: Email (primary), Slack/Discord (secondary), weekly video calls
- **Sync Meetings**: Tuesday & Friday mornings (9 AM IST = 11:30 PM US EST) or TBD with mentors

---

## Section 10: Code Samples & Portfolio Links

### Relevant Portfolio Projects

1. **Personal Portfolio (React + TypeScript)**
   - Live: https://projects.gu-saurabh.site/about
   - Demonstrates: Modern React patterns, responsive design, performance optimization
   - Relevance: Frontend architecture similar to proposed project

2. **Email Spam Detection (Python + ML)**
   - Repo: Check GitHub profile (link provided in personal info)
   - Demonstrates: Python data pipeline, model evaluation, scientific computing
   - Relevance: Backend structure and Python ecosystem familiarity

3. **Admin Dashboard (React + APIs)**
   - Tech: React, Redux, Tailwind CSS, REST APIs
   - Demonstrates: Complex state management, data visualization, API integration
   - Relevance: Transferable UI patterns, filter/drill-down interactions

### Code Sample: Graph Parsing Logic (Python)

```python
# Simple example showing SIF parser structure
import networkx as nx

def parse_sif(file_path: str) -> nx.Graph:
    """Parse Simple Interaction Format (SIF) file."""
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                node1, interaction_type, *targets = parts
                for node2 in targets:
                    G.add_edge(node1, node2, interaction_type=interaction_type)
    return G

# Usage
network = parse_sif("protein_interactions.sif")
centrality = nx.betweenness_centrality(network)
```

---

## Section 11: AI Assistance Disclosure

This proposal was drafted with assistance from AI tools (Claude) for:
- Structural organization and formatting
- Technical terminology refinement
- Timeline planning and risk analysis organization

All project concepts, technical decisions, technical stack choices, and learning goals reflect my own research, project experience, and interpretation of NRNB's mission and existing tools. The proposal content—problem definition, deliverables, architecture, and biological network understanding—represents my genuine learning and design thinking, not AI generation.

---

## Section 12: Contact & Questions

**Primary Contact**: Saurabhtbj143@gmail.com  
**Secondary Contact**: +91 9798024301  
**GitHub**: https://github.com/SaurabhtBJ1201  
**Time Zone**: IST (UTC+5:30)  

I am available for pre-acceptance discussions about:
- Project scope refinement with mentors
- Tool selection validation
- Timeline adjustments based on organization needs
- Questions about my background or project approach

---

## Appendix A: References & Resources

### Biological Network Tools & Concepts
- [Cytoscape User Guide](https://cytoscape.org/)
- [NetworkX Documentation](https://networkx.org/)
- [NDEx Network Exchange](https://www.ndexbio.org/)
- ["Network Biology" (Barabasi & Oltvai, 2004)](https://www.nature.com/articles/nrm1635) – Foundational paper

### Technical References
- [React Documentation](https://react.dev/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Cytoscape.js Documentation](https://js.cytoscape.org/)
- [python-louvain GitHub](https://github.com/taynaud/python-louvain)

### Data Format Specifications
- [SIF Format Guide](https://cytoscape.org/wiki/spaces/cytoscape/pages/89161367/Network+file+formats)
- [GraphML Specification](http://graphml.graphdrawing.org/)
- [JSON Graph Format](https://github.com/jsongraph/json-graph-spec)

### GSoC Resources
- [GSoC Contributor Guide](https://summerofcode.withgoogle.com/help/student-rules)
- [NRNB GSoC Archive](https://nrnb.org/) – Past project examples

---

**Proposal Version**: 1.0  
**Last Updated**: March 19, 2026  
**Next Review**: Upon mentor assignment
