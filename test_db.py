#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour vérifier la base de données Olive Oil Tracker Pro
"""

import pandas as pd
from database import db
import os

def test_database():
    """Test complet de la base de données"""
    print("🫒 Test de la base de données Olive Oil Tracker Pro")
    print("=" * 50)
    
    # 1. Vérifier si le fichier CSV existe
    if os.path.exists("olive_oil_data.csv"):
        print("✅ Fichier CSV trouvé")
        
        # Lire le CSV pour vérifier les colonnes
        df_csv = pd.read_csv("olive_oil_data.csv")
        print(f"📊 Colonnes CSV: {list(df_csv.columns)}")
        print(f"📈 Lignes CSV: {len(df_csv)}")
        
        # Afficher les premières lignes
        print("\n📋 Premières lignes du CSV:")
        print(df_csv.head())
        
    else:
        print("❌ Fichier CSV non trouvé!")
        return False
    
    # 2. Tester la base de données
    try:
        # Charger les données dans la DB
        print("\n🗄️ Chargement des données dans la base de données...")
        success = db.load_data_from_csv("olive_oil_data.csv")
        
        if success:
            print("✅ Données chargées avec succès")
            
            # Récupérer les données
            df_db = db.get_all_data()
            print(f"📊 Données récupérées: {len(df_db)} lignes")
            print(f"📋 Colonnes DB: {list(df_db.columns)}")
            
            # Afficher les premières lignes
            print("\n📋 Premières lignes de la DB:")
            print(df_db.head())
            
            # Statistiques
            stats = db.get_statistics()
            print(f"\n📈 Statistiques:")
            print(f"   - Total enregistrements: {stats['total_records']}")
            print(f"   - Total ventes: {stats['total_sales']:,.2f} €")
            print(f"   - Pays: {stats['countries_count']}")
            print(f"   - Période: {stats['year_range'][0]}-{stats['year_range'][1]}")
            
            return True
        else:
            print("❌ Échec du chargement des données")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de la DB: {e}")
        return False

def test_analytics():
    """Test du module d'analyse"""
    print("\n🔍 Test du module d'analyse")
    print("=" * 30)
    
    try:
        from analytics import AdvancedAnalytics
        
        # Récupérer les données
        df = db.get_all_data()
        if len(df) == 0:
            print("❌ Aucune donnée disponible pour l'analyse")
            return False
        
        # Créer l'instance d'analyse
        analytics = AdvancedAnalytics(df)
        
        # Test des KPIs
        kpis = analytics.calculate_kpis()
        print(f"✅ KPIs calculés: {len(kpis)} métriques")
        
        # Test des recommandations
        recommendations = analytics.generate_recommendations()
        print(f"✅ Recommandations générées: {len(recommendations)} conseils")
        
        # Test de la détection d'anomalies
        anomalies = analytics.detect_anomalies()
        if anomalies is not None:
            anomaly_count = len(anomalies[anomalies['is_anomaly']])
            print(f"✅ Anomalies détectées: {anomaly_count}")
        else:
            print("⚠️ Détection d'anomalies échouée")
        
        # Test des prévisions
        predictions, score = analytics.predict_sales()
        if predictions is not None:
            print(f"✅ Prévisions générées: {len(predictions)} périodes")
            print(f"📊 Score du modèle: {score:.2f}")
        else:
            print("⚠️ Prévisions échouées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'analyse: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests...")
    
    # Test de la base de données
    db_ok = test_database()
    
    if db_ok:
        # Test de l'analyse
        analytics_ok = test_analytics()
        
        if analytics_ok:
            print("\n🎉 Tous les tests sont passés!")
            print("✅ L'application est prête à être utilisée")
        else:
            print("\n⚠️ Tests d'analyse échoués")
    else:
        print("\n❌ Tests de base de données échoués")
    
    print("\n" + "=" * 50) 