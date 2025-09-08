import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

class HygieneVisualizer:
    def __init__(self, df):
        self.df = df.copy()
        self.hygiene_practices = [
            'Existence_BPH', 'Existence_BPF', 'Existence_HACCP',
            'Procedures_ecrites', 'Formation_du_personnel_en_hygiene',
            'Hygiene_du_personnel', 'Hygiene_des_locaux',
            'Stockage_des_matieres_premieres', 'Controle_qualite_regulier'
        ]
        
        # French labels for better readability
        self.practice_labels = {
            'Existence_BPH': 'BPH',
            'Existence_BPF': 'BPF',
            'Existence_HACCP': 'HACCP',
            'Procedures_ecrites': 'Procédures écrites',
            'Formation_du_personnel_en_hygiene': 'Formation personnel',
            'Hygiene_du_personnel': 'Hygiène personnel',
            'Hygiene_des_locaux': 'Hygiène locaux',
            'Stockage_des_matieres_premieres': 'Stockage matières',
            'Controle_qualite_regulier': 'Contrôle qualité'
        }
        
        self.colors = {
            'Oui': '#2E8B57',
            'Non': '#DC143C',
            'Inconnu': '#FFA500'
        }
    
    def create_company_radar(self, company_id):
        """Create a radar chart for a specific company"""
        company_data = self.df[self.df['ID_entreprise'] == company_id].iloc[0]
        
        # Prepare data for radar chart
        categories = []
        values = []
        colors = []
        
        for practice in self.hygiene_practices:
            if practice in company_data:
                categories.append(self.practice_labels.get(practice, practice))
                value = company_data[practice]
                
                if value == 'Oui':
                    values.append(1)
                    colors.append(self.colors['Oui'])
                elif value == 'Non':
                    values.append(0)
                    colors.append(self.colors['Non'])
                else:
                    values.append(0.5)  # Neutral value for unknown
                    colors.append(self.colors['Inconnu'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=company_id,
            line_color='rgb(32, 201, 151)',
            fillcolor='rgba(32, 201, 151, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickvals=[0, 0.5, 1],
                    ticktext=['Non', 'Inconnu', 'Oui']
                )
            ),
            showlegend=True,
            title=f"Profil d'hygiène - {company_id}",
            font=dict(size=12)
        )
        
        return fig
    
    def create_obstacles_chart(self):
        """Create a bar chart for obstacles analysis"""
        obstacle_columns = [
            'Obstacle_technique', 'Obstacle_financier', 
            'Obstacle_organisationnel', 'Obstacle_humain'
        ]
        
        obstacle_data = []
        
        for col in obstacle_columns:
            if col in self.df.columns:
                yes_count = (self.df[col] == 'Oui').sum()
                total_responses = len(self.df[col][self.df[col].isin(['Oui', 'Non'])])
                
                if total_responses > 0:
                    percentage = (yes_count / total_responses) * 100
                    
                    obstacle_data.append({
                        'Type d\'obstacle': col.replace('Obstacle_', '').replace('_', ' ').title(),
                        'Pourcentage': percentage,
                        'Nombre': yes_count,
                        'Total': total_responses
                    })
        
        if not obstacle_data:
            return go.Figure().add_annotation(text="Aucune donnée d'obstacles disponible")
        
        df_obstacles = pd.DataFrame(obstacle_data)
        
        fig = px.bar(
            df_obstacles,
            x='Type d\'obstacle',
            y='Pourcentage',
            title='Fréquence des obstacles rencontrés (%)',
            text='Nombre',
            color='Pourcentage',
            color_continuous_scale='Reds'
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            yaxis_title='Pourcentage d\'entreprises',
            xaxis_title='Type d\'obstacle',
            showlegend=False
        )
        
        return fig
    
    def create_training_chart(self):
        """Create a chart for training analysis"""
        if 'Formation_reçue' not in self.df.columns:
            return go.Figure().add_annotation(text="Aucune donnée de formation disponible")
        
        training_counts = {'BPH': 0, 'BPF': 0, 'HACCP': 0, 'Aucune': 0, 'Multiple': 0}
        
        for training_text in self.df['Formation_reçue'].dropna():
            if training_text and training_text != 'Inconnu':
                training_str = str(training_text)
                individual_trainings = []
                
                for training_type in ['BPH', 'BPF', 'HACCP']:
                    if training_type in training_str:
                        individual_trainings.append(training_type)
                        training_counts[training_type] += 1
                
                if 'Aucune' in training_str:
                    training_counts['Aucune'] += 1
                elif len(individual_trainings) > 1:
                    training_counts['Multiple'] += 1
        
        # Create pie chart
        fig = px.pie(
            values=list(training_counts.values()),
            names=list(training_counts.keys()),
            title='Distribution des formations reçues',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        return fig
    
    def create_training_correlation_heatmap(self):
        """Create correlation heatmap between training and hygiene practices"""
        # Prepare data for correlation
        correlation_data = pd.DataFrame()
        
        # Add training dummy variables
        training_types = ['BPH', 'BPF', 'HACCP']
        for training_type in training_types:
            correlation_data[f'Formation_{training_type}'] = self.df['Formation_reçue'].apply(
                lambda x: 1 if pd.notna(x) and training_type in str(x) else 0
            )
        
        # Add hygiene practice dummy variables
        for practice in self.hygiene_practices:
            if practice in self.df.columns:
                correlation_data[practice] = self.df[practice].apply(
                    lambda x: 1 if x == 'Oui' else (0 if x == 'Non' else np.nan)
                )
        
        # Calculate correlation matrix
        corr_matrix = correlation_data.corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            title='Corrélation entre formations et pratiques d\'hygiène',
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        
        fig.update_layout(
            width=800,
            height=600
        )
        
        return fig
    
    def create_company_comparison_chart(self):
        """Create a comparison chart of hygiene scores across companies"""
        from data_analysis import DataAnalyzer
        
        analyzer = DataAnalyzer(self.df)
        scores = analyzer.get_company_hygiene_scores()
        
        if not scores:
            return go.Figure().add_annotation(text="Aucune donnée de score disponible")
        
        companies = list(scores.keys())
        score_values = list(scores.values())
        
        # Add product type information
        product_types = []
        for company in companies:
            product_type = self.df[self.df['ID_entreprise'] == company]['Type _de_produit'].iloc[0]
            product_types.append(product_type)
        
        fig = px.bar(
            x=companies,
            y=score_values,
            color=product_types,
            title='Scores d\'hygiène par entreprise',
            labels={'x': 'Entreprise', 'y': 'Score d\'hygiène (0-1)', 'color': 'Type de produit'}
        )
        
        fig.update_layout(
            xaxis_title='Entreprise',
            yaxis_title='Score d\'hygiène',
            yaxis=dict(range=[0, 1])
        )
        
        return fig
    
    def create_hygiene_boxplot(self):
        """Create boxplot for hygiene practices"""
        # Prepare data for boxplot
        plot_data = []
        
        for practice in self.hygiene_practices:
            if practice in self.df.columns:
                for _, row in self.df.iterrows():
                    value = row[practice]
                    if value in ['Oui', 'Non']:
                        numerical_value = 1 if value == 'Oui' else 0
                        plot_data.append({
                            'Pratique': self.practice_labels.get(practice, practice),
                            'Valeur': numerical_value,
                            'Entreprise': row['ID_entreprise']
                        })
        
        if not plot_data:
            return go.Figure().add_annotation(text="Aucune donnée disponible pour le boxplot")
        
        df_plot = pd.DataFrame(plot_data)
        
        fig = px.box(
            df_plot,
            x='Pratique',
            y='Valeur',
            title='Distribution des pratiques d\'hygiène',
            points='all'
        )
        
        fig.update_layout(
            xaxis_title='Pratique d\'hygiène',
            yaxis_title='Conformité (0=Non, 1=Oui)',
            yaxis=dict(tickvals=[0, 1], ticktext=['Non', 'Oui']),
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_product_type_analysis(self):
        """Create analysis by product type"""
        from data_analysis import DataAnalyzer
        
        analyzer = DataAnalyzer(self.df)
        
        # Calculate average hygiene scores by product type
        product_scores = {}
        
        for product_type in self.df['Type _de_produit'].unique():
            if pd.notna(product_type):
                product_companies = self.df[self.df['Type _de_produit'] == product_type]
                scores = []
                
                for _, row in product_companies.iterrows():
                    score = analyzer.calculate_hygiene_score(row)
                    if score > 0:  # Only include valid scores
                        scores.append(score)
                
                if scores:
                    product_scores[product_type] = np.mean(scores)
        
        if not product_scores:
            return go.Figure().add_annotation(text="Aucune donnée disponible pour l'analyse par type de produit")
        
        fig = px.bar(
            x=list(product_scores.values()),
            y=list(product_scores.keys()),
            orientation='h',
            title='Score d\'hygiène moyen par type de produit',
            labels={'x': 'Score moyen', 'y': 'Type de produit'}
        )
        
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        
        return fig
