# network_analysis.py

## Overview
Comprehensive transit network analysis module that computes topology metrics, route overlap, stop spacing efficiency, resource waste indicators, and ecological impact proxies for bus route optimization.

## Purpose
This script performs graph-theoretic network analysis to quantify transit system inefficiencies and identify optimization opportunities without relying on ridership data or demand estimates.

## Usage

### Basic Usage
```bash
python scripts/network_analysis.py
```

### Expected Output
```
Loaded 208 bus routes and 3841 stops

=== Running Comprehensive Transit Network Analysis ===

1. Analyzing network topology...
   ✓ Network density: 0.0004
   ✓ Identified 239 hub stops

2. Analyzing route overlap...
   ✓ Overlap percentage: 46.84%
   ✓ High duplication corridors: 20

3. Analyzing stop spacing...
   ✓ Mean stop spacing: 10.339 km
   ✓ Overly dense segments: 1014

4. Computing resource waste metrics...
   ✓ Total vehicle-km: 7745.44
   ✓ Wasted vehicle-km: 3244.91 (41.89%)

5. Estimating ecological impact...
   ✓ CO2 reduction potential: 41.89%
   ✓ Potential annual CO2 savings: 1077.80 tons

=== Analysis Complete ===

Analysis results saved to data/analysis_results.json
Network Efficiency Score: 62.73/100
```

## Output
- **File**: `data/analysis_results.json`
- **Format**: JSON object with comprehensive analysis results
- **Size**: Variable based on network complexity

---

## Core Components

### 1. TransitNetworkAnalyzer Class

Main analysis engine with the following capabilities:

#### Initialization
```python
analyzer = TransitNetworkAnalyzer(
    'data/busDetails.json',
    'data/stops.json'
)
```

Loads transit data and builds stop index for efficient lookups.

---

## Analysis Modules

### 1. Network Topology Analysis

#### `build_stop_graph()` → Dict

Constructs graph representation of the transit network.

**Returns:**
- `adjacency`: Stop connectivity graph (adjacency list)
- `degrees`: Node degree distribution
- `stop_routes`: Routes serving each stop
- `edge_routes`: Routes using each edge
- `hubs`: High-degree stops (connectivity > mean + 1.5σ)
- `mean_degree`: Average node connectivity
- `max_degree`: Maximum connectivity
- `network_density`: Actual edges / possible edges

**Methodology:**
- Builds directed graph from route stop sequences
- Computes degree distribution
- Identifies hub stops using statistical threshold
- Calculates network density metric

**Use Cases:**
- Hub stop identification for infrastructure investment
- Bottleneck detection
- Transfer opportunity analysis
- Network resilience assessment

---

### 2. Route Overlap Analysis

#### `analyze_route_overlap()` → Dict

Detects and quantifies route segment duplication.

**Returns:**
- `total_edges`: Total unique route segments
- `overlapping_edges`: Segments served by multiple routes
- `overlap_percentage`: System-wide duplication rate
- `edge_routes`: Routes serving each segment
- `high_duplication_corridors`: Segments with ≥5 overlapping routes
- `route_duplication_index`: Per-route duplication percentage
- `avg_duplication_index`: Network-wide average

**Methodology:**
- Extracts route segments from stop sequences
- Maps segments to serving routes
- Counts routes per segment
- Computes per-route and system-wide duplication metrics

**Use Cases:**
- Corridor consolidation planning
- Route merger identification
- Resource reallocation analysis
- Service redundancy assessment

**Example High-Duplication Corridor:**
```json
{
  "edge": [1234, 5678],
  "routes": ["1", "5", "18", "22", "45", "50", "67", "120"],
  "duplication_factor": 8
}
```

---

### 3. Stop Spacing Analysis

#### `analyze_stop_spacing()` → Dict

Computes inter-stop distances and identifies spacing inefficiencies.

**Returns:**
- `route_spacings`: Per-route spacing statistics
- `network_mean_spacing`: Average across all segments
- `network_median_spacing`: Median spacing
- `overly_dense_segments`: Count of segments < 200m
- `overly_sparse_segments`: Count of segments > 2km
- `dense_percentage`: Percentage of overly dense segments
- `optimal_spacing_range`: Industry standard (0.3-0.8 km)
- `spacing_distribution`: Complete distribution data

**Methodology:**
- Haversine distance calculation between consecutive stops
- Statistical analysis of spacing distribution
- Comparison to industry standards

**Optimal Spacing Benchmarks:**
- **Urban Transit:** 300-800m
- **Trunk/BRT Lines:** 600-1000m
- **Local Service:** 400-600m

**Use Cases:**
- Stop consolidation planning
- Travel time optimization
- Operational speed improvement
- Accessibility vs efficiency trade-off analysis

---

### 4. Resource Waste Metrics

#### `compute_resource_waste_metrics(overlap_analysis)` → Dict

Quantifies operational inefficiencies based on network structure.

