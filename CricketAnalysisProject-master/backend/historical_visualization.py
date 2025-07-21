import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List
import numpy as np
from datetime import datetime

def create_form_trajectory_plot(trajectory_data: Dict[str, Any], output_path: str):
    """Create a plot showing form trajectory over time."""
    plt.figure(figsize=(12, 6))
    
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in trajectory_data['dates']]
    values = trajectory_data['values']
    
    # Plot the trajectory
    plt.plot(dates, values, 'b-', linewidth=2, label='Performance')
    
    # Add trend line
    if len(values) >= 2:
        z = np.polyfit(range(len(values)), values, 1)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(values))), 'r--', 
                label=f'Trend ({trajectory_data["trend"]})')
    
    # Customize plot
    plt.title('Performance Trajectory Over Time')
    plt.xlabel('Date')
    plt.ylabel('Performance Value')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_comparison_plot(comparison_data: Dict[str, Any], output_path: str):
    """Create a plot comparing current performance with historical data."""
    plt.figure(figsize=(10, 6))
    
    # Prepare data
    labels = ['Current', 'Average', 'Best', 'Worst']
    values = [
        comparison_data['current'],
        comparison_data['average'],
        comparison_data['best'],
        comparison_data['worst']
    ]
    
    # Create bar plot
    bars = plt.bar(labels, values)
    
    # Color bars based on comparison
    for i, bar in enumerate(bars):
        if i == 0:  # Current performance
            if values[i] > comparison_data['average']:
                bar.set_color('green')
            elif values[i] < comparison_data['average']:
                bar.set_color('red')
            else:
                bar.set_color('blue')
        else:
            bar.set_color('gray')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    # Customize plot
    plt.title('Performance Comparison')
    plt.ylabel('Performance Value')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_zone_evolution_plot(zone_data: List[Dict[str, float]], output_path: str):
    """Create a plot showing evolution of shot zones over time."""
    plt.figure(figsize=(12, 6))
    
    # Get all unique zones
    all_zones = set()
    for data in zone_data:
        all_zones.update(data.keys())
    
    # Prepare data for plotting
    dates = range(len(zone_data))
    for zone in all_zones:
        values = [data.get(zone, 0) for data in zone_data]
        plt.plot(dates, values, label=zone, marker='o')
    
    # Customize plot
    plt.title('Shot Zone Evolution Over Time')
    plt.xlabel('Time Period')
    plt.ylabel('Zone Distribution')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_performance_heatmap(metrics: List[str], comparison_data: Dict[str, Dict[str, Any]], 
                             output_path: str):
    """Create a heatmap showing performance across different metrics."""
    plt.figure(figsize=(10, 8))
    
    # Prepare data for heatmap
    data = []
    for metric in metrics:
        row = [
            comparison_data[metric]['current'],
            comparison_data[metric]['average'],
            comparison_data[metric]['best'],
            comparison_data[metric]['worst']
        ]
        data.append(row)
    
    # Create heatmap
    sns.heatmap(data, 
                annot=True, 
                fmt='.2f',
                cmap='RdYlGn',
                xticklabels=['Current', 'Average', 'Best', 'Worst'],
                yticklabels=metrics)
    
    # Customize plot
    plt.title('Performance Heatmap Across Metrics')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close() 