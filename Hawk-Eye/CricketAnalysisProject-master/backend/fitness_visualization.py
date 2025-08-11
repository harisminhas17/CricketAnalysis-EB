import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Any

def create_fitness_trends_plot(trends: Dict[str, List[float]], output_path: str) -> bool:
    """Create a plot showing fitness and load trends over time."""
    try:
        # Set style
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 8))
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot fatigue and workload trends
        x = range(len(trends['fatigue_trend']))
        ax1.plot(x, trends['fatigue_trend'], label='Fatigue Level', color='red')
        ax1.plot(x, trends['workload_trend'], label='Workload Level', color='blue')
        ax1.set_title('Fatigue and Workload Trends')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Level (0-1)')
        ax1.legend()
        ax1.grid(True)
        
        # Plot speed and distance trends
        ax2.plot(x, trends['speed_trend'], label='Speed', color='green')
        ax2.plot(x, trends['distance_trend'], label='Distance', color='purple')
        ax2.set_title('Speed and Distance Trends')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Value')
        ax2.legend()
        ax2.grid(True)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(output_path)
        plt.close('all')
        
        print(f"✅ Fitness trends plot saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating fitness trends plot: {str(e)}")
        return False
    finally:
        plt.close('all')

def create_heatmap_plot(trends: Dict[str, List[float]], output_path: str) -> bool:
    """Create a heatmap showing the correlation between different metrics."""
    try:
        # Create correlation matrix
        metrics = {
            'Fatigue': trends['fatigue_trend'],
            'Workload': trends['workload_trend'],
            'Speed': trends['speed_trend'],
            'Distance': trends['distance_trend']
        }
        
        # Calculate correlation matrix
        corr_matrix = np.corrcoef([metrics[m] for m in metrics.keys()])
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap='coolwarm',
            xticklabels=metrics.keys(),
            yticklabels=metrics.keys(),
            vmin=-1,
            vmax=1
        )
        
        plt.title('Correlation Between Fitness Metrics')
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(output_path)
        plt.close('all')
        
        print(f"✅ Fitness correlation heatmap saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating fitness correlation heatmap: {str(e)}")
        return False
    finally:
        plt.close('all') 