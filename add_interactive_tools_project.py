#!/usr/bin/env python3
"""
Script pour ajouter un projet "Outils Interactifs de Cybersécurité" 
qui intègre les 7 outils développés dans l'interface InteractiveTools.jsx
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

# Add current directory to path to import models
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from models import Project

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Nouveau projet pour les outils interactifs
INTERACTIVE_TOOLS_PROJECT = {
    "title": "Plateforme d'Outils Interactifs de Cybersécurité", 
    "category": "Cybersécurité",
    "level": "Avancé",
    "description": "Collection complète de 7 outils interactifs de cybersécurité développés en React pour démontrer l'expertise technique et offrir des services éducatifs en sécurité informatique.",
    "technologies": ["React", "JavaScript", "CryptoJS", "Tailwind CSS", "Lucide Icons"],
    "features": [
        "Générateur de Hash multi-algorithmes (MD5, SHA1, SHA256, SHA512)",
        "Analyseur de mots de passe avec calcul d'entropie et suggestions",
        "Scanner de ports simulé avec détection de services",
        "Chiffreur/Déchiffreur AES avec interface intuitive",
        "Analyseur d'URL avec parsing sécurisé des composants",
        "Détecteur XSS avancé avec analyse de patterns malveillants",
        "Validateur JSON avec formatage et analyse structurelle",
        "Interface responsive avec thème sombre cybersécurité",
        "Système de copie en un clic pour tous les résultats",
        "Feedback visuel et alertes éducatives pour chaque outil"
    ],
    "status": "Terminé",
    "duration": "3 semaines",
    "github": "https://github.com/jeanyves/cybersecurity-tools",
    "demo": "/tools",  # Lien vers la page d'outils interactifs
    "order_index": 10  # Mettre en dernier pour qu'il apparaisse en premier
}

async def add_interactive_tools_project():
    """Ajoute le projet des outils interactifs"""
    print("🔄 Adding Interactive Cybersecurity Tools project...")
    
    # Check if already exists
    existing = await db.projects.find_one({"title": INTERACTIVE_TOOLS_PROJECT["title"]})
    if existing:
        print("ℹ️ Interactive Tools project already exists, updating...")
        # Update existing project
        project_obj = Project(**INTERACTIVE_TOOLS_PROJECT)
        await db.projects.update_one(
            {"title": INTERACTIVE_TOOLS_PROJECT["title"]},
            {"$set": project_obj.dict()}
        )
        print("✅ Interactive Tools project updated successfully")
    else:
        # Create new project
        project_obj = Project(**INTERACTIVE_TOOLS_PROJECT)
        await db.projects.insert_one(project_obj.dict())
        print("✅ Interactive Tools project added successfully")

async def main():
    """Main function"""
    print("🚀 Adding Interactive Cybersecurity Tools project to MongoDB...")
    print(f"📍 MongoDB URL: {mongo_url}")
    print(f"📍 Database: {os.environ.get('DB_NAME', 'test_database')}")
    print()
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        print()
        
        # Add project
        await add_interactive_tools_project()
        
        print()
        print("🎉 Project addition completed successfully!")
        
    except Exception as e:
        print(f"❌ Operation failed: {str(e)}")
        sys.exit(1)
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())