**Returns:**
- `total_vehicle_km`: Total daily network capacity
- `wasted_vehicle_km`: Capacity consumed by duplication
- `waste_percentage`: System-wide waste rate
- `route_efficiency`: Stops per km by route
- `network_redundancy_coefficient`: Average duplication factor

**Methodology:**
- Calculates wasted vehicle-km from overlapping segments
- Computes route efficiency ratios (stops/km)
- Derives network redundancy coefficient

**Financial Proxy:**
```
Assuming $3.50/vehicle-km operating cost:
- Total daily cost = vehicle_km × $3.50
- Wasted cost = wasted_vehicle_km × $3.50
- Annual waste = wasted_cost × 365 days
```

**Use Cases:**
- Budget optimization
- Route efficiency benchmarking
- Cost-benefit analysis for restructuring
- Operational performance monitoring

---

### 5. Ecological Impact Estimation

#### `estimate_ecological_impact(waste_metrics, overlap_analysis)` → Dict

Estimates environmental costs of network inefficiency.

**Returns:**
- `total_annual_co2_tons`: Baseline network emissions
- `wasted_annual_co2_tons`: Avoidable emissions
- `wasted_fuel_liters_annual`: Excess fuel consumption
- `co2_reduction_potential_percent`: Optimization opportunity
- `high_inefficiency_routes`: Routes with >70% duplication
- `assumptions`: Documented calculation basis

**Assumptions (Industry Standard):**
- **Fuel Consumption:** 35 liters per 100 km (diesel bus)
- **CO₂ Emission Factor:** 2.6 kg per liter diesel
- **Analysis Basis:** Wasted vehicle-km from route overlap

**Calculation:**
```
Base fuel = (total_km / 100) × 35 L
Base CO₂ = base_fuel × 2.6 kg

Wasted fuel = (wasted_km / 100) × 35 L
Wasted CO₂ = wasted_fuel × 2.6 kg

Annual emissions = daily CO₂ × 365
```

**Use Cases:**
- Climate action planning
- Environmental impact assessment
- Sustainability reporting
- Green financing applications
- Carbon credit quantification

---

### 6. Comprehensive Analysis Orchestration

#### `run_full_analysis()` → Dict

Executes all analysis modules and computes efficiency score.

**Returns:**
```json
{
  "topology": { /* topology metrics */ },
  "overlap": { /* overlap analysis */ },
  "spacing": { /* spacing analysis */ },
  "waste": { /* resource waste */ },
  "ecology": { /* ecological impact */ },
  "summary": {
    "total_routes": 208,
    "total_stops": 3841,
    "network_efficiency_score": 62.73
  }
}
```

**Network Efficiency Score Calculation:**
```
Overlap score = 100 - overlap_percentage
Waste score = 100 - waste_percentage
Spacing score = 100 - dense_percentage

Efficiency = 0.4×overlap + 0.4×waste + 0.2×spacing

Range: 0-100 (higher is better)
Interpretation:
  - 80-100: Excellent
  - 70-80: Good
  - 60-70: Fair (requires intervention)
  - <60: Poor (urgent action needed)
```

---

## Utility Functions

### `haversine_distance(lat1, lon1, lat2, lon2)` → float

Calculates great circle distance between two points.

**Parameters:**
- `lat1, lon1`: First point coordinates
- `lat2, lon2`: Second point coordinates

**Returns:**
- Distance in kilometers

**Formula:** Standard haversine formula for spherical earth

---

### `_clean_coordinate(coord_str)` → float

Cleans coordinate strings (removes commas used as thousand separators).

**Parameters:**
- `coord_str`: Coordinate as string or numeric

**Returns:**
- Cleaned float value

**Use:** Handles various coordinate format inconsistencies in source data

---

### `_compute_network_density(adjacency)` → float

Computes graph density (connectivity metric).

**Formula:**
```
density = actual_edges / possible_edges
where possible_edges = n(n-1)/2
```

**Interpretation:**
- 0.0: Completely disconnected
- 1.0: Fully connected (every node connected to every other)
- Typical transit networks: 0.0001-0.001 (sparse by design)

---

### `_compute_efficiency_score(topology, overlap, spacing, waste)` → float

Combines component scores into overall network efficiency metric.

**Weighting:**
- Route overlap: 40%
- Resource waste: 40%
- Stop spacing: 20%

---

## Dependencies

```python
import json
import math
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import numpy as np
```

### Installation
```bash
pip install numpy
```

---

## Output Data Structure

### Saved to `data/analysis_results.json`

