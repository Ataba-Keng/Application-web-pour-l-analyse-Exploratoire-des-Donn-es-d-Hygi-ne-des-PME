import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from data_analysis import DataAnalyzer
from visualization import HygieneVisualizer

def main():
    st.set_page_config( 
        page_title="Analyse Exploratoire - Évaluation Hygiène PME",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Analyse Exploratoire des Données d'Hygiène des PME")
    st.markdown("---")
    
    # Load data
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv('attached_assets/data_1757344901533.csv', encoding='utf-8-sig')
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            return None
    
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Initialize analyzers
    analyzer = DataAnalyzer(df)
    visualizer = HygieneVisualizer(df)
    
    # Sidebar for navigation
    st.sidebar.title("🔍 Navigation")
    section = st.sidebar.radio(
        "Choisir une section:",
        ["Vue d'ensemble", "Statistiques descriptives", "Visualisations par entreprise", 
         "Analyse des obstacles", "Analyse des formations", "Comparaisons inter-entreprises"]
    )
    
    if section == "Vue d'ensemble":
        show_overview(df, analyzer)
    elif section == "Statistiques descriptives":
        show_descriptive_stats(analyzer)
    elif section == "Visualisations par entreprise":
        show_company_analysis(df, visualizer)
    elif section == "Analyse des obstacles":
        show_obstacles_analysis(analyzer, visualizer)
    elif section == "Analyse des formations":
        show_training_analysis(analyzer, visualizer)
    elif section == "Comparaisons inter-entreprises":
        show_comparative_analysis(visualizer)

def show_overview(df, analyzer):
    st.header("📋 Vue d'ensemble des données")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nombre d'entreprises", len(df['ID_entreprise'].unique()))
    
    with col2:
        st.metric("Localités couvertes", len(df['Localisation'].unique()))
    
    with col3:
        st.metric("Types de produits", len(df['Type _de_produit'].unique()))
    
    with col4:
        missing_rate = (df == "Inconnu").sum().sum() / (df.shape[0] * df.shape[1]) * 100
        st.metric("Taux de données manquantes", f"{missing_rate:.1f}%")
    
    st.subheader("Aperçu des données")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Distribution par type de produit")
    product_dist = df['Type _de_produit'].value_counts()
    fig = px.bar(x=product_dist.values, y=product_dist.index, 
                 orientation='h', title="Répartition par type de produit")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

def show_descriptive_stats(analyzer):
    st.header("📈 Statistiques descriptives")
    
    # Hygiene practices statistics
    st.subheader("Statistiques des pratiques d'hygiène")
    hygiene_stats = analyzer.calculate_hygiene_statistics()
    
    for practice, stats_dict in hygiene_stats.items():
        with st.expander(f"📊 {practice}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Proportions:**")
                for category, data in stats_dict.items():
                    if category != 'confidence_intervals':
                        st.write(f"- {category}: {data['proportion']:.1%}")
            
            with col2:
                st.write("**Intervalles de confiance (95%):**")
                for category, ci in stats_dict['confidence_intervals'].items():
                    st.write(f"- {category}: [{ci[0]:.3f}, {ci[1]:.3f}]")
    
    # Staff size statistics
    st.subheader("Distribution de l'effectif du personnel")
    staff_stats = analyzer.calculate_staff_statistics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Statistiques descriptives:**")
        for key, value in staff_stats.items():
            if key != 'confidence_intervals':
                if isinstance(value, float):
                    st.write(f"- {key}: {value:.2f}")
                else:
                    st.write(f"- {key}: {value}")
    
    with col2:
        st.write("**Intervalles de confiance:**")
        for category, ci in staff_stats['confidence_intervals'].items():
            st.write(f"- {category}: [{ci[0]:.3f}, {ci[1]:.3f}]")

def show_company_analysis(df, visualizer):
    st.header("🏭 Analyse par entreprise")
    
    companies = sorted(df['ID_entreprise'].unique())
    selected_company = st.selectbox("Sélectionner une entreprise:", companies)
    
    if selected_company:
        company_data = df[df['ID_entreprise'] == selected_company].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Informations - {selected_company}")
            st.write(f"**Localisation:** {company_data['Localisation']}")
            st.write(f"**Type de produit:** {company_data['Type _de_produit']}")
            st.write(f"**Effectif:** {company_data['Effectif_du_personnel']}")
            st.write(f"**Formation reçue:** {company_data['Formation_reçue']}")
        
        with col2:
            st.subheader("Profil radar des pratiques d'hygiène")
            radar_fig = visualizer.create_company_radar(selected_company)
            st.plotly_chart(radar_fig, use_container_width=True)
        
        st.subheader("Détail des pratiques d'hygiène")
        hygiene_practices = [
            'Existence_BPH', 'Existence_BPF', 'Existence_HACCP',
            'Procedures_ecrites', 'Formation_du_personnel_en_hygiene',
            'Hygiene_du_personnel', 'Hygiene_des_locaux',
            'Stockage_des_matieres_premieres', 'Controle_qualite_regulier'
        ]
        
        practice_data = []
        for practice in hygiene_practices:
            value = company_data[practice]
            if value == "Oui":
                status = "✅ Conforme"
                color = "green"
            elif value == "Non":
                status = "❌ Non conforme"
                color = "red"
            else:
                status = "❓ Inconnu"
                color = "orange"
            
            practice_data.append({
                'Pratique': practice.replace('_', ' ').title(),
                'Statut': status
            })
        
        practice_df = pd.DataFrame(practice_data)
        st.dataframe(practice_df, use_container_width=True)

def show_obstacles_analysis(analyzer, visualizer):
    st.header("🚧 Analyse des obstacles")
    
    obstacles_stats = analyzer.analyze_obstacles()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fréquence des obstacles")
        fig = visualizer.create_obstacles_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Statistiques des obstacles")
        for obstacle_type, stats_dict in obstacles_stats.items():
            with st.expander(f"📊 {obstacle_type}"):
                st.write(f"**Proportion:** {stats_dict['proportion']:.1%}")
                ci = stats_dict['confidence_interval']
                st.write(f"**IC 95%:** [{ci[0]:.3f}, {ci[1]:.3f}]")
    
    st.subheader("Analyse détaillée des obstacles spécifiques")
    specific_obstacles = analyzer.analyze_specific_obstacles()
    
    if specific_obstacles:
        fig = px.bar(
            x=list(specific_obstacles.values()),
            y=list(specific_obstacles.keys()),
            orientation='h',
            title="Fréquence des obstacles spécifiques mentionnés"
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

def show_training_analysis(analyzer, visualizer):
    st.header("🎓 Analyse des formations")
    
    training_stats = analyzer.analyze_training()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution des formations")
        fig = visualizer.create_training_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Statistiques des formations")
        for training_type, stats_dict in training_stats.items():
            with st.expander(f"📚 {training_type}"):
                st.write(f"**Proportion:** {stats_dict['proportion']:.1%}")
                ci = stats_dict['confidence_interval']
                st.write(f"**IC 95%:** [{ci[0]:.3f}, {ci[1]:.3f}]")
    
    st.subheader("Corrélation formation-pratiques")
    correlation_fig = visualizer.create_training_correlation_heatmap()
    st.plotly_chart(correlation_fig, use_container_width=True)

def show_comparative_analysis(visualizer):
    st.header("⚖️ Comparaisons inter-entreprises")
    
    st.subheader("Comparaison des scores d'hygiène par entreprise")
    comparison_fig = visualizer.create_company_comparison_chart()
    st.plotly_chart(comparison_fig, use_container_width=True)
    
    st.subheader("Boxplot des pratiques d'hygiène")
    boxplot_fig = visualizer.create_hygiene_boxplot()
    st.plotly_chart(boxplot_fig, use_container_width=True)
    
    st.subheader("Analyse par type de produit")
    product_analysis_fig = visualizer.create_product_type_analysis()
    st.plotly_chart(product_analysis_fig, use_container_width=True)

if __name__ == "__main__":
    main()
