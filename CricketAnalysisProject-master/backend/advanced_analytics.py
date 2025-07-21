import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
import pandas as pd
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CorrelationResult:
    metric1: str
    metric2: str
    correlation: float
    p_value: float
    strength: str  # 'strong', 'moderate', 'weak'
    direction: str  # 'positive', 'negative'

@dataclass
class ClusterResult:
    cluster_id: int
    center: Dict[str, float]
    metrics: Dict[str, float]
    size: int
    characteristics: List[str]

@dataclass
class ForecastResult:
    metric: str
    current_value: float
    predicted_value: float
    confidence_interval: Tuple[float, float]
    trend: str
    factors: List[str]

class AdvancedAnalytics:
    def __init__(self):
        self.scaler = StandardScaler()
        self.cluster_model = KMeans(n_clusters=3, random_state=42)
        self.forecast_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def analyze_correlations(self, metrics_data: Dict[str, List[float]]) -> List[CorrelationResult]:
        """Analyze correlations between different metrics."""
        results = []
        metrics = list(metrics_data.keys())
        
        for i in range(len(metrics)):
            for j in range(i + 1, len(metrics)):
                metric1 = metrics[i]
                metric2 = metrics[j]
                
                # Calculate correlation
                correlation, p_value = stats.pearsonr(
                    metrics_data[metric1],
                    metrics_data[metric2]
                )
                
                # Determine strength
                abs_corr = abs(correlation)
                if abs_corr >= 0.7:
                    strength = 'strong'
                elif abs_corr >= 0.3:
                    strength = 'moderate'
                else:
                    strength = 'weak'
                
                # Determine direction
                direction = 'positive' if correlation > 0 else 'negative'
                
                results.append(CorrelationResult(
                    metric1=metric1,
                    metric2=metric2,
                    correlation=correlation,
                    p_value=p_value,
                    strength=strength,
                    direction=direction
                ))
        
        return results
    
    def perform_clustering(self, metrics_data: Dict[str, List[float]]) -> List[ClusterResult]:
        """Perform clustering analysis on the metrics data."""
        # Prepare data for clustering
        data = np.array([metrics_data[metric] for metric in metrics_data.keys()]).T
        scaled_data = self.scaler.fit_transform(data)
        
        # Perform clustering
        clusters = self.cluster_model.fit_predict(scaled_data)
        
        # Analyze clusters
        results = []
        for cluster_id in range(self.cluster_model.n_clusters):
            cluster_mask = clusters == cluster_id
            cluster_data = scaled_data[cluster_mask]
            
            # Calculate cluster center
            center = self.scaler.inverse_transform(
                self.cluster_model.cluster_centers_[cluster_id]
            )
            
            # Calculate cluster metrics
            cluster_metrics = {
                metric: np.mean(data[cluster_mask, i])
                for i, metric in enumerate(metrics_data.keys())
            }
            
            # Identify cluster characteristics
            characteristics = self._identify_cluster_characteristics(
                cluster_metrics,
                metrics_data.keys()
            )
            
            results.append(ClusterResult(
                cluster_id=cluster_id,
                center=dict(zip(metrics_data.keys(), center)),
                metrics=cluster_metrics,
                size=int(np.sum(cluster_mask)),
                characteristics=characteristics
            ))
        
        return results
    
    def _identify_cluster_characteristics(self, metrics: Dict[str, float], all_metrics: List[str]) -> List[str]:
        """Identify key characteristics of a cluster."""
        characteristics = []
        
        # Define thresholds for different characteristics
        thresholds = {
            'bat_speed': {'high': 80, 'low': 60},
            'shot_accuracy': {'high': 0.8, 'low': 0.6},
            'fatigue_level': {'high': 0.7, 'low': 0.3}
        }
        
        for metric, value in metrics.items():
            if metric in thresholds:
                if value >= thresholds[metric]['high']:
                    characteristics.append(f"High {metric.replace('_', ' ')}")
                elif value <= thresholds[metric]['low']:
                    characteristics.append(f"Low {metric.replace('_', ' ')}")
        
        return characteristics
    
    def forecast_performance(self, 
                           historical_data: Dict[str, List[float]], 
                           forecast_horizon: int = 5) -> Dict[str, ForecastResult]:
        """Forecast future performance based on historical data."""
        results = {}
        
        for metric, values in historical_data.items():
            if len(values) < 10:  # Need minimum data points for forecasting
                continue
            
            # Prepare features for forecasting
            X = np.array(range(len(values))).reshape(-1, 1)
            y = np.array(values)
            
            # Train forecasting model
            self.forecast_model.fit(X, y)
            
            # Make predictions
            future_X = np.array(range(len(values), len(values) + forecast_horizon)).reshape(-1, 1)
            predictions = self.forecast_model.predict(future_X)
            
            # Calculate confidence intervals
            std_dev = np.std(self.forecast_model.predict(X) - y)
            confidence_interval = (
                predictions[-1] - 1.96 * std_dev,
                predictions[-1] + 1.96 * std_dev
            )
            
            # Determine trend
            current_value = values[-1]
            predicted_value = predictions[-1]
            trend = 'improving' if predicted_value > current_value else 'declining'
            
            # Identify important factors
            factors = self._identify_forecast_factors(metric, historical_data)
            
            results[metric] = ForecastResult(
                metric=metric,
                current_value=current_value,
                predicted_value=predicted_value,
                confidence_interval=confidence_interval,
                trend=trend,
                factors=factors
            )
        
        return results
    
    def _identify_forecast_factors(self, target_metric: str, 
                                 historical_data: Dict[str, List[float]]) -> List[str]:
        """Identify factors that influence the forecast."""
        factors = []
        
        # Calculate correlations with other metrics
        for metric, values in historical_data.items():
            if metric != target_metric:
                correlation, _ = stats.pearsonr(
                    historical_data[target_metric],
                    values
                )
                
                if abs(correlation) >= 0.5:
                    factors.append(f"{metric.replace('_', ' ')} (correlation: {correlation:.2f})")
        
        return factors
    
    def get_analytics_summary(self, metrics_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Get a comprehensive summary of all analytics."""
        correlations = self.analyze_correlations(metrics_data)
        clusters = self.perform_clustering(metrics_data)
        forecasts = self.forecast_performance(metrics_data)
        
        return {
            'correlations': [
                {
                    'metric1': c.metric1,
                    'metric2': c.metric2,
                    'correlation': c.correlation,
                    'p_value': c.p_value,
                    'strength': c.strength,
                    'direction': c.direction
                }
                for c in correlations
            ],
            'clusters': [
                {
                    'cluster_id': c.cluster_id,
                    'center': c.center,
                    'metrics': c.metrics,
                    'size': c.size,
                    'characteristics': c.characteristics
                }
                for c in clusters
            ],
            'forecasts': {
                metric: {
                    'current_value': f.current_value,
                    'predicted_value': f.predicted_value,
                    'confidence_interval': f.confidence_interval,
                    'trend': f.trend,
                    'factors': f.factors
                }
                for metric, f in forecasts.items()
            }
        } 