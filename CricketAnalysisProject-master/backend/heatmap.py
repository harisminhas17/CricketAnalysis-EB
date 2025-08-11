import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import cv2
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def create_shot_zone_heatmap(shot_zones, output_path):
    """
    Create a heatmap of shot zones.
    
    Args:
        shot_zones: List of shot zone data
        output_path: Path to save the heatmap
    """
    try:
        # Create figure and axis
        plt.figure(figsize=(10, 6))
        
        # Count occurrences of each zone
        zone_counts = {}
        for zone in shot_zones:
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
        
        # Create bar chart
        zones = list(zone_counts.keys())
        counts = list(zone_counts.values())
        
        plt.bar(zones, counts)
        plt.title('Shot Zone Distribution')
        plt.xlabel('Zone')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        
        # Save the plot
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Shot zone heatmap saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating shot zone heatmap: {str(e)}")
        raise

def create_impact_zone_heatmap(ball_positions, output_path, trajectory=None):
    """
    Create a heatmap of ball impact zones, with optional white line for ball direction.
    
    Args:
        ball_positions: List of ball position data
        output_path: Path to save the heatmap
        trajectory: Optional list of (x, y) tuples for ball direction
    """
    try:
        # Create figure and axis
        plt.figure(figsize=(10, 6))
        
        # Extract x and y coordinates
        x_coords = [pos[0] for pos in ball_positions]
        y_coords = [pos[1] for pos in ball_positions]
        
        # Create 2D histogram
        plt.hist2d(x_coords, y_coords, bins=50, cmap='hot')
        plt.colorbar(label='Count')
        plt.title('Ball Impact Zone Heatmap')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        
        # Draw white line for ball direction if trajectory is provided
        if trajectory and len(trajectory) >= 2:
            traj_x = [p[0] for p in trajectory]
            traj_y = [p[1] for p in trajectory]
            plt.plot(traj_x, traj_y, color='white', linewidth=3, zorder=10, label='Ball Direction')
            plt.scatter(traj_x, traj_y, color='cyan', s=30, zorder=11)
            plt.legend()
        
        # Save the plot
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Impact zone heatmap saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating impact zone heatmap: {str(e)}")
        raise
