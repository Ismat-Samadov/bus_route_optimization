"""
Chart Generation Script for Transit Network Analysis
Generates comprehensive visualizations for strategic optimization report
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter

# Use non-interactive backend
matplotlib.use('Agg')

# Set publication-quality parameters
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13


class ChartGenerator:
    """
    Generate comprehensive transit network visualizations
    """

    def __init__(self, analysis_results_path: str, output_dir: str = 'charts'):
        """Load analysis results"""
        with open(analysis_results_path, 'r', encoding='utf-8') as f:
            self.results = json.load(f)

        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        print(f"Loaded analysis results from {analysis_results_path}")
        print(f"Charts will be saved to {output_dir}/\n")

    def generate_all_charts(self):
        """Generate all visualization charts"""
        print("=== Generating Charts ===\n")

        self.plot_network_degree_distribution()
        self.plot_route_overlap_analysis()
        self.plot_stop_spacing_distribution()
        self.plot_resource_waste_metrics()
        self.plot_route_efficiency_comparison()
        self.plot_ecological_impact()
        self.plot_high_duplication_corridors()
        self.plot_hub_stops_analysis()
        self.plot_network_efficiency_breakdown()
        self.plot_optimization_potential()

        print("\n=== All Charts Generated Successfully ===")

    def plot_network_degree_distribution(self):
        """Plot stop connectivity degree distribution"""
        degrees = list(self.results['topology']['degrees'].values())

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Histogram
        ax1.hist(degrees, bins=30, color='#2E86AB', alpha=0.7, edgecolor='black')
        ax1.axvline(np.mean(degrees), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(degrees):.1f}')
        ax1.axvline(np.median(degrees), color='orange', linestyle='--', linewidth=2, label=f'Median: {np.median(degrees):.1f}')
        ax1.set_xlabel('Node Degree (Connections)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Stop Connectivity Distribution')
        ax1.legend()
        ax1.grid(alpha=0.3)

        # Top connected stops
        top_hubs = sorted(self.results['topology']['hubs'], key=lambda x: x['degree'], reverse=True)[:10]
        hub_degrees = [h['degree'] for h in top_hubs]
        hub_labels = [f"Stop {h['stop_id']}" for h in top_hubs]

        ax2.barh(range(len(hub_degrees)), hub_degrees, color='#A23B72', alpha=0.7)
        ax2.set_yticks(range(len(hub_degrees)))
        ax2.set_yticklabels(hub_labels)
        ax2.set_xlabel('Degree (Number of Connections)')
        ax2.set_title('Top 10 Hub Stops by Connectivity')
        ax2.grid(axis='x', alpha=0.3)
        ax2.invert_yaxis()

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/network_degree_distribution.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: network_degree_distribution.png")

    def plot_route_overlap_analysis(self):
        """Plot route overlap metrics"""
        overlap_data = self.results['overlap']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Overall overlap statistics
        categories = ['Unique\nSegments', 'Overlapping\nSegments']
        values = [
            overlap_data['total_edges'] - overlap_data['overlapping_edges'],
            overlap_data['overlapping_edges']
        ]
        colors = ['#2E86AB', '#F18F01']

        ax1.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Number of Route Segments')
        ax1.set_title(f"Network Overlap: {overlap_data['overlap_percentage']:.1f}% Duplicated")
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, v in enumerate(values):
            ax1.text(i, v + 20, str(v), ha='center', fontweight='bold')

        # Route duplication index distribution
        dup_indices = list(overlap_data['route_duplication_index'].values())

        ax2.hist(dup_indices, bins=20, color='#C73E1D', alpha=0.7, edgecolor='black')
        ax2.axvline(np.mean(dup_indices), color='blue', linestyle='--', linewidth=2,
                    label=f'Mean: {np.mean(dup_indices):.1f}%')
        ax2.set_xlabel('Route Duplication Index (%)')
        ax2.set_ylabel('Number of Routes')
        ax2.set_title('Route Duplication Distribution')
        ax2.legend()
        ax2.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/route_overlap_analysis.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: route_overlap_analysis.png")

    def plot_stop_spacing_distribution(self):
        """Plot stop spacing analysis"""
        spacing_data = self.results['spacing']
        all_spacings = spacing_data['spacing_distribution']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Spacing distribution histogram
        ax1.hist(all_spacings, bins=50, color='#06A77D', alpha=0.7, edgecolor='black')
        ax1.axvline(spacing_data['network_mean_spacing'], color='red', linestyle='--',
                    linewidth=2, label=f"Mean: {spacing_data['network_mean_spacing']:.2f} km")
        ax1.axvline(spacing_data['network_median_spacing'], color='orange', linestyle='--',
                    linewidth=2, label=f"Median: {spacing_data['network_median_spacing']:.2f} km")

        # Optimal range
        opt_min, opt_max = spacing_data['optimal_spacing_range']
        ax1.axvspan(opt_min, opt_max, alpha=0.2, color='green', label='Optimal Range')

        ax1.set_xlabel('Stop Spacing (km)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Inter-Stop Distance Distribution')
        ax1.legend()
        ax1.grid(alpha=0.3)
        ax1.set_xlim(0, 3)  # Focus on reasonable range

        # Spacing quality categories
        dense_count = spacing_data['overly_dense_segments']
        sparse_count = spacing_data['overly_sparse_segments']
        optimal_count = len(all_spacings) - dense_count - sparse_count

        categories = ['Too Dense\n(<0.2km)', 'Optimal\n(0.3-0.8km)', 'Too Sparse\n(>2km)']
        values = [dense_count, optimal_count, sparse_count]
        colors = ['#C73E1D', '#06A77D', '#F18F01']

        ax2.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Number of Segments')
        ax2.set_title('Stop Spacing Quality Assessment')
        ax2.grid(axis='y', alpha=0.3)

        # Add percentage labels
        total = sum(values)
        for i, v in enumerate(values):
            percentage = v / total * 100
            ax2.text(i, v + 20, f'{v}\n({percentage:.1f}%)', ha='center', fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/stop_spacing_distribution.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: stop_spacing_distribution.png")

    def plot_resource_waste_metrics(self):
        """Plot resource waste indicators"""
        waste_data = self.results['waste']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Vehicle-km waste
        total_km = waste_data['total_vehicle_km']
        wasted_km = waste_data['wasted_vehicle_km']
        efficient_km = total_km - wasted_km

        categories = ['Efficient\nOperation', 'Wasted Due\nto Overlap']
        values = [efficient_km, wasted_km]
        colors = ['#06A77D', '#C73E1D']

        ax1.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Vehicle-km')
        ax1.set_title(f"Resource Waste: {waste_data['waste_percentage']:.1f}% of Network Capacity")
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, v in enumerate(values):
            ax1.text(i, v + 50, f'{v:.0f} km', ha='center', fontweight='bold')

        # Route efficiency scatter
        efficiency_data = waste_data['route_efficiency']
        stops_per_km = [r['stops_per_km'] for r in efficiency_data]
        route_lengths = [r['route_length'] for r in efficiency_data]

        scatter = ax2.scatter(route_lengths, stops_per_km, alpha=0.6, c=stops_per_km,
                             cmap='RdYlGn', s=50, edgecolor='black', linewidth=0.5)
        ax2.set_xlabel('Route Length (km)')
        ax2.set_ylabel('Stops per km')
        ax2.set_title('Route Efficiency: Stop Density vs Length')
        ax2.grid(alpha=0.3)

        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax2)
        cbar.set_label('Stops per km', rotation=270, labelpad=15)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/resource_waste_metrics.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: resource_waste_metrics.png")

    def plot_route_efficiency_comparison(self):
        """Plot route efficiency comparison"""
        efficiency_data = self.results['waste']['route_efficiency']

        # Sort by efficiency
        sorted_routes = sorted(efficiency_data, key=lambda x: x['stops_per_km'])

        # Take top 15 most efficient and 15 least efficient
        least_efficient = sorted_routes[:15]
        most_efficient = sorted_routes[-15:]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Least efficient routes
        routes1 = [r['route'] for r in least_efficient]
        eff1 = [r['stops_per_km'] for r in least_efficient]

        ax1.barh(range(len(routes1)), eff1, color='#C73E1D', alpha=0.7, edgecolor='black')
        ax1.set_yticks(range(len(routes1)))
        ax1.set_yticklabels(routes1)
        ax1.set_xlabel('Stops per km (Lower = Less Efficient)')
        ax1.set_title('15 Least Efficient Routes\n(Candidates for Optimization)')
        ax1.grid(axis='x', alpha=0.3)
        ax1.invert_yaxis()

        # Most efficient routes
        routes2 = [r['route'] for r in most_efficient]
        eff2 = [r['stops_per_km'] for r in most_efficient]

        ax2.barh(range(len(routes2)), eff2, color='#06A77D', alpha=0.7, edgecolor='black')
        ax2.set_yticks(range(len(routes2)))
        ax2.set_yticklabels(routes2)
        ax2.set_xlabel('Stops per km (Higher = More Efficient)')
        ax2.set_title('15 Most Efficient Routes\n(Best Practice Examples)')
        ax2.grid(axis='x', alpha=0.3)
        ax2.invert_yaxis()

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/route_efficiency_comparison.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: route_efficiency_comparison.png")

    def plot_ecological_impact(self):
        """Plot ecological impact proxies"""
        ecology_data = self.results['ecology']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # CO2 emissions comparison
        total_co2 = ecology_data['total_annual_co2_tons']
        wasted_co2 = ecology_data['wasted_annual_co2_tons']
        optimized_co2 = total_co2 - wasted_co2

        scenarios = ['Current\nNetwork', 'After\nOptimization']
        current_values = [optimized_co2, wasted_co2]
        optimized_values = [optimized_co2, 0]

        x = np.arange(len(scenarios))
        width = 0.35

        # Stacked bars
        ax1.bar(scenarios[0], optimized_co2, width=0.5, label='Necessary Emissions',
                color='#2E86AB', alpha=0.7, edgecolor='black')
        ax1.bar(scenarios[0], wasted_co2, width=0.5, bottom=optimized_co2, label='Wasted Emissions',
                color='#C73E1D', alpha=0.7, edgecolor='black')
        ax1.bar(scenarios[1], optimized_co2, width=0.5, color='#06A77D', alpha=0.7, edgecolor='black')

        ax1.set_ylabel('Annual CO₂ Emissions (tons)')
        ax1.set_title(f'Emission Reduction Potential: {ecology_data["co2_reduction_potential_percent"]:.1f}%')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels
        ax1.text(0, total_co2 + 50, f'{total_co2:.0f} tons', ha='center', fontweight='bold')
        ax1.text(1, optimized_co2 + 50, f'{optimized_co2:.0f} tons\n(-{wasted_co2:.0f} tons)',
                ha='center', fontweight='bold', color='green')

        # Fuel consumption
        wasted_fuel = ecology_data['wasted_fuel_liters_annual']
        total_fuel = wasted_fuel / (ecology_data['co2_reduction_potential_percent'] / 100)
        optimized_fuel = total_fuel - wasted_fuel

        categories = ['Annual Fuel\nConsumption', 'Potential\nSavings']
        values = [total_fuel / 1000, wasted_fuel / 1000]  # Convert to thousands
        colors = ['#2E86AB', '#06A77D']

        ax2.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Fuel (thousands of liters)')
        ax2.set_title('Fuel Consumption and Savings Potential')
        ax2.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, v in enumerate(values):
            ax2.text(i, v + 10, f'{v:.0f}k L', ha='center', fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/ecological_impact.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: ecological_impact.png")

    def plot_high_duplication_corridors(self):
        """Plot high duplication corridors"""
        corridors = self.results['overlap']['high_duplication_corridors'][:10]

        if not corridors:
            print("⚠ Skipped: high_duplication_corridors.png (no data)")
            return

        fig, ax = plt.subplots(figsize=(12, 6))

        corridor_labels = [f"Corridor {i+1}" for i in range(len(corridors))]
        duplication_factors = [c['duplication_factor'] for c in corridors]

        bars = ax.barh(range(len(corridor_labels)), duplication_factors,
                       color='#C73E1D', alpha=0.7, edgecolor='black')

        # Color gradient based on severity
        for i, bar in enumerate(bars):
            factor = duplication_factors[i]
            if factor >= 10:
                bar.set_color('#8B0000')  # Dark red for extreme duplication
            elif factor >= 7:
                bar.set_color('#C73E1D')  # Red
            else:
                bar.set_color('#F18F01')  # Orange

        ax.set_yticks(range(len(corridor_labels)))
        ax.set_yticklabels(corridor_labels)
        ax.set_xlabel('Number of Overlapping Routes')
        ax.set_title('Top 10 Most Duplicated Corridors\n(Priority Consolidation Targets)')
        ax.grid(axis='x', alpha=0.3)
        ax.invert_yaxis()

        # Add value labels
        for i, v in enumerate(duplication_factors):
            routes = corridors[i]['routes']
            ax.text(v + 0.2, i, f'{v} routes', va='center', fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/high_duplication_corridors.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: high_duplication_corridors.png")

    def plot_hub_stops_analysis(self):
        """Plot hub stops analysis"""
        hubs = self.results['topology']['hubs'][:15]

        fig, ax = plt.subplots(figsize=(12, 7))

        hub_labels = [f"Stop {h['stop_id']}" for h in hubs]
        route_counts = [h['routes_count'] for h in hubs]

        bars = ax.barh(range(len(hub_labels)), route_counts,
                       color='#A23B72', alpha=0.7, edgecolor='black')

        # Color gradient based on hub importance
        colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(bars)))
        for bar, color in zip(bars, colors_gradient):
            bar.set_color(color)

        ax.set_yticks(range(len(hub_labels)))
        ax.set_yticklabels(hub_labels)
        ax.set_xlabel('Number of Routes Serving Stop')
        ax.set_title('Top 15 Hub Stops by Route Count\n(Critical Network Nodes)')
        ax.grid(axis='x', alpha=0.3)
        ax.invert_yaxis()

        # Add value labels
        for i, v in enumerate(route_counts):
            ax.text(v + 0.5, i, str(v), va='center', fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/hub_stops_analysis.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: hub_stops_analysis.png")

    def plot_network_efficiency_breakdown(self):
        """Plot network efficiency score breakdown"""
        overlap = self.results['overlap']
        waste = self.results['waste']
        spacing = self.results['spacing']

        # Calculate component scores
        overlap_score = 100 - overlap['overlap_percentage']
        waste_score = 100 - waste['waste_percentage']
        spacing_score = 100 - spacing['dense_percentage']
        overall_score = self.results['summary']['network_efficiency_score']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Component scores
        components = ['Route\nOverlap', 'Resource\nWaste', 'Stop\nSpacing', 'Overall\nScore']
        scores = [overlap_score, waste_score, spacing_score, overall_score]
        colors = ['#C73E1D' if s < 50 else '#F18F01' if s < 70 else '#06A77D' for s in scores]
        colors[-1] = '#2E86AB'  # Different color for overall

        bars = ax1.bar(components, scores, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax1.axhline(y=70, color='green', linestyle='--', linewidth=2, label='Good (>70)')
        ax1.axhline(y=50, color='orange', linestyle='--', linewidth=2, label='Fair (>50)')
        ax1.set_ylabel('Efficiency Score (0-100)')
        ax1.set_title('Network Efficiency Component Breakdown')
        ax1.set_ylim(0, 110)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax1.text(i, score + 2, f'{score:.1f}', ha='center', fontweight='bold')

        # Improvement potential
        current_inefficiencies = {
            'Route Overlap': 100 - overlap_score,
            'Resource Waste': 100 - waste_score,
            'Poor Stop Spacing': 100 - spacing_score
        }

        issues = list(current_inefficiencies.keys())
        impact = list(current_inefficiencies.values())
        colors_impact = ['#C73E1D', '#F18F01', '#FFB627']

        ax2.barh(issues, impact, color=colors_impact, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Inefficiency Score (Lower is Better)')
        ax2.set_title('Key Improvement Areas\n(Optimization Priorities)')
        ax2.grid(axis='x', alpha=0.3)
        ax2.invert_yaxis()

        # Add value labels
        for i, v in enumerate(impact):
            ax2.text(v + 1, i, f'{v:.1f}%', va='center', fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/network_efficiency_breakdown.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: network_efficiency_breakdown.png")

    def plot_optimization_potential(self):
        """Plot optimization potential summary"""
        waste_data = self.results['waste']
        ecology_data = self.results['ecology']

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

        # 1. Operational cost reduction potential
        waste_pct = waste_data['waste_percentage']
        efficient_pct = 100 - waste_pct

        ax1.pie([efficient_pct, waste_pct],
                labels=['Efficient', 'Waste'],
                colors=['#06A77D', '#C73E1D'],
                autopct='%1.1f%%',
                startangle=90,
                explode=[0, 0.1],
                textprops={'fontsize': 11, 'weight': 'bold'})
        ax1.set_title(f'Operational Efficiency\n{waste_pct:.1f}% Resource Waste')

        # 2. Environmental impact reduction
        co2_reduction = ecology_data['co2_reduction_potential_percent']
        co2_retained = 100 - co2_reduction

        ax2.pie([co2_retained, co2_reduction],
                labels=['Current', 'Reducible'],
                colors=['#2E86AB', '#06A77D'],
                autopct='%1.1f%%',
                startangle=90,
                explode=[0, 0.1],
                textprops={'fontsize': 11, 'weight': 'bold'})
        ax2.set_title(f'CO₂ Reduction Potential\n{co2_reduction:.1f}% Achievable')

        # 3. Quantified benefits
        benefits = {
            'Vehicle-km\nReduction': waste_data['wasted_vehicle_km'],
            'CO₂ Reduction\n(tons/year)': ecology_data['wasted_annual_co2_tons'],
            'Fuel Savings\n(k liters/year)': ecology_data['wasted_fuel_liters_annual'] / 1000
        }

        ax3.bar(benefits.keys(), benefits.values(),
                color=['#F18F01', '#06A77D', '#2E86AB'],
                alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Quantified Savings')
        ax3.set_title('Annual Optimization Benefits\n(If All Recommendations Implemented)')
        ax3.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, (k, v) in enumerate(benefits.items()):
            ax3.text(i, v + max(benefits.values()) * 0.02, f'{v:.0f}',
                    ha='center', fontweight='bold')

        # 4. Network quality score
        current_score = self.results['summary']['network_efficiency_score']
        potential_score = 85  # Realistic target after optimization

        scores = [current_score, potential_score]
        labels = ['Current\nNetwork', 'Post-\nOptimization\nTarget']
        colors = ['#C73E1D', '#06A77D']

        bars = ax4.bar(labels, scores, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax4.axhline(y=70, color='orange', linestyle='--', linewidth=2, label='Good Threshold')
        ax4.set_ylabel('Network Efficiency Score')
        ax4.set_title('Network Quality Improvement Trajectory')
        ax4.set_ylim(0, 100)
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, v in enumerate(scores):
            ax4.text(i, v + 2, f'{v:.1f}', ha='center', fontweight='bold', fontsize=12)

        # Add improvement arrow
        ax4.annotate('', xy=(1, potential_score - 5), xytext=(0, current_score + 5),
                    arrowprops=dict(arrowstyle='->', lw=2, color='green'))
        improvement = potential_score - current_score
        ax4.text(0.5, (current_score + potential_score) / 2,
                f'+{improvement:.1f} points',
                ha='center', fontsize=11, fontweight='bold', color='green',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='green', linewidth=2))

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/optimization_potential.png', bbox_inches='tight')
        plt.close()
        print("✓ Generated: optimization_potential.png")


if __name__ == "__main__":
    generator = ChartGenerator('data/analysis_results.json')
    generator.generate_all_charts()

    print(f"\nAll charts saved to '{generator.output_dir}/' directory")
    print("Charts are ready for inclusion in strategic documentation.")
