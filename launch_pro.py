#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🫒 Olive Oil Tracker Pro - Script de lancement
==============================================

Script de lancement amélioré pour l'application ultra-avancée
avec vérification des dépendances et configuration automatique.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Vérifier la version de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis!")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} détecté")
    return True

def check_dependencies():
    """Vérifier les dépendances principales"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'numpy',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package} installé")
    
    if missing_packages:
        print(f"❌ Packages manquants: {', '.join(missing_packages)}")
        print("📦 Installation automatique...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Installation réussie!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Échec de l'installation automatique")
            print("💡 Installez manuellement: pip install -r requirements.txt")
            return False
    
    return True

def check_files():
    """Vérifier les fichiers nécessaires"""
    required_files = [
        'app.py',
        'database.py', 
        'analytics.py',
        'olive_oil_data.csv'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ {file} trouvé")
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True

def check_env():
    """Vérifier la configuration de l'environnement"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ Fichier .env trouvé")
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'GEMINI_API_KEY' in content:
                    print("✅ Clé API Gemini configurée")
                else:
                    print("⚠️ Clé API Gemini non configurée (optionnel)")
        except Exception as e:
            print(f"⚠️ Erreur lecture .env: {e}")
    else:
        print("⚠️ Fichier .env non trouvé (optionnel)")
    
    return True

def launch_app():
    """Lancer l'application"""
    print("\n🚀 Lancement de Olive Oil Tracker Pro...")
    print("=" * 50)
    
    try:
        # Vérifications préalables
        if not check_python_version():
            return False
        
        if not check_dependencies():
            return False
        
        if not check_files():
            return False
        
        check_env()
        
        print("\n🎯 Toutes les vérifications sont passées!")
        print("🌐 L'application va s'ouvrir dans votre navigateur...")
        print("📱 URL locale: http://localhost:8501")
        print("🔄 Pour arrêter: Ctrl+C")
        print("=" * 50)
        
        # Lancer Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])
        
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("🫒 Olive Oil Tracker Pro - Lanceur")
    print("=" * 40)
    
    # Vérifier si on est dans le bon répertoire
    if not Path('app.py').exists():
        print("❌ Veuillez exécuter ce script depuis le répertoire du projet")
        return
    
    # Lancer l'application
    success = launch_app()
    
    if not success:
        print("\n💡 Solutions possibles:")
        print("1. Vérifiez que vous êtes dans le bon répertoire")
        print("2. Installez les dépendances: pip install -r requirements.txt")
        print("3. Vérifiez la configuration Python")
        print("4. Consultez le README.md pour plus d'informations")

if __name__ == "__main__":
    main() 