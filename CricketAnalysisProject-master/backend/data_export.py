import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os
import pandas as pd
import csv
import xlsxwriter
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ExportConfig:
    format: str  # 'json', 'csv', 'excel'
    include_metrics: bool
    include_media: bool
    include_timestamps: bool
    compression: bool

class DataExporter:
    def __init__(self, data_dir: str = "data/exports"):
        """
        Initialize the data exporter.
        
        Args:
            data_dir (str): Directory to store exported data
        """
        self.data_dir = data_dir
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating data directory: {str(e)}")
            raise
            
    def export_analysis_data(
        self,
        data: Dict[str, Any],
        config: ExportConfig,
        output_path: Optional[str] = None
    ) -> str:
        """
        Export analysis data in the specified format.
        
        Args:
            data (Dict[str, Any]): Analysis data to export
            config (ExportConfig): Export configuration
            output_path (Optional[str]): Custom output path
            
        Returns:
            str: Path to exported file
        """
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    self.data_dir,
                    f"analysis_export_{timestamp}.{config.format}"
                )
            
            if config.format == 'json':
                return self._export_json(data, output_path, config)
            elif config.format == 'csv':
                return self._export_csv(data, output_path, config)
            elif config.format == 'excel':
                return self._export_excel(data, output_path, config)
            else:
                raise ValueError(f"Unsupported export format: {config.format}")
                
        except Exception as e:
            logger.error(f"Error exporting analysis data: {str(e)}")
            raise
            
    def export_training_data(
        self,
        data: Dict[str, Any],
        config: ExportConfig,
        output_path: Optional[str] = None
    ) -> str:
        """
        Export training data in the specified format.
        
        Args:
            data (Dict[str, Any]): Training data to export
            config (ExportConfig): Export configuration
            output_path (Optional[str]): Custom output path
            
        Returns:
            str: Path to exported file
        """
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    self.data_dir,
                    f"training_export_{timestamp}.{config.format}"
                )
            
            if config.format == 'json':
                return self._export_json(data, output_path, config)
            elif config.format == 'csv':
                return self._export_csv(data, output_path, config)
            elif config.format == 'excel':
                return self._export_excel(data, output_path, config)
            else:
                raise ValueError(f"Unsupported export format: {config.format}")
                
        except Exception as e:
            logger.error(f"Error exporting training data: {str(e)}")
            raise
            
    def export_match_data(
        self,
        data: Dict[str, Any],
        config: ExportConfig,
        output_path: Optional[str] = None
    ) -> str:
        """
        Export match data in the specified format.
        
        Args:
            data (Dict[str, Any]): Match data to export
            config (ExportConfig): Export configuration
            output_path (Optional[str]): Custom output path
            
        Returns:
            str: Path to exported file
        """
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    self.data_dir,
                    f"match_export_{timestamp}.{config.format}"
                )
            
            if config.format == 'json':
                return self._export_json(data, output_path, config)
            elif config.format == 'csv':
                return self._export_csv(data, output_path, config)
            elif config.format == 'excel':
                return self._export_excel(data, output_path, config)
            else:
                raise ValueError(f"Unsupported export format: {config.format}")
                
        except Exception as e:
            logger.error(f"Error exporting match data: {str(e)}")
            raise
            
    def _export_json(
        self,
        data: Dict[str, Any],
        output_path: str,
        config: ExportConfig
    ) -> str:
        """
        Export data to JSON format.
        
        Args:
            data (Dict[str, Any]): Data to export
            output_path (str): Output file path
            config (ExportConfig): Export configuration
            
        Returns:
            str: Path to exported file
        """
        try:
            # Prepare data for export
            export_data = self._prepare_data_for_export(data, config)
            
            # Write to file
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            # Compress if requested
            if config.compression:
                compressed_path = f"{output_path}.gz"
                self._compress_file(output_path, compressed_path)
                os.remove(output_path)
                return compressed_path
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {str(e)}")
            raise
            
    def _export_csv(
        self,
        data: Dict[str, Any],
        output_path: str,
        config: ExportConfig
    ) -> str:
        """
        Export data to CSV format.
        
        Args:
            data (Dict[str, Any]): Data to export
            output_path (str): Output file path
            config (ExportConfig): Export configuration
            
        Returns:
            str: Path to exported file
        """
        try:
            # Convert data to DataFrame
            df = self._convert_to_dataframe(data, config)
            
            # Write to file
            df.to_csv(output_path, index=False)
            
            # Compress if requested
            if config.compression:
                compressed_path = f"{output_path}.gz"
                self._compress_file(output_path, compressed_path)
                os.remove(output_path)
                return compressed_path
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            raise
            
    def _export_excel(
        self,
        data: Dict[str, Any],
        output_path: str,
        config: ExportConfig
    ) -> str:
        """
        Export data to Excel format.
        
        Args:
            data (Dict[str, Any]): Data to export
            output_path (str): Output file path
            config (ExportConfig): Export configuration
            
        Returns:
            str: Path to exported file
        """
        try:
            # Convert data to DataFrame
            df = self._convert_to_dataframe(data, config)
        
        # Create Excel writer
            writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
            
            # Write to Excel
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Add formatting
            workbook = writer.book
            worksheet = writer.sheets['Data']
            
            # Add header format
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'bg_color': '#D9E1F2',
                'border': 1
            })
            
            # Apply header format
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Auto-adjust column widths
            for i, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.set_column(i, i, max_length + 2)
            
            # Save file
            writer.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {str(e)}")
            raise
            
    def _prepare_data_for_export(
        self,
        data: Dict[str, Any],
        config: ExportConfig
    ) -> Dict[str, Any]:
        """
        Prepare data for export.
        
        Args:
            data (Dict[str, Any]): Data to prepare
            config (ExportConfig): Export configuration
            
        Returns:
            Dict[str, Any]: Prepared data
        """
        try:
            export_data = data.copy()
            
            # Remove metrics if not included
            if not config.include_metrics:
                export_data.pop('metrics', None)
            
            # Remove media paths if not included
            if not config.include_media:
                export_data.pop('media_path', None)
            
            # Convert timestamps to strings if not included
            if not config.include_timestamps:
                for key, value in export_data.items():
                    if isinstance(value, datetime):
                        export_data[key] = value.isoformat()
            
            return export_data
            
        except Exception as e:
            logger.error(f"Error preparing data for export: {str(e)}")
            raise
            
    def _convert_to_dataframe(
        self,
        data: Dict[str, Any],
        config: ExportConfig
    ) -> pd.DataFrame:
        """
        Convert data to pandas DataFrame.
        
        Args:
            data (Dict[str, Any]): Data to convert
            config (ExportConfig): Export configuration
            
        Returns:
            pd.DataFrame: Converted data
        """
        try:
            # Prepare data
            export_data = self._prepare_data_for_export(data, config)
            
            # Convert to DataFrame
            if isinstance(export_data, dict):
                # Handle nested dictionaries
                flattened_data = self._flatten_dict(export_data)
                df = pd.DataFrame([flattened_data])
            elif isinstance(export_data, list):
                # Handle list of dictionaries
                flattened_data = [self._flatten_dict(item) for item in export_data]
                df = pd.DataFrame(flattened_data)
            else:
                raise ValueError("Unsupported data format")
            
            return df
            
        except Exception as e:
            logger.error(f"Error converting to DataFrame: {str(e)}")
            raise
            
    def _flatten_dict(
        self,
        d: Dict[str, Any],
        parent_key: str = '',
        sep: str = '_'
    ) -> Dict[str, Any]:
        """
        Flatten nested dictionary.
        
        Args:
            d (Dict[str, Any]): Dictionary to flatten
            parent_key (str): Parent key for nested items
            sep (str): Separator for nested keys
            
        Returns:
            Dict[str, Any]: Flattened dictionary
        """
        try:
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(
                        self._flatten_dict(v, new_key, sep=sep).items()
                    )
                else:
                    items.append((new_key, v))
            return dict(items)
            
        except Exception as e:
            logger.error(f"Error flattening dictionary: {str(e)}")
            raise
            
    def _compress_file(self, input_path: str, output_path: str) -> None:
        """
        Compress a file using gzip.
        
        Args:
            input_path (str): Path to input file
            output_path (str): Path to output file
        """
        try:
            import gzip
            with open(input_path, 'rb') as f_in:
                with gzip.open(output_path, 'wb') as f_out:
                    f_out.writelines(f_in)
                    
        except Exception as e:
            logger.error(f"Error compressing file: {str(e)}")
            raise 