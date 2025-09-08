import pandas as pd
import numpy as np
from scipy import stats
import re

class DataAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        self.hygiene_practices = [
            'Existence_BPH', 'Existence_BPF', 'Existence_HACCP',
            'Procedures_ecrites', 'Formation_du_personnel_en_hygiene',
            'Hygiene_du_personnel', 'Hygiene_des_locaux',
            'Stockage_des_matieres_premieres', 'Controle_qualite_regulier'
        ]
        self.obstacle_columns = [
            'Obstacle_technique', 'Obstacle_financier', 
            'Obstacle_organisationnel', 'Obstacle_humain'
        ]
    
    def calculate_hygiene_statistics(self):
        """Calculate descriptive statistics for hygiene practices"""
        results = {}
        
        for practice in self.hygiene_practices:
            if practice in self.df.columns:
                # Count occurrences
                value_counts = self.df[practice].value_counts()
                total = len(self.df[practice])
                
                # Calculate proportions and confidence intervals
                stats_dict = {}
                confidence_intervals = {}
                
                for value in ['Oui', 'Non', 'Inconnu']:
                    count = value_counts.get(value, 0)
                    proportion = count / total
                    
                    # Exact binomial confidence interval
                    if count > 0:
                        ci_lower, ci_upper = stats.binom.interval(0.95, total, proportion)
                        ci_lower = ci_lower / total
                        ci_upper = ci_upper / total
                    else:
                        ci_lower = ci_upper = 0.0
                    
                    stats_dict[value] = {
                        'count': count,
                        'proportion': proportion
                    }
                    confidence_intervals[value] = (ci_lower, ci_upper)
                
                stats_dict['confidence_intervals'] = confidence_intervals
                results[practice] = stats_dict
        
        return results
    
    def calculate_staff_statistics(self):
        """Calculate statistics for staff size"""
        # Convert staff size to numerical values for analysis
        staff_mapping = {
            '10 à 20': 15,
            '20 à 30': 25
        }
        
        staff_numeric = self.df['Effectif_du_personnel'].map(staff_mapping).dropna()
        
        if len(staff_numeric) == 0:
            return {}
        
        # Calculate descriptive statistics
        stats_dict = {
            'count': len(staff_numeric),
            'mean': staff_numeric.mean(),
            'median': staff_numeric.median(),
            'std': staff_numeric.std(),
            'min': staff_numeric.min(),
            'max': staff_numeric.max(),
            'q1': staff_numeric.quantile(0.25),
            'q3': staff_numeric.quantile(0.75),
            'iqr': staff_numeric.quantile(0.75) - staff_numeric.quantile(0.25)
        }
        
        # Confidence intervals for proportions of each category
        staff_counts = self.df['Effectif_du_personnel'].value_counts()
        total = len(self.df['Effectif_du_personnel'])
        confidence_intervals = {}
        
        for category, count in staff_counts.items():
            proportion = count / total
            if count > 0:
                ci_lower, ci_upper = stats.binom.interval(0.95, total, proportion)
                ci_lower = ci_lower / total
                ci_upper = ci_upper / total
            else:
                ci_lower = ci_upper = 0.0
            confidence_intervals[category] = (ci_lower, ci_upper)
        
        stats_dict['confidence_intervals'] = confidence_intervals
        return stats_dict
    
    def analyze_obstacles(self):
        """Analyze obstacles faced by companies"""
        results = {}
        
        for obstacle_col in self.obstacle_columns:
            if obstacle_col in self.df.columns:
                # Count Yes/No responses
                value_counts = self.df[obstacle_col].value_counts()
                total_responses = len(self.df[obstacle_col][self.df[obstacle_col].isin(['Oui', 'Non'])])
                
                if total_responses > 0:
                    yes_count = value_counts.get('Oui', 0)
                    proportion = yes_count / total_responses
                    
                    # Exact binomial confidence interval
                    if yes_count > 0:
                        ci_lower, ci_upper = stats.binom.interval(0.95, total_responses, proportion)
                        ci_lower = ci_lower / total_responses
                        ci_upper = ci_upper / total_responses
                    else:
                        ci_lower = ci_upper = 0.0
                    
                    results[obstacle_col] = {
                        'count': yes_count,
                        'total': total_responses,
                        'proportion': proportion,
                        'confidence_interval': (ci_lower, ci_upper)
                    }
        
        return results
    
    def analyze_specific_obstacles(self):
        """Analyze specific obstacles mentioned in 'Autres_obstacles' column"""
        if 'Autres_obstacles' not in self.df.columns:
            return {}
        
        obstacle_mentions = {}
        
        for obstacles_text in self.df['Autres_obstacles'].dropna():
            if obstacles_text and obstacles_text != 'Inconnu':
                # Split by common separators and clean
                obstacles = re.split(r'[,;]', str(obstacles_text))
                for obstacle in obstacles:
                    obstacle = obstacle.strip()
                    if obstacle and len(obstacle) > 3:  # Filter out very short entries
                        obstacle_mentions[obstacle] = obstacle_mentions.get(obstacle, 0) + 1
        
        # Sort by frequency
        return dict(sorted(obstacle_mentions.items(), key=lambda x: x[1], reverse=True))
    
    def analyze_training(self):
        """Analyze training received by companies"""
        if 'Formation_reçue' not in self.df.columns:
            return {}
        
        results = {}
        training_types = ['BPH', 'BPF', 'HACCP', 'Aucune']
        
        for training_type in training_types:
            # Count companies that received this training
            count = 0
            total = 0
            
            for training_text in self.df['Formation_reçue']:
                if pd.notna(training_text) and training_text != 'Inconnu':
                    total += 1
                    if training_type in str(training_text):
                        count += 1
            
            if total > 0:
                proportion = count / total
                
                # Exact binomial confidence interval
                if count > 0:
                    ci_lower, ci_upper = stats.binom.interval(0.95, total, proportion)
                    ci_lower = ci_lower / total
                    ci_upper = ci_upper / total
                else:
                    ci_lower = ci_upper = 0.0
                
                results[training_type] = {
                    'count': count,
                    'total': total,
                    'proportion': proportion,
                    'confidence_interval': (ci_lower, ci_upper)
                }
        
        return results
    
    def calculate_hygiene_score(self, row):
        """Calculate a composite hygiene score for a company"""
        score = 0
        total_practices = 0
        
        for practice in self.hygiene_practices:
            if practice in row and pd.notna(row[practice]) and row[practice] != 'Inconnu':
                total_practices += 1
                if row[practice] == 'Oui':
                    score += 1
        
        return score / total_practices if total_practices > 0 else 0
    
    def get_company_hygiene_scores(self):
        """Get hygiene scores for all companies"""
        scores = {}
        for _, row in self.df.iterrows():
            company_id = row['ID_entreprise']
            score = self.calculate_hygiene_score(row)
            scores[company_id] = score
        
        return scores
