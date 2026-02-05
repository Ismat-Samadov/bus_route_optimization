"""
Network Analysis Module for Bus Transit Optimization
Computes topology, overlap, efficiency, and ecological impact metrics
"""

import json
import math
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import numpy as np


class TransitNetworkAnalyzer:
    """
    Comprehensive transit network analyzer for route optimization
    """

    def __init__(self, bus_details_path: str, stops_path: str):
        """Load transit network data"""
        with open(bus_details_path, 'r', encoding='utf-8') as f:
            self.buses = json.load(f)

        with open(stops_path, 'r', encoding='utf-8') as f:
            self.stops = json.load(f)

        self.stop_index = {stop['id']: stop for stop in self.stops}
        print(f"Loaded {len(self.buses)} bus routes and {len(self.stops)} stops")

    def _clean_coordinate(self, coord_str: str) -> float:
        """Clean coordinate string (remove commas used as thousand separators)"""
        if isinstance(coord_str, (int, float)):
            return float(coord_str)
        # Remove commas that might be used as thousand separators
        cleaned = str(coord_str).replace(',', '')
        return float(cleaned)

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great circle distance between two points in kilometers"""
        R = 6371  # Earth radius in kilometers

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    # ==================== NETWORK TOPOLOGY ANALYSIS ====================

    def build_stop_graph(self) -> Dict:
        """
        Build network graph from bus routes
        Returns stop connectivity, degree distribution, and hub identification
        """
        # Build adjacency list
        adjacency = defaultdict(set)
        stop_routes = defaultdict(set)  # Which routes serve each stop
        edge_routes = defaultdict(set)  # Which routes use each edge

        for bus in self.buses:
            bus_number = bus['number']

            for stop_seq in bus['stops']:
                stop_id = stop_seq['stopId']
                stop_routes[stop_id].add(bus_number)

            # Build edges from stop sequence
            for direction in [1, 2]:
                stops_in_direction = sorted(
                    [s for s in bus['stops'] if s['directionTypeId'] == direction],
                    key=lambda x: x['id']
                )

                for i in range(len(stops_in_direction) - 1):
                    from_stop = stops_in_direction[i]['stopId']
                    to_stop = stops_in_direction[i + 1]['stopId']

                    adjacency[from_stop].add(to_stop)
                    edge = tuple(sorted([from_stop, to_stop]))
                    edge_routes[edge].add(bus_number)

        # Compute degree distribution
        degrees = {stop_id: len(neighbors) for stop_id, neighbors in adjacency.items()}

        # Identify hubs (stops with high degree)
        mean_degree = np.mean(list(degrees.values()))
        std_degree = np.std(list(degrees.values()))
        hub_threshold = mean_degree + 1.5 * std_degree

        hubs = [
            {
                'stop_id': stop_id,
                'degree': degree,
                'routes_count': len(stop_routes[stop_id]),
                'routes': list(stop_routes[stop_id])
            }
            for stop_id, degree in degrees.items()
            if degree >= hub_threshold
        ]

        return {
            'adjacency': dict(adjacency),
            'degrees': degrees,
            'stop_routes': dict(stop_routes),
            'edge_routes': dict(edge_routes),
            'hubs': sorted(hubs, key=lambda x: x['degree'], reverse=True),
            'mean_degree': mean_degree,
            'max_degree': max(degrees.values()) if degrees else 0,
            'network_density': self._compute_network_density(adjacency)
        }

    def _compute_network_density(self, adjacency: Dict) -> float:
        """Compute network density (actual edges / possible edges)"""
        n_nodes = len(adjacency)
        if n_nodes <= 1:
            return 0.0

        actual_edges = sum(len(neighbors) for neighbors in adjacency.values()) / 2
        possible_edges = n_nodes * (n_nodes - 1) / 2

        return actual_edges / possible_edges if possible_edges > 0 else 0.0

    # ==================== ROUTE OVERLAP ANALYSIS ====================

    def analyze_route_overlap(self) -> Dict:
        """
        Detect overlapping route segments and quantify duplication
        """
        # Build edge-to-routes mapping
        edge_routes = defaultdict(set)
        route_edges = defaultdict(set)

        for bus in self.buses:
            bus_number = bus['number']

            for direction in [1, 2]:
                stops_in_direction = sorted(
                    [s for s in bus['stops'] if s['directionTypeId'] == direction],
                    key=lambda x: x['id']
                )

                for i in range(len(stops_in_direction) - 1):
                    from_stop = stops_in_direction[i]['stopId']
                    to_stop = stops_in_direction[i + 1]['stopId']

                    edge = tuple(sorted([from_stop, to_stop]))
                    edge_routes[edge].add(bus_number)
                    route_edges[bus_number].add(edge)

        # Compute overlap metrics
        overlapping_edges = {edge: routes for edge, routes in edge_routes.items() if len(routes) > 1}

        total_edges = len(edge_routes)
        overlapping_edge_count = len(overlapping_edges)
        overlap_percentage = (overlapping_edge_count / total_edges * 100) if total_edges > 0 else 0

        # Find highly duplicated corridors
        high_duplication_threshold = 5
        high_duplication_corridors = [
            {'edge': edge, 'routes': list(routes), 'duplication_factor': len(routes)}
            for edge, routes in overlapping_edges.items()
            if len(routes) >= high_duplication_threshold
        ]

        # Compute per-route duplication index
        route_duplication = {}
        for bus_number, edges in route_edges.items():
            duplicated_edges = sum(1 for edge in edges if len(edge_routes[edge]) > 1)
            duplication_index = (duplicated_edges / len(edges) * 100) if edges else 0
            route_duplication[bus_number] = duplication_index

        return {
            'total_edges': total_edges,
            'overlapping_edges': overlapping_edge_count,
            'overlap_percentage': overlap_percentage,
            'edge_routes': dict(edge_routes),
            'high_duplication_corridors': sorted(
                high_duplication_corridors,
                key=lambda x: x['duplication_factor'],
                reverse=True
            )[:20],
            'route_duplication_index': route_duplication,
            'avg_duplication_index': np.mean(list(route_duplication.values()))
        }

    # ==================== STOP SPACING ANALYSIS ====================

    def analyze_stop_spacing(self) -> Dict:
        """
        Compute inter-stop distances and identify spacing issues
        """
        route_spacings = {}
        all_spacings = []

        for bus in self.buses:
            bus_number = bus['number']
            spacings = []

            for direction in [1, 2]:
                stops_in_direction = sorted(
                    [s for s in bus['stops'] if s['directionTypeId'] == direction],
                    key=lambda x: x['id']
                )

                for i in range(len(stops_in_direction) - 1):
                    stop1 = stops_in_direction[i]['stop']
                    stop2 = stops_in_direction[i + 1]['stop']

                    distance = self.haversine_distance(
                        self._clean_coordinate(stop1['latitude']),
                        self._clean_coordinate(stop1['longitude']),
                        self._clean_coordinate(stop2['latitude']),
                        self._clean_coordinate(stop2['longitude'])
                    )

                    spacings.append(distance)
                    all_spacings.append(distance)

            if spacings:
                route_spacings[bus_number] = {
                    'mean_spacing': np.mean(spacings),
                    'min_spacing': np.min(spacings),
                    'max_spacing': np.max(spacings),
                    'std_spacing': np.std(spacings),
                    'spacings': spacings
                }

        # Identify overly dense stops (< 200m)
        dense_threshold = 0.2  # km
        overly_dense_count = sum(1 for s in all_spacings if s < dense_threshold)

        # Identify sparse stops (> 2km)
        sparse_threshold = 2.0  # km
        overly_sparse_count = sum(1 for s in all_spacings if s > sparse_threshold)

        return {
            'route_spacings': route_spacings,
            'network_mean_spacing': np.mean(all_spacings) if all_spacings else 0,
            'network_median_spacing': np.median(all_spacings) if all_spacings else 0,
            'overly_dense_segments': overly_dense_count,
            'overly_sparse_segments': overly_sparse_count,
            'dense_percentage': (overly_dense_count / len(all_spacings) * 100) if all_spacings else 0,
            'optimal_spacing_range': (0.3, 0.8),  # Industry standard: 300-800m
            'spacing_distribution': all_spacings
        }

    # ==================== RESOURCE WASTE INDICATORS ====================

    def compute_resource_waste_metrics(self, overlap_analysis: Dict) -> Dict:
        """
        Compute resource waste indicators based on network topology
        """
        # Compute total network vehicle-km
        total_vehicle_km = sum(bus.get('routLength', 0) for bus in self.buses)

        # Compute wasted vehicle-km due to overlap
        edge_routes = overlap_analysis['edge_routes']

        # Estimate km per edge (simplified)
        wasted_km = 0
        for edge, routes in edge_routes.items():
            if len(routes) > 1:
                # Get edge distance
                stop1_id, stop2_id = edge
                if stop1_id in self.stop_index and stop2_id in self.stop_index:
                    stop1 = self.stop_index[stop1_id]
                    stop2 = self.stop_index[stop2_id]

                    distance = self.haversine_distance(
                        self._clean_coordinate(stop1['latitude']),
                        self._clean_coordinate(stop1['longitude']),
                        self._clean_coordinate(stop2['latitude']),
                        self._clean_coordinate(stop2['longitude'])
                    )

                    # Wasted km = (n_routes - 1) * distance
                    wasted_km += (len(routes) - 1) * distance

        # Route efficiency: stops per km
        route_efficiency = []
        for bus in self.buses:
            route_length = bus.get('routLength', 0)
            stop_count = len(set(s['stopId'] for s in bus['stops']))

            if route_length > 0:
                efficiency = stop_count / route_length
                route_efficiency.append({
                    'route': bus['number'],
                    'stops_per_km': efficiency,
                    'route_length': route_length,
                    'stop_count': stop_count
                })

        return {
            'total_vehicle_km': total_vehicle_km,
            'wasted_vehicle_km': wasted_km,
            'waste_percentage': (wasted_km / total_vehicle_km * 100) if total_vehicle_km > 0 else 0,
            'route_efficiency': sorted(route_efficiency, key=lambda x: x['stops_per_km']),
            'network_redundancy_coefficient': overlap_analysis['avg_duplication_index'] / 100
        }

    # ==================== ECOLOGICAL IMPACT PROXIES ====================

    def estimate_ecological_impact(self, waste_metrics: Dict, overlap_analysis: Dict) -> Dict:
        """
        Estimate ecological impact proxies based on route characteristics

        Assumptions:
        - Average bus fuel consumption: 35 liters / 100 km
        - CO2 emission: 2.6 kg per liter of diesel
        - Overlap factor increases fuel consumption proportionally
        """
        FUEL_CONSUMPTION = 35  # liters per 100 km
        CO2_PER_LITER = 2.6  # kg

        total_km = waste_metrics['total_vehicle_km']
        wasted_km = waste_metrics['wasted_vehicle_km']

        # Base emissions
        base_fuel = (total_km / 100) * FUEL_CONSUMPTION
        base_co2 = base_fuel * CO2_PER_LITER

        # Wasted emissions
        wasted_fuel = (wasted_km / 100) * FUEL_CONSUMPTION
        wasted_co2 = wasted_fuel * CO2_PER_LITER

        # High inefficiency corridors (routes with >70% duplication)
        high_waste_routes = [
            route for route, dup_idx in overlap_analysis['route_duplication_index'].items()
            if dup_idx > 70
        ]

        return {
            'total_annual_co2_tons': base_co2 * 365 / 1000,  # Approximate annual
            'wasted_annual_co2_tons': wasted_co2 * 365 / 1000,
            'wasted_fuel_liters_annual': wasted_fuel * 365,
            'co2_reduction_potential_percent': (wasted_co2 / base_co2 * 100) if base_co2 > 0 else 0,
            'high_inefficiency_routes': high_waste_routes,
            'assumptions': {
                'fuel_consumption_l_per_100km': FUEL_CONSUMPTION,
                'co2_kg_per_liter': CO2_PER_LITER,
                'basis': 'Wasted vehicle-km from route overlap'
            }
        }

    # ==================== COMPREHENSIVE ANALYSIS ====================

    def run_full_analysis(self) -> Dict:
        """
        Execute comprehensive network analysis
        """
        print("\n=== Running Comprehensive Transit Network Analysis ===\n")

        print("1. Analyzing network topology...")
        topology = self.build_stop_graph()
        print(f"   ✓ Network density: {topology['network_density']:.4f}")
        print(f"   ✓ Identified {len(topology['hubs'])} hub stops")

        print("\n2. Analyzing route overlap...")
        overlap = self.analyze_route_overlap()
        print(f"   ✓ Overlap percentage: {overlap['overlap_percentage']:.2f}%")
        print(f"   ✓ High duplication corridors: {len(overlap['high_duplication_corridors'])}")

        print("\n3. Analyzing stop spacing...")
        spacing = self.analyze_stop_spacing()
        print(f"   ✓ Mean stop spacing: {spacing['network_mean_spacing']:.3f} km")
        print(f"   ✓ Overly dense segments: {spacing['overly_dense_segments']}")

        print("\n4. Computing resource waste metrics...")
        waste = self.compute_resource_waste_metrics(overlap)
        print(f"   ✓ Total vehicle-km: {waste['total_vehicle_km']:.2f}")
        print(f"   ✓ Wasted vehicle-km: {waste['wasted_vehicle_km']:.2f} ({waste['waste_percentage']:.2f}%)")

        print("\n5. Estimating ecological impact...")
        ecology = self.estimate_ecological_impact(waste, overlap)
        print(f"   ✓ CO2 reduction potential: {ecology['co2_reduction_potential_percent']:.2f}%")
        print(f"   ✓ Potential annual CO2 savings: {ecology['wasted_annual_co2_tons']:.2f} tons")

        print("\n=== Analysis Complete ===\n")

        return {
            'topology': topology,
            'overlap': overlap,
            'spacing': spacing,
            'waste': waste,
            'ecology': ecology,
            'summary': {
                'total_routes': len(self.buses),
                'total_stops': len(self.stops),
                'network_efficiency_score': self._compute_efficiency_score(topology, overlap, spacing, waste)
            }
        }

    def _compute_efficiency_score(self, topology: Dict, overlap: Dict, spacing: Dict, waste: Dict) -> float:
        """
        Compute overall network efficiency score (0-100)
        Higher is better
        """
        # Penalize high overlap
        overlap_score = 100 - overlap['overlap_percentage']

        # Penalize resource waste
        waste_score = 100 - waste['waste_percentage']

        # Penalize poor stop spacing
        dense_penalty = spacing['dense_percentage']
        spacing_score = 100 - dense_penalty

        # Weighted average
        efficiency_score = (
            0.4 * overlap_score +
            0.4 * waste_score +
            0.2 * spacing_score
        )

        return max(0, min(100, efficiency_score))


if __name__ == "__main__":
    analyzer = TransitNetworkAnalyzer(
        'data/busDetails.json',
        'data/stops.json'
    )

    results = analyzer.run_full_analysis()

    # Save results
    with open('data/analysis_results.json', 'w', encoding='utf-8') as f:
        # Convert sets to lists for JSON serialization
        import copy

        def convert_for_json(obj):
            """Recursively convert objects for JSON serialization"""
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, tuple):
                return list(obj)
            elif isinstance(obj, dict):
                # Convert tuple keys to strings
                return {
                    str(key) if isinstance(key, tuple) else key: convert_for_json(value)
                    for key, value in obj.items()
                }
            elif isinstance(obj, list):
                return [convert_for_json(item) for item in obj]
            else:
                return obj

        results_copy = convert_for_json(results)
        json.dump(results_copy, f, indent=2, ensure_ascii=False)

    print(f"Analysis results saved to data/analysis_results.json")
    print(f"Network Efficiency Score: {results['summary']['network_efficiency_score']:.2f}/100")
