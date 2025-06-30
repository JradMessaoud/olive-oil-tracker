import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import sqlite3

# Import our custom modules
from database import db
from analytics import AdvancedAnalytics

# Configuration de la page
st.set_page_config(
    page_title="🫒 Olive Oil Tracker Pro",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🫒"
)

# Chargement des variables d'environnement
load_dotenv()

# Configuration Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Initialize database and load data
@st.cache_data
def load_data():
    """Load data from database and populate if empty"""
    try:
        # First, ensure the database and tables exist. This is robust.
        db.init_database()
        
        # Then, check if the sales table is empty.
        conn = sqlite3.connect(db.db_path)
        try:
            count = pd.read_sql_query("SELECT COUNT(*) FROM sales", conn).iloc[0, 0]
        except pd.io.sql.DatabaseError:
            # Table might not exist yet if init failed somehow, so count is 0
            count = 0
        finally:
            conn.close()

        if count == 0:
            # If empty, load from CSV.
            db.load_data_from_csv("olive_oil_data.csv")

        # Finally, get all data.
        return db.get_all_data()
    except Exception as e:
        st.error(f"❌ Erreur critique lors du chargement de la base de données: {str(e)}")
        return pd.DataFrame()

def generate_ai_summary(filtered_data):
    """Generate AI summary using Gemini"""
    if not gemini_api_key:
        return "💡 AI feature not available: Gemini is not configured."
    try:
        # Prepare data for prompt
        total_sales = filtered_data['sales'].sum()
        total_volume = filtered_data['volume'].sum()
        avg_price = filtered_data['price'].mean()
        countries = filtered_data['country'].unique()
        years = filtered_data['year'].unique()
        
        prompt = f"""
        Analyze the following olive oil sales data and generate a concise summary in French:
        
        - Total sales: {total_sales:,.2f} EUR
        - Total volume: {total_volume:,.0f} liters
        - Average price: {avg_price:.2f} EUR/liter
        - Countries: {', '.join(countries)}
        - Years: {', '.join(map(str, years))}
        
        Please provide a brief analysis of the sales trends and key insights.
        """
        
        # Use gemini-1.5-flash which is confirmed to work
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as ai_error:
            # If AI fails, fallback to manual summary
            return f"🤖 AI temporarily unavailable. Here's a manual analysis:\n\n{generate_manual_summary(filtered_data)}"
        
    except Exception as e:
        # Handle encoding errors safely
        error_msg = str(e)
        safe_error = error_msg.encode('ascii', 'ignore').decode('ascii')
        return f"❌ Error generating AI summary: {safe_error}\n\n{generate_manual_summary(filtered_data)}"

def generate_manual_summary(filtered_data):
    """Generate a manual summary when AI is not available"""
    total_sales = filtered_data['sales'].sum()
    total_volume = filtered_data['volume'].sum()
    avg_price = filtered_data['price'].mean()
    countries = filtered_data['country'].unique()
    years = filtered_data['year'].unique()
    
    # Find top performing country
    sales_by_country = filtered_data.groupby('country')['sales'].sum()
    top_country = sales_by_country.idxmax()
    top_sales = sales_by_country.max()
    
    # Find sales trend
    sales_by_year = filtered_data.groupby('year')['sales'].sum()
    if len(sales_by_year) > 1:
        trend = "croissant" if sales_by_year.iloc[-1] > sales_by_year.iloc[0] else "décroissant"
    else:
        trend = "stable"
    
    summary = f"""
    📊 **Résumé des ventes d'huile d'olive**
    
    **Données générales :**
    - Total des ventes : {total_sales:,.2f} EUR
    - Volume total : {total_volume:,.0f} litres
    - Prix moyen : {avg_price:.2f} EUR/litre
    
    **Répartition géographique :**
    - Pays inclus : {', '.join(countries)}
    - Meilleur performeur : {top_country} ({top_sales:,.2f} EUR)
    
    **Évolution temporelle :**
    - Période : {min(years)} - {max(years)}
    - Tendance : {trend}
    
    **Insights :**
    - {len(filtered_data)} enregistrements analysés
    - Prix moyen stable autour de {avg_price:.2f} EUR/litre
    - Diversité géographique avec {len(countries)} pays
    """
    
    return summary

def export_data(df, format_type):
    """Export data in different formats"""
    try:
        if format_type == "Excel":
            filename = f"olive_oil_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            return filename
        elif format_type == "CSV":
            filename = f"olive_oil_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            return filename
    except Exception as e:
        st.error(f"❌ Erreur lors de l'export: {str(e)}")
        return None

