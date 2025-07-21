import json
import os
from datetime import datetime
from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    date: str
    ball_by_ball: List[Dict[str, Any]]
    fitness_metrics: Dict[str, float]
    shot_zones: List[str]
    lbw_analysis: Dict[str, Any]

class HistoricalAnalyzer:
    def __init__(self, db_connection):
        """
        Initialize the historical analyzer.
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
        self.player_id = None
        self.history_file = None
    
    def _ensure_history_file(self):
        """Ensure the history file exists."""
        os.makedirs('uploads/history', exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def add_performance(self, performance: PerformanceMetrics):
        """Add a new performance record to history."""
        with open(self.history_file, 'r') as f:
            history = json.load(f)
        
        history.append({
            'date': performance.date,
            'ball_by_ball': performance.ball_by_ball,
            'fitness_metrics': performance.fitness_metrics,
            'shot_zones': performance.shot_zones,
            'lbw_analysis': performance.lbw_analysis
        })
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_form_trajectory(self, metric: str, days: int = 30) -> Dict[str, Any]:
        """Get form trajectory for a specific metric over time."""
        with open(self.history_file, 'r') as f:
            history = json.load(f)
        
        if not history:
            return {'dates': [], 'values': [], 'trend': 'insufficient_data'}
        
        # Sort by date
        history.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        # Filter by date range
        cutoff_date = (datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        recent_history = [h for h in history if h['date'] >= cutoff_date]
        
        if not recent_history:
            return {'dates': [], 'values': [], 'trend': 'insufficient_data'}
        
        dates = []
        values = []
        
        for record in recent_history:
            dates.append(record['date'])
            
            if metric == 'fitness':
                values.append(record['fitness_metrics']['fatigue_level'])
            elif metric == 'workload':
                values.append(record['fitness_metrics']['workload_level'])
            elif metric == 'shot_accuracy':
                # Calculate shot accuracy based on ball-by-ball analysis
                total_shots = len(record['ball_by_ball'])
                successful_shots = sum(1 for ball in record['ball_by_ball'] 
                                    if ball['result'] in ['Boundary', 'Single'])
                values.append(successful_shots / total_shots if total_shots > 0 else 0)
            elif metric == 'zone_distribution':
                # Calculate zone distribution
                zones = record['shot_zones']
                total_shots = len(zones)
                if total_shots > 0:
                    zone_counts = {}
                    for zone in zones:
                        zone_counts[zone] = zone_counts.get(zone, 0) + 1
                    values.append({zone: count/total_shots for zone, count in zone_counts.items()})
                else:
                    values.append({})
        
        # Calculate trend
        if len(values) >= 2:
            trend = np.polyfit(range(len(values)), values, 1)[0]
            trend_direction = 'improving' if trend > 0 else 'declining' if trend < 0 else 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        return {
            'dates': dates,
            'values': values,
            'trend': trend_direction
        }
    
    def get_comparison(self, metric: str, period: str = 'last_5') -> Dict[str, Any]:
        """Compare current performance with historical data."""
        with open(self.history_file, 'r') as f:
            history = json.load(f)
        
        if not history:
            return {'current': None, 'average': None, 'best': None, 'worst': None}
        
        # Sort by date
        history.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        # Get current performance
        current = history[-1]
        
        # Get historical data based on period
        if period == 'last_5':
            historical = history[-6:-1]  # Exclude current
        elif period == 'last_10':
            historical = history[-11:-1]
        else:  # all_time
            historical = history[:-1]
        
        if not historical:
            return {'current': None, 'average': None, 'best': None, 'worst': None}
        
        # Calculate metrics
        current_value = self._extract_metric_value(current, metric)
        historical_values = [self._extract_metric_value(h, metric) for h in historical]
        
        return {
            'current': current_value,
            'average': np.mean(historical_values),
            'best': max(historical_values),
            'worst': min(historical_values)
        }
    
    def _extract_metric_value(self, record: Dict[str, Any], metric: str) -> float:
        """Extract metric value from a record."""
        if metric == 'fitness':
            return record['fitness_metrics']['fatigue_level']
        elif metric == 'workload':
            return record['fitness_metrics']['workload_level']
        elif metric == 'shot_accuracy':
            total_shots = len(record['ball_by_ball'])
            successful_shots = sum(1 for ball in record['ball_by_ball'] 
                                if ball['result'] in ['Boundary', 'Single'])
            return successful_shots / total_shots if total_shots > 0 else 0
        elif metric == 'zone_consistency':
            zones = record['shot_zones']
            if not zones:
                return 0
            zone_counts = {}
            for zone in zones:
                zone_counts[zone] = zone_counts.get(zone, 0) + 1
            # Calculate consistency as 1 - standard deviation of zone distribution
            distribution = [count/len(zones) for count in zone_counts.values()]
            return 1 - np.std(distribution)
        return 0

    def get_performance_trends(
        self,
        player_id: str,
        start_date: datetime,
        end_date: datetime,
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get performance trends for a player over time.
        
        Args:
            player_id (str): Player identifier
            start_date (datetime): Start date for analysis
            end_date (datetime): End date for analysis
            metrics (List[str]): List of metrics to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing trend data
        """
        try:
            if metrics is None:
                metrics = ['batting_average', 'strike_rate', 'boundary_percentage']
            
            # Query database for player performance data
            query = """
                SELECT date, metric, value
                FROM player_performance
                WHERE player_id = ? AND date BETWEEN ? AND ?
                AND metric IN ({})
            """.format(','.join(['?'] * len(metrics)))
            
            params = [player_id, start_date, end_date] + metrics
            df = pd.read_sql_query(query, self.db, params=params)
            
            # Calculate trends
            trends = {}
            for metric in metrics:
                metric_data = df[df['metric'] == metric]
                if not metric_data.empty:
                    # Calculate moving average
                    metric_data['moving_avg'] = metric_data['value'].rolling(window=5).mean()
                    
                    # Calculate trend line
                    x = np.arange(len(metric_data))
                    z = np.polyfit(x, metric_data['value'], 1)
                    trend_line = np.poly1d(z)(x)
                    
                    trends[metric] = {
                        'dates': metric_data['date'].tolist(),
                        'values': metric_data['value'].tolist(),
                        'moving_avg': metric_data['moving_avg'].tolist(),
                        'trend_line': trend_line.tolist(),
                        'slope': z[0]  # Positive slope indicates improvement
                    }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error getting performance trends: {str(e)}")
            raise
            
    def analyze_shot_selection(
        self,
        player_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Analyze shot selection patterns over time.
        
        Args:
            player_id (str): Player identifier
            start_date (datetime): Start date for analysis
            end_date (datetime): End date for analysis
            
        Returns:
            Dict[str, Any]: Dictionary containing shot selection analysis
        """
        try:
            # Query database for shot data
            query = """
                SELECT date, shot_type, result, zone
                FROM shot_data
                WHERE player_id = ? AND date BETWEEN ? AND ?
            """
            
            df = pd.read_sql_query(query, self.db, params=[player_id, start_date, end_date])
            
            # Analyze shot selection patterns
            shot_analysis = {
                'shot_types': df['shot_type'].value_counts().to_dict(),
                'zone_distribution': df['zone'].value_counts().to_dict(),
                'success_rate': df.groupby('shot_type')['result'].apply(
                    lambda x: (x == 'success').mean()
                ).to_dict(),
                'temporal_trends': self._analyze_temporal_trends(df)
            }
            
            return shot_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing shot selection: {str(e)}")
            raise
            
    def _analyze_temporal_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze temporal trends in shot data.
        
        Args:
            df (pd.DataFrame): DataFrame containing shot data
            
        Returns:
            Dict[str, Any]: Dictionary containing temporal trend analysis
        """
        try:
            # Convert date to datetime if not already
            df['date'] = pd.to_datetime(df['date'])
            
            # Group by month and calculate metrics
            monthly_stats = df.groupby(df['date'].dt.to_period('M')).agg({
                'shot_type': 'count',
                'result': lambda x: (x == 'success').mean()
            }).reset_index()
            
            # Calculate trend lines
            x = np.arange(len(monthly_stats))
            shot_count_trend = np.poly1d(np.polyfit(x, monthly_stats['shot_type'], 1))(x)
            success_rate_trend = np.poly1d(np.polyfit(x, monthly_stats['result'], 1))(x)
            
            return {
                'months': monthly_stats['date'].astype(str).tolist(),
                'shot_counts': monthly_stats['shot_type'].tolist(),
                'success_rates': monthly_stats['result'].tolist(),
                'shot_count_trend': shot_count_trend.tolist(),
                'success_rate_trend': success_rate_trend.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing temporal trends: {str(e)}")
            raise
            
    def generate_performance_report(
        self,
        player_id: str,
        start_date: datetime,
        end_date: datetime,
        output_path: str
    ) -> None:
        """
        Generate a comprehensive performance report.
        
        Args:
            player_id (str): Player identifier
            start_date (datetime): Start date for analysis
            end_date (datetime): End date for analysis
            output_path (str): Path to save the report
        """
        try:
            # Get performance trends
            trends = self.get_performance_trends(player_id, start_date, end_date)
            
            # Get shot selection analysis
            shot_analysis = self.analyze_shot_selection(player_id, start_date, end_date)
            
            # Create visualizations
            plt.figure(figsize=(15, 10))
            
            # Plot performance trends
            plt.subplot(2, 2, 1)
            for metric, data in trends.items():
                plt.plot(data['dates'], data['moving_avg'], label=metric)
            plt.title('Performance Trends')
            plt.legend()
            
            # Plot shot type distribution
            plt.subplot(2, 2, 2)
            shot_types = pd.Series(shot_analysis['shot_types'])
            shot_types.plot(kind='pie', autopct='%1.1f%%')
            plt.title('Shot Type Distribution')
            
            # Plot success rates
            plt.subplot(2, 2, 3)
            success_rates = pd.Series(shot_analysis['success_rate'])
            success_rates.plot(kind='bar')
            plt.title('Success Rate by Shot Type')
            
            # Plot temporal trends
            plt.subplot(2, 2, 4)
            temporal = shot_analysis['temporal_trends']
            plt.plot(temporal['months'], temporal['success_rates'], label='Success Rate')
            plt.plot(temporal['months'], temporal['success_rate_trend'], '--', label='Trend')
            plt.title('Success Rate Over Time')
            plt.legend()
            
            # Save the report
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()
            
            logger.info(f"Performance report saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error generating performance report: {str(e)}")
            raise 