```json
{
  "topology": {
    "adjacency": { "stop_id": ["connected_stops"] },
    "degrees": { "stop_id": degree },
    "stop_routes": { "stop_id": ["route_numbers"] },
    "edge_routes": { "[stop1, stop2]": ["routes"] },
    "hubs": [
      {
        "stop_id": 1234,
        "degree": 45,
        "routes_count": 18,
        "routes": ["1", "5", "22"]
      }
    ],
    "mean_degree": 2.34,
    "max_degree": 45,
    "network_density": 0.0004
  },
  "overlap": {
    "total_edges": 6382,
    "overlapping_edges": 2990,
    "overlap_percentage": 46.84,
    "high_duplication_corridors": [ /* ... */ ],
    "route_duplication_index": { "route_number": percentage },
    "avg_duplication_index": 43.53
  },
  "spacing": {
    "route_spacings": { /* per-route stats */ },
    "network_mean_spacing": 10.339,
    "network_median_spacing": 0.45,
    "overly_dense_segments": 1014,
    "overly_sparse_segments": 123,
    "dense_percentage": 18.5,
    "spacing_distribution": [ /* all spacings */ ]
  },
  "waste": {
    "total_vehicle_km": 7745.44,
    "wasted_vehicle_km": 3244.91,
    "waste_percentage": 41.89,
    "route_efficiency": [ /* stops/km by route */ ],
    "network_redundancy_coefficient": 0.44
  },
  "ecology": {
    "total_annual_co2_tons": 2573.0,
    "wasted_annual_co2_tons": 1077.8,
    "wasted_fuel_liters_annual": 348000,
    "co2_reduction_potential_percent": 41.89,
    "high_inefficiency_routes": ["1", "5", "22"],
    "assumptions": { /* documented */ }
  },
  "summary": {
    "total_routes": 208,
    "total_stops": 3841,
    "network_efficiency_score": 62.73
  }
}
```

---

## Use Cases

### 1. Network Optimization Planning
- Identify high-duplication corridors for consolidation
- Target routes for merger or elimination
- Prioritize stop consolidation locations

### 2. Budget Justification
- Quantify financial waste from inefficiency
- Project cost savings from optimization
- Support capital investment proposals

### 3. Environmental Policy
- Document carbon reduction potential
- Support climate action commitments
- Quantify sustainability improvements

### 4. Performance Monitoring
- Track network efficiency over time
- Benchmark against targets
- Measure optimization program impact

### 5. Strategic Planning
- Evidence base for trunk-feeder restructuring
- Hub infrastructure investment prioritization
- Long-term network evolution guidance

---

## Integration Example

```python
from scripts.network_analysis import TransitNetworkAnalyzer

# Initialize analyzer
analyzer = TransitNetworkAnalyzer(
    'data/busDetails.json',
    'data/stops.json'
)

# Run complete analysis
results = analyzer.run_full_analysis()

# Access specific metrics
efficiency_score = results['summary']['network_efficiency_score']
overlap_pct = results['overlap']['overlap_percentage']
wasted_km = results['waste']['wasted_vehicle_km']
co2_savings = results['ecology']['wasted_annual_co2_tons']

# Identify priority corridors
high_dup_corridors = results['overlap']['high_duplication_corridors']
for corridor in high_dup_corridors[:5]:
    print(f"Corridor: {corridor['edge']}")
    print(f"  Duplication: {corridor['duplication_factor']} routes")
    print(f"  Routes: {', '.join(corridor['routes'])}")

# Find hub stops for infrastructure investment
hubs = results['topology']['hubs'][:15]
for hub in hubs:
    print(f"Stop {hub['stop_id']}: {hub['routes_count']} routes")
```

---

## Performance

- **Processing Time:** 10-30 seconds (depends on network size)
- **Memory Usage:** ~100-200 MB (for 200 routes, 4000 stops)
- **Output Size:** 5-15 MB JSON file

---

## Limitations & Assumptions

**No Ridership Data:**
- Analysis based purely on network topology and geometry
- Cannot assess passenger demand or volume
- Assumes geographic coverage is proxy for service quality

**Ecological Proxies:**
- CO₂ estimates use industry-standard emission factors
- Actual emissions depend on fleet composition, driving patterns
- Conservative estimates (likely understate actual impact)

**Financial Proxies:**
- Operating cost estimates use industry averages
- Local costs may vary significantly
- Does not account for peak/off-peak variations

**Data Quality:**
- Dependent on accuracy of source data (API)
- Coordinate cleaning handles known format issues
- Some bus routes may have incomplete data

---

## Related Files

- **Input Data:**
  - `data/busDetails.json` — Route and stop data (from `busDetails.py`)
  - `data/stops.json` — Stop locations (from `stops.py`)

- **Output Data:**
  - `data/analysis_results.json` — Complete analysis results

- **Visualization:**
  - `scripts/generate_charts.py` — Creates visualizations from results

- **Documentation:**
  - `docs/route_network_optimization.md` — Strategic route analysis
  - `docs/stop_infrastructure_optimization.md` — Strategic stop analysis

---

## Notes

- All assumptions are explicitly documented in output
- Analysis is fully reproducible given same input data
- Results saved to JSON for use by other tools/scripts
- Designed for policy-level decision support, not operational planning
- Metrics are comparative (good for before/after, benchmarking)

---

**For detailed strategic recommendations based on these metrics, see:**
- `docs/route_network_optimization.md`
- `docs/stop_infrastructure_optimization.md`
- `README.md` (executive summary)