# Interface principale avec onglets
def main():
    st.title("🫒 Olive Oil Tracker Pro")
    st.markdown("### **Dashboard avancé pour le suivi des ventes d'huile d'olive**")
    
    # Load data
    df = load_data()
    if df.empty:
        st.error("❌ Aucune donnée disponible!")
        return
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", 
        "🔍 Analyse Avancée", 
        "📈 Prévisions", 
        "🤖 IA & Insights", 
        "💾 Gestion Données",
        "⚙️ Paramètres"
    ])
    
    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filtres")
        
        # Country filter
        all_countries = ["Tous"] + list(df['country'].unique())
        selected_country = st.selectbox("Pays", all_countries)
        
        # Year filter
        all_years = ["Toutes"] + list(df['year'].unique())
        selected_year = st.selectbox("Année", all_years)
        
        # Type filter
        all_types = ["Tous"] + list(df['type'].unique())
        selected_type = st.selectbox("Type d'huile", all_types)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_country != "Tous":
            filtered_df = filtered_df[filtered_df['country'] == selected_country]
        if selected_year != "Toutes":
            filtered_df = filtered_df[filtered_df['year'] == selected_year]
        if selected_type != "Tous":
            filtered_df = filtered_df[filtered_df['type'] == selected_type]
        
        st.markdown(f"📊 **{len(filtered_df)}** enregistrements trouvés")
        
        # Database stats
        st.markdown("---")
        st.subheader("📈 Statistiques DB")
        stats = db.get_statistics()
        st.metric("Total enregistrements", stats['total_records'])
        st.metric("Pays", stats['countries_count'])
        st.metric("Période", f"{stats['year_range'][0]}-{stats['year_range'][1]}")
    
    # Tab 1: Dashboard
    with tab1:
        st.header("📊 Dashboard Principal")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = filtered_df['sales'].sum()
            st.metric("💰 Total Ventes", f"{total_sales:,.2f} €")
        
        with col2:
            total_volume = filtered_df['volume'].sum()
            st.metric("🫒 Volume Total", f"{total_volume:,.0f} L")
        
        with col3:
            avg_price = filtered_df['price'].mean()
            st.metric("💵 Prix Moyen", f"{avg_price:.2f} €/L")
        
        with col4:
            growth_rate = ((filtered_df.groupby('year')['sales'].sum().iloc[-1] - 
                          filtered_df.groupby('year')['sales'].sum().iloc[0]) / 
                         filtered_df.groupby('year')['sales'].sum().iloc[0] * 100) if len(filtered_df.groupby('year')['sales'].sum()) > 1 else 0
            st.metric("📈 Croissance", f"{growth_rate:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Ventes par pays")
            sales_by_country = filtered_df.groupby('country')['sales'].sum().reset_index()
            fig1 = px.bar(sales_by_country, x='country', y='sales', 
                         title="Ventes totales par pays",
                         labels={'sales': 'Ventes (€)', 'country': 'Pays'})
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("📈 Évolution annuelle")
            sales_by_year = filtered_df.groupby('year')['sales'].sum().reset_index()
            fig2 = px.line(sales_by_year, x='year', y='sales',
                          title="Évolution des ventes par année",
                          labels={'sales': 'Ventes (€)', 'year': 'Année'})
            st.plotly_chart(fig2, use_container_width=True)
        
        # Additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥧 Répartition par type")
            sales_by_type = filtered_df.groupby('type')['sales'].sum().reset_index()
            fig3 = px.pie(sales_by_type, values='sales', names='type',
                         title="Répartition des ventes par type d'huile")
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            st.subheader("📋 Données détaillées")
            st.dataframe(filtered_df, use_container_width=True)
    
    # Tab 2: Advanced Analytics
    with tab2:
        st.header("🔍 Analyse Avancée")
        
        analytics = AdvancedAnalytics(filtered_df)
        
        # Advanced KPIs
        col1, col2, col3, col4 = st.columns(4)
        kpis = analytics.calculate_kpis()
        
        with col1:
            st.metric("📊 Croissance Ventes", f"{kpis.get('sales_growth', 0):.1f}%")
        with col2:
            st.metric("📈 Croissance Volume", f"{kpis.get('volume_growth', 0):.1f}%")
        with col3:
            st.metric("💰 Volatilité Prix", f"{kpis.get('price_volatility', 0):.2f}")
        with col4:
            st.metric("🎯 Concentration Marché", f"{kpis.get('market_concentration', 0):.2f}")
        
        # Advanced visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Heatmap des ventes")
            heatmap_fig = analytics.create_heatmap()
            if heatmap_fig:
                st.plotly_chart(heatmap_fig, use_container_width=True)
            else:
                st.warning("❌ Impossible de créer la heatmap")
        
        with col2:
            st.subheader("🎲 Analyse 3D")
            scatter_3d_fig = analytics.create_3d_scatter()
            if scatter_3d_fig:
                st.plotly_chart(scatter_3d_fig, use_container_width=True)
            else:
                st.warning("❌ Impossible de créer le graphique 3D")
        
        # Anomaly detection
        st.subheader("🚨 Détection d'anomalies")
        anomaly_data = analytics.detect_anomalies()
        if anomaly_data is not None:
            anomalies = anomaly_data[anomaly_data['is_anomaly']]
            if len(anomalies) > 0:
                st.warning(f"⚠️ {len(anomalies)} anomalies détectées!")
                st.dataframe(anomalies[['country', 'year', 'type', 'sales', 'anomaly_score']])
            else:
                st.success("✅ Aucune anomalie détectée")
        else:
            st.error("❌ Erreur lors de la détection d'anomalies")
    
    # Tab 3: Predictions
    with tab3:
        st.header("📈 Prévisions et Tendances")
        
        analytics = AdvancedAnalytics(filtered_df)
        
        # Sales predictions
        st.subheader("🔮 Prévisions de ventes")
        predictions, model_score = analytics.predict_sales(periods=3)
        
        if predictions is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📊 Score du modèle", f"{model_score:.2f}")
                st.dataframe(predictions)
            
            with col2:
                # Create prediction chart
                historical = filtered_df.groupby('year')['sales'].sum().reset_index()
                historical['type'] = 'Historique'
                predictions['type'] = 'Prédiction'
                predictions['sales'] = predictions['predicted_sales']
                
                combined = pd.concat([historical[['year', 'sales', 'type']], 
                                    predictions[['year', 'sales', 'type']]])
                
                fig = px.line(combined, x='year', y='sales', color='type',
                             title="Prévisions de ventes",
                             labels={'sales': 'Ventes (€)', 'year': 'Année'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ Impossible de générer les prévisions")
        
        # Trend analysis
        st.subheader("📊 Analyse des tendances")
        trend_data = filtered_df.groupby('year').agg({
            'sales': 'sum',
            'volume': 'sum',
            'price': 'mean'
        }).reset_index()
        
        fig = px.line(trend_data, x='year', y=['sales', 'volume'],
                     title="Évolution des ventes et volumes",
                     labels={'value': 'Montant', 'year': 'Année'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: AI & Insights
    with tab4:
        st.header("🤖 IA & Insights")
        
        # AI Summary
        st.subheader("📝 Résumé IA")
        if st.button("🧠 Générer un résumé IA"):
            with st.spinner("Génération du résumé en cours..."):
                summary = generate_ai_summary(filtered_df)
                st.markdown(summary)
        
        # Business recommendations
        st.subheader("💡 Recommandations Business")
        analytics = AdvancedAnalytics(filtered_df)
        recommendations = analytics.generate_recommendations()
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Advanced analysis report
        st.subheader("📊 Rapport d'analyse complet")
        if st.button("📋 Générer rapport complet"):
            with st.spinner("Génération du rapport..."):
                report = analytics.generate_report()
                st.markdown(report['summary'])
                
                # Save analysis to database
                db.save_analysis("comprehensive_report", 
                               {"filters": {"country": selected_country, "year": selected_year}},
                               report['summary'])
                st.success("✅ Rapport sauvegardé dans la base de données")
    
    # Tab 5: Data Management
    with tab5:
        st.header("💾 Gestion des Données")
        
        # --- Section pour Ajouter une nouvelle vente ---
        with st.expander("➕ Ajouter un nouvel enregistrement", expanded=False):
            with st.form("add_form", clear_on_submit=True):
                st.subheader("Nouveau enregistrement")
                add_country = st.text_input("Pays", key="add_country")
                add_year = st.number_input("Année", min_value=2000, max_value=datetime.now().year + 1, value=datetime.now().year, key="add_year")
                add_type = st.selectbox("Type d'huile", df['type'].unique(), key="add_type")
                add_sales = st.number_input("Ventes (€)", min_value=0.0, format="%.2f", key="add_sales")
                add_volume = st.number_input("Volume (L)", min_value=0.0, format="%.2f", key="add_volume")
                
                # Auto-calculate price
                if add_volume > 0:
                    add_price = add_sales / add_volume
                    st.text(f"Prix calculé: {add_price:.2f} €/L")
                else:
                    add_price = 0

                submitted_add = st.form_submit_button("💾 Ajouter la vente")
                if submitted_add:
                    if not add_country:
                        st.warning("Le nom du pays est obligatoire.")
                    else:
                        db.add_sale(add_country, add_year, add_type, add_sales, add_volume, add_price)
                        st.success(f"✅ Vente pour {add_country} en {add_year} ajoutée !")
                        st.cache_data.clear()
                        st.rerun()

        st.markdown("---")
        
        # --- Section pour Modifier ou Supprimer une vente ---
        st.subheader("✏️ Modifier ou Supprimer un enregistrement")
        
        if filtered_df.empty:
            st.warning("Aucune donnée à modifier/supprimer avec les filtres actuels.")
        else:
            # Create a more descriptive label for the selectbox
            filtered_df['display_label'] = filtered_df.apply(
                lambda row: f"ID: {row['id']} - {row['country']} ({row['year']}) - {row['sales']:,.0f}€", axis=1
            )
            
            # Select record to edit/delete
            record_to_edit_id = st.selectbox(
                "Sélectionnez un enregistrement",
                options=filtered_df['id'],
                format_func=lambda x: filtered_df.loc[filtered_df['id'] == x, 'display_label'].iloc[0]
            )
            
            selected_record = db.get_all_data().loc[db.get_all_data()['id'] == record_to_edit_id].iloc[0]

            with st.form("edit_form"):
                st.subheader(f"Modification de l'enregistrement ID: {selected_record['id']}")
                
                edit_country = st.text_input("Pays", value=selected_record['country'], key="edit_country")
                edit_year = st.number_input("Année", min_value=2000, max_value=datetime.now().year + 1, value=int(selected_record['year']), key="edit_year")
                
                # Get index of the current type for the selectbox
                type_options = list(df['type'].unique())
                current_type_index = type_options.index(selected_record['type']) if selected_record['type'] in type_options else 0
                edit_type = st.selectbox("Type d'huile", options=type_options, index=current_type_index, key="edit_type")
                
                edit_sales = st.number_input("Ventes (€)", value=float(selected_record['sales']), min_value=0.0, format="%.2f", key="edit_sales")
                edit_volume = st.number_input("Volume (L)", value=float(selected_record['volume']), min_value=0.0, format="%.2f", key="edit_volume")
                
                # Auto-calculate price
                if edit_volume > 0:
                    edit_price = edit_sales / edit_volume
                    st.text(f"Prix calculé: {edit_price:.2f} €/L")
                else:
                    edit_price = 0
                
                col1, col2 = st.columns([1, 0.2])
                with col1:
                    submitted_edit = st.form_submit_button("💾 Mettre à jour")
                with col2:
                    submitted_delete = st.form_submit_button("🗑️ Supprimer")

                if submitted_edit:
                    db.update_sale(record_to_edit_id, edit_country, edit_year, edit_type, edit_sales, edit_volume, edit_price)
                    st.success(f"✅ Enregistrement ID {record_to_edit_id} mis à jour !")
                    st.cache_data.clear()
                    st.rerun()

                if submitted_delete:
                    db.delete_sale(record_to_edit_id)
                    st.success(f"✅ Enregistrement ID {record_to_edit_id} supprimé !")
                    st.cache_data.clear()
                    st.rerun()

        st.markdown("---")
        
        # --- Section pour l'export et l'historique ---
        st.subheader("📤 Export et Historique")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Export des données filtrées**")
            export_format = st.selectbox("Format d'export", ["Excel", "CSV"], key="export_format")
            if st.button("💾 Exporter les données"):
                filename = export_data(filtered_df, export_format)
                if filename:
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="📥 Télécharger le fichier",
                            data=f.read(),
                            file_name=filename,
                            mime="application/octet-stream"
                        )
        
        with col2:
            st.markdown("**Historique récent des analyses**")
            history = db.get_analysis_history(5)
            if history:
                for record in history:
                    st.info(f"**{record[1]}** ({record[4]})")
            else:
                st.info("Aucun historique disponible.")
    
    # Tab 6: Settings
    with tab6:
        st.header("⚙️ Paramètres")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Configuration")
            st.info("Configuration actuelle:")
            st.markdown(f"- **Base de données:** {db.db_path}")
            st.markdown(f"- **API Gemini:** {'✅ Configurée' if gemini_api_key else '❌ Non configurée'}")
            st.markdown(f"- **Enregistrements:** {len(df)}")
        
        with col2:
            st.subheader("🔄 Actions système")
            if st.button("🔄 Recharger les données"):
                st.cache_data.clear()
                st.success("✅ Données rechargées!")
                st.rerun()
            
            if st.button("🗑️ Vider le cache"):
                st.cache_data.clear()
                st.success("✅ Cache vidé!")

if __name__ == "__main__":
    main() 