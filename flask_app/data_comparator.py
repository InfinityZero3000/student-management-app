"""
Data Comparator Module
Handles comparison between different datasets
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class DataComparator:
    """Class for comparing different datasets"""
    
    def __init__(self):
        self.comparison_results = {}
    
    def compare_datasets(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                        key_column: str = None) -> Dict:
        """
        Compare two datasets and return detailed comparison results
        
        Args:
            df1: First dataset
            df2: Second dataset  
            key_column: Column to use as key for comparison
            
        Returns:
            Dictionary containing comparison results
        """
        try:
            results = {
                'basic_stats': self._compare_basic_stats(df1, df2),
                'column_comparison': self._compare_columns(df1, df2),
                'data_types': self._compare_data_types(df1, df2),
                'missing_data': self._compare_missing_data(df1, df2),
                'summary': {}
            }
            
            # Row-level comparison if key column provided
            if key_column and key_column in df1.columns and key_column in df2.columns:
                results['row_comparison'] = self._compare_rows(df1, df2, key_column)
            
            # Generate summary
            results['summary'] = self._generate_summary(results)
            
            return results
            
        except Exception as e:
            return {'error': f'Error comparing datasets: {str(e)}'}
    
    def _compare_basic_stats(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict:
        """Compare basic statistics between datasets"""
        return {
            'dataset1': {
                'rows': len(df1),
                'columns': len(df1.columns),
                'memory_usage': df1.memory_usage(deep=True).sum()
            },
            'dataset2': {
                'rows': len(df2), 
                'columns': len(df2.columns),
                'memory_usage': df2.memory_usage(deep=True).sum()
            }
        }
    
    def _compare_columns(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict:
        """Compare columns between datasets"""
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        
        return {
            'common_columns': list(cols1.intersection(cols2)),
            'unique_to_dataset1': list(cols1 - cols2),
            'unique_to_dataset2': list(cols2 - cols1),
            'total_common': len(cols1.intersection(cols2))
        }
    
    def _compare_data_types(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict:
        """Compare data types of common columns"""
        common_cols = set(df1.columns).intersection(set(df2.columns))
        type_comparison = {}
        
        for col in common_cols:
            type_comparison[col] = {
                'dataset1_type': str(df1[col].dtype),
                'dataset2_type': str(df2[col].dtype),
                'types_match': df1[col].dtype == df2[col].dtype
            }
        
        return type_comparison
    
    def _compare_missing_data(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Dict:
        """Compare missing data patterns"""
        common_cols = set(df1.columns).intersection(set(df2.columns))
        missing_comparison = {}
        
        for col in common_cols:
            missing_comparison[col] = {
                'dataset1_missing': df1[col].isnull().sum(),
                'dataset1_missing_pct': (df1[col].isnull().sum() / len(df1)) * 100,
                'dataset2_missing': df2[col].isnull().sum(),
                'dataset2_missing_pct': (df2[col].isnull().sum() / len(df2)) * 100
            }
        
        return missing_comparison
    
    def _compare_rows(self, df1: pd.DataFrame, df2: pd.DataFrame, key_column: str) -> Dict:
        """Compare rows using a key column"""
        try:
            # Get unique keys from both datasets
            keys1 = set(df1[key_column].dropna())
            keys2 = set(df2[key_column].dropna())
            
            return {
                'common_keys': list(keys1.intersection(keys2)),
                'unique_to_dataset1': list(keys1 - keys2),
                'unique_to_dataset2': list(keys2 - keys1),
                'total_common_rows': len(keys1.intersection(keys2))
            }
        except Exception as e:
            return {'error': f'Error comparing rows: {str(e)}'}
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate a summary of comparison results"""
        summary = {
            'datasets_similar': True,
            'major_differences': [],
            'recommendations': []
        }
        
        # Check for major differences
        basic_stats = results.get('basic_stats', {})
        if basic_stats:
            row_diff = abs(basic_stats['dataset1']['rows'] - basic_stats['dataset2']['rows'])
            if row_diff > 100:  # Arbitrary threshold
                summary['major_differences'].append(f'Significant row count difference: {row_diff}')
                summary['datasets_similar'] = False
        
        column_comp = results.get('column_comparison', {})
        if column_comp:
            if len(column_comp['unique_to_dataset1']) > 0:
                summary['major_differences'].append(f"Dataset 1 has {len(column_comp['unique_to_dataset1'])} unique columns")
            if len(column_comp['unique_to_dataset2']) > 0:
                summary['major_differences'].append(f"Dataset 2 has {len(column_comp['unique_to_dataset2'])} unique columns")
        
        # Generate recommendations
        if not summary['datasets_similar']:
            summary['recommendations'].append('Consider data cleaning and standardization')
        if column_comp and len(column_comp['common_columns']) < 5:
            summary['recommendations'].append('Very few common columns - verify data sources')
        
        return summary
    
    def export_comparison_report(self, comparison_results: Dict, format: str = 'dict') -> Dict:
        """Export comparison results in specified format"""
        if format == 'dict':
            return comparison_results
        elif format == 'summary':
            return comparison_results.get('summary', {})
        else:
            return {'error': f'Unsupported format: {format}'}
