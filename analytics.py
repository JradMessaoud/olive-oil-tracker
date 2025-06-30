#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

class AdvancedAnalytics:
    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()
    
    def detect_anomalies(self, column='sales', contamination=0.1):
        """Detect anomalies in sales data"""
        try:
            # Prepare data for anomaly detection
            X = self.data[column].values.reshape(-1, 1)
            X_scaled = self.scaler.fit_transform(X)
            
            # Use Isolation Forest for anomaly detection
            iso_forest = IsolationForest(contamination=contamination, random_state=42)
            anomalies = iso_forest.fit_predict(X_scaled)
            
            # Create anomaly dataframe
            anomaly_data = self.data.copy()
            anomaly_data['is_anomaly'] = anomalies == -1
            anomaly_data['anomaly_score'] = iso_forest.decision_function(X_scaled)
            
            return anomaly_data
        except Exception as e:
            return None
    
    def predict_sales(self, periods=3):
        """Predict future sales using linear regression"""
        try:
            # Prepare time series data
            time_series = self.data.groupby('year')['sales'].sum().reset_index()
            time_series['time_index'] = range(len(time_series))
            
            # Train linear regression model
            X = time_series['time_index'].values.reshape(-1, 1)
            y = time_series['sales'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict future periods
            future_indices = np.array(range(len(time_series), len(time_series) + periods)).reshape(-1, 1)
            predictions = model.predict(future_indices)
            
            # Create prediction dataframe
            future_years = range(time_series['year'].max() + 1, time_series['year'].max() + 1 + periods)
            predictions_df = pd.DataFrame({
                'year': future_years,
                'predicted_sales': predictions,
                'confidence': [0.85] * periods  # Simple confidence score
            })
            
            return predictions_df, model.score(X, y)
        except Exception as e:
            return None, 0
    
    def generate_recommendations(self):
        """Generate business recommendations based on data analysis"""
        recommendations = []
        
        try:
            # Analyze sales trends
            sales_by_year = self.data.groupby('year')['sales'].sum()
            if len(sales_by_year) > 1:
                growth_rate = (sales_by_year.iloc[-1] - sales_by_year.iloc[0]) / sales_by_year.iloc[0] * 100
                
                if growth_rate > 10:
                    recommendations.append("📈 Excellente croissance des ventes ! Considérez l'expansion vers de nouveaux marchés.")
                elif growth_rate > 0:
                    recommendations.append("📊 Croissance positive. Maintenez les stratégies actuelles.")
                else:
                    recommendations.append("⚠️ Déclin des ventes. Analysez les causes et ajustez la stratégie.")
            
            # Analyze country performance
            country_performance = self.data.groupby('country')['sales'].sum().sort_values(ascending=False)
            top_country = country_performance.index[0]
            top_sales = country_performance.iloc[0]
            
            recommendations.append(f"🏆 {top_country} est votre meilleur marché avec {top_sales:,.0f}€ de ventes.")
            
            # Analyze price trends
            price_trend = self.data.groupby('year')['price'].mean()
            if len(price_trend) > 1:
                price_change = (price_trend.iloc[-1] - price_trend.iloc[0]) / price_trend.iloc[0] * 100
                
                if price_change > 5:
                    recommendations.append("💰 Prix en hausse. Évaluez l'impact sur la demande.")
                elif price_change < -5:
                    recommendations.append("💸 Prix en baisse. Vérifiez la rentabilité.")
                else:
                    recommendations.append("⚖️ Prix stables. Bonne gestion des coûts.")
            
            # Analyze product mix
            type_performance = self.data.groupby('type')['sales'].sum().sort_values(ascending=False)
            best_type = type_performance.index[0]
            
            recommendations.append(f"🫒 {best_type} est votre produit le plus vendu. Concentrez-vous sur ce segment.")
            
            # Seasonal analysis
            if len(self.data['year'].unique()) > 1:
                recommendations.append("📅 Analysez les tendances saisonnières pour optimiser la production.")
            
        except Exception as e:
            recommendations.append("❌ Erreur lors de l'analyse des données.")
        
        return recommendations
    
    def create_heatmap(self):
        """Create a heatmap of sales by country and year"""
        try:
            pivot_data = self.data.pivot_table(
                values='sales', 
                index='country', 
                columns='year', 
                aggfunc='sum'
            ).fillna(0)
            
            fig = px.imshow(
                pivot_data,
                title="Heatmap des ventes par pays et année",
                labels=dict(x="Année", y="Pays", color="Ventes (€)"),
                color_continuous_scale="viridis"
            )
            
            return fig
        except Exception as e:
            return None
    
    def create_3d_scatter(self):
        """Create a 3D scatter plot of sales, volume, and price"""
        try:
            fig = px.scatter_3d(
                self.data,
                x='sales',
                y='volume',
                z='price',
                color='country',
                size='sales',
                title="Analyse 3D : Ventes, Volume et Prix",
                labels={'sales': 'Ventes (€)', 'volume': 'Volume (L)', 'price': 'Prix (€/L)'}
            )
            
            return fig
        except Exception as e:
            return None
    
    def calculate_kpis(self):
        """Calculate advanced KPIs"""
        try:
            kpis = {}
            
            # Basic KPIs
            kpis['total_sales'] = self.data['sales'].sum()
            kpis['total_volume'] = self.data['volume'].sum()
            kpis['avg_price'] = self.data['price'].mean()
            
            # Advanced KPIs
            kpis['sales_growth'] = self.calculate_growth_rate('sales')
            kpis['volume_growth'] = self.calculate_growth_rate('volume')
            kpis['price_volatility'] = self.data['price'].std()
            
            # Market share analysis
            country_sales = self.data.groupby('country')['sales'].sum()
            kpis['market_concentration'] = (country_sales ** 2).sum() / (country_sales.sum() ** 2)
            
            # Efficiency metrics
            kpis['sales_per_liter'] = kpis['total_sales'] / kpis['total_volume']
            
            return kpis
        except Exception as e:
            return {}
    
    def calculate_growth_rate(self, column):
        """Calculate year-over-year growth rate"""
        try:
            yearly_data = self.data.groupby('year')[column].sum()
            if len(yearly_data) > 1:
                return ((yearly_data.iloc[-1] - yearly_data.iloc[0]) / yearly_data.iloc[0]) * 100
            return 0
        except:
            return 0
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        report = {
            'summary': self.generate_summary(),
            'kpis': self.calculate_kpis(),
            'recommendations': self.generate_recommendations(),
            'anomalies': self.detect_anomalies(),
            'predictions': self.predict_sales()
        }
        
        return report
    
    def generate_summary(self):
        """Generate a summary of the analysis"""
        try:
            summary = f"""
            📊 **Rapport d'analyse complet**
            
            **Données analysées :**
            - Période : {self.data['year'].min()} - {self.data['year'].max()}
            - Pays : {len(self.data['country'].unique())}
            - Types d'huile : {len(self.data['type'].unique())}
            - Enregistrements : {len(self.data)}
            
            **Performance globale :**
            - Ventes totales : {self.data['sales'].sum():,.0f} €
            - Volume total : {self.data['volume'].sum():,.0f} L
            - Prix moyen : {self.data['price'].mean():.2f} €/L
            
            **Tendances :**
            - Croissance des ventes : {self.calculate_growth_rate('sales'):.1f}%
            - Croissance du volume : {self.calculate_growth_rate('volume'):.1f}%
            """
            
            return summary
        except Exception as e:
            return "❌ Erreur lors de la génération du résumé." 