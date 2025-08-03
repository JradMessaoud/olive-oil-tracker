# 🫒 Olive Oil Tracker Pro

https://olive-oil-tracker.streamlit.app/


## 🚀 **Dashboard ultra-avancé pour le suivi des ventes d'huile d'olive**

Une application Streamlit complète avec **IA intégrée**, **base de données SQLite**, **analyses prédictives**, **visualisations 3D** et **gestion avancée des données**.

## ✨ **Fonctionnalités Ultra-Avancées**

### 📊 **Dashboard Principal**
- **KPIs en temps réel** : Ventes, volumes, prix, croissance
- **Graphiques interactifs** : Barres, lignes, camemberts
- **Filtres dynamiques** : Par pays, année, type d'huile
- **Interface responsive** : Multi-onglets, design moderne

### 🔍 **Analyse Avancée**
- **Détection d'anomalies** : Algorithmes ML pour identifier les valeurs aberrantes
- **Heatmaps interactives** : Visualisation des ventes par pays/année
- **Graphiques 3D** : Analyse multi-dimensionnelle (ventes, volume, prix)
- **KPIs avancés** : Croissance, volatilité, concentration de marché

### 📈 **Prévisions & IA**
- **Modèles prédictifs** : Régression linéaire pour prévoir les ventes futures
- **Analyse des tendances** : Évolution temporelle des métriques
- **IA Gemini** : Résumés automatiques et insights business
- **Recommandations** : Conseils stratégiques basés sur les données

### 💾 **Gestion des Données**
- **Base de données SQLite** : Persistance complète des données
- **Export multi-format** : Excel, CSV avec horodatage
- **Historique des analyses** : Sauvegarde des rapports générés
- **Ajout/Modification** : Interface pour gérer les données

### 🤖 **Intelligence Artificielle**
- **Résumés automatiques** : Analyse intelligente des données
- **Recommandations business** : Insights stratégiques
- **Détection de patterns** : Identification des tendances cachées
- **Fallback intelligent** : Résumés manuels si l'IA n'est pas disponible

## 🛠️ **Installation**

### 1. **Cloner le projet**
```bash
git clone <repository-url>
cd olive_oil_tracker
```

### 2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 3. **Configuration de l'IA (Optionnel)**
Créez un fichier `.env` avec votre clé API Gemini :
```env
GEMINI_API_KEY=votre_clé_api_gemini_ici
```

### 4. **Lancer l'application**
```bash
python -m streamlit run app.py
```

## 📁 **Structure du Projet**

```
olive_oil_tracker/
├── app.py                 # Application principale
├── database.py            # Gestion de la base de données SQLite
├── analytics.py           # Module d'analyse avancée
├── olive_oil_data.csv     # Données d'exemple
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement
└── README.md             # Documentation
```

## 🎯 **Utilisation**

### **Onglet Dashboard**
- Visualisez les KPIs principaux
- Explorez les graphiques interactifs
- Filtrez les données selon vos besoins

### **Onglet Analyse Avancée**
- Détectez les anomalies dans vos données
- Explorez les heatmaps et graphiques 3D
- Analysez les métriques avancées

### **Onglet Prévisions**
- Consultez les prévisions de ventes
- Analysez les tendances temporelles
- Évaluez la performance des modèles

### **Onglet IA & Insights**
- Générez des résumés automatiques
- Consultez les recommandations business
- Créez des rapports complets

### **Onglet Gestion Données**
- Exportez vos données
- Consultez l'historique des analyses
- Ajoutez de nouveaux enregistrements

### **Onglet Paramètres**
- Configurez l'application
- Gérez le cache et les données

## 🔧 **Configuration Avancée**

### **Base de Données**
L'application utilise SQLite pour la persistance :
- **Tables automatiques** : Création automatique des schémas
- **Sauvegarde des analyses** : Historique des rapports générés
- **Statistiques en temps réel** : Métriques de la base de données

### **IA Gemini**
Pour activer les fonctionnalités IA :
1. Obtenez une clé API sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Ajoutez-la dans le fichier `.env`
3. L'application utilisera automatiquement l'IA pour les analyses

### **Personnalisation**
- **Thèmes** : Interface personnalisable
- **Métriques** : KPIs configurables
- **Visualisations** : Graphiques adaptables

## 📊 **Données d'Exemple**

Le fichier `olive_oil_data.csv` contient des données d'exemple avec :
- **Pays** : France, Espagne, Italie, Grèce
- **Années** : 2020-2024
- **Types** : Extra Virgin, Pure, Organic
- **Métriques** : Ventes (€), Volume (L), Prix (€/L)

## 🚀 **Fonctionnalités Techniques**

### **Performance**
- **Cache intelligent** : Optimisation des requêtes
- **Chargement lazy** : Données chargées à la demande
- **Interface responsive** : Adaptation à tous les écrans

### **Sécurité**
- **Validation des données** : Contrôles d'intégrité
- **Gestion d'erreurs** : Fallbacks robustes
- **API sécurisée** : Clés d'API protégées

### **Extensibilité**
- **Architecture modulaire** : Facilement extensible
- **APIs internes** : Interfaces bien définies
- **Documentation** : Code commenté et structuré

## 🤝 **Contribution**

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 **Licence**

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 **Support**

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Contactez l'équipe de développement

---

**🫒 Olive Oil Tracker Pro** - L'outil ultime pour analyser vos ventes d'huile d'olive avec l'intelligence artificielle ! 
