#!/usr/bin/env python3
"""
Script de migration des données mock vers MongoDB
Usage: python migrate_mock_data.py
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

# Add current directory to path to import models
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from models import (
    PersonalInfo, SkillCategory, SkillItem, Technology,
    Project, Service, Testimonial, Statistic, SocialLink, ProcessStep
)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Mock data (extracted from frontend/src/data/mock.js)
MOCK_DATA = {
    "personal": {
        "name": "Jean Yves",
        "title": "Spécialiste Cybersécurité & Développeur Python",
        "subtitle": "Expert en sécurité numérique et développement d'applications Python",
        "bio": "Passionné par la cybersécurité et le développement Python, je mets mon expertise technique au service de votre sécurité numérique. Formé aux dernières technologies et constamment en veille sur les menaces émergentes, j'accompagne les entreprises dans leur transformation digitale sécurisée.",
        "email": "contact@jeanyves.dev",
        "phone": "+33 6 12 34 56 78",
        "location": "Paris, France",
        "availability": "Disponible pour missions freelance",
        "website": "https://jeanyves.dev"
    },
    
    "skills": {
        "cybersecurity": {
            "title": "Cybersécurité",
            "icon": "Shield",
            "category_key": "cybersecurity",
            "items": [
                {"name": "Audit de sécurité", "level": 85},
                {"name": "Tests de pénétration", "level": 75},
                {"name": "Analyse de vulnérabilités", "level": 80},
                {"name": "Sécurité réseau", "level": 90},
                {"name": "Forensic numérique", "level": 70},
                {"name": "Conformité GDPR", "level": 75}
            ]
        },
        "python": {
            "title": "Développement Python",
            "icon": "Code",
            "category_key": "python",
            "items": [
                {"name": "Applications web", "level": 90},
                {"name": "Scripts d'automatisation", "level": 95},
                {"name": "Analyse de données", "level": 80},
                {"name": "Machine Learning", "level": 70},
                {"name": "Web scraping", "level": 85},
                {"name": "APIs REST", "level": 90}
            ]
        },
        "network": {
            "title": "Réseaux & Infrastructure",
            "icon": "Network",
            "category_key": "network",
            "items": [
                {"name": "Configuration réseau", "level": 85},
                {"name": "Monitoring système", "level": 80},
                {"name": "Diagnostic réseau", "level": 90},
                {"name": "Cloud computing", "level": 75},
                {"name": "IoT et objets connectés", "level": 70},
                {"name": "Containers Docker", "level": 65}
            ]
        }
    },
    
    "technologies": [
        {"name": "Python", "category": "Language", "icon": "Code"},
        {"name": "FastAPI", "category": "Framework", "icon": "Zap"},
        {"name": "Django", "category": "Framework", "icon": "Globe"},
        {"name": "PostgreSQL", "category": "Database", "icon": "Database"},
        {"name": "Docker", "category": "DevOps", "icon": "Container"},
        {"name": "AWS", "category": "Cloud", "icon": "Cloud"},
        {"name": "Linux", "category": "OS", "icon": "Terminal"},
        {"name": "Nmap", "category": "Security", "icon": "Search"},
        {"name": "Wireshark", "category": "Security", "icon": "Eye"},
        {"name": "Metasploit", "category": "Security", "icon": "Shield"},
        {"name": "Burp Suite", "category": "Security", "icon": "Bug"},
        {"name": "Git", "category": "Version Control", "icon": "GitBranch"}
    ],
    
    "services": [
        {
            "title": "Audit de Sécurité",
            "icon": "Shield",
            "description": "Analyse complète de votre infrastructure pour identifier les vulnérabilités et risques potentiels.",
            "features": [
                "Audit technique complet",
                "Test de pénétration",
                "Analyse des vulnérabilités",
                "Rapport détaillé",
                "Recommandations d'amélioration"
            ],
            "price": "À partir de 1500€",
            "duration": "1-2 semaines",
            "order_index": 1
        },
        {
            "title": "Développement Python",
            "icon": "Code",
            "description": "Création d'applications et scripts Python sur mesure pour vos besoins spécifiques.",
            "features": [
                "Applications web",
                "Scripts d'automatisation",
                "APIs REST",
                "Analyse de données",
                "Intégrations sur mesure"
            ],
            "price": "À partir de 500€/jour",
            "duration": "Variable",
            "order_index": 2
        },
        {
            "title": "Sécurisation d'Infrastructure",
            "icon": "Server",
            "description": "Mise en place de mesures de sécurité pour protéger votre infrastructure IT.",
            "features": [
                "Configuration sécurisée",
                "Monitoring avancé",
                "Détection d'intrusions",
                "Sauvegarde sécurisée",
                "Formation équipe"
            ],
            "price": "À partir de 800€/jour",
            "duration": "1-4 semaines",
            "order_index": 3
        },
        {
            "title": "Consulting & Formation",
            "icon": "Users",
            "description": "Accompagnement et formation de vos équipes aux bonnes pratiques de sécurité.",
            "features": [
                "Audit organisationnel",
                "Formation personnalisée",
                "Sensibilisation sécurité",
                "Processus et procédures",
                "Suivi et accompagnement"
            ],
            "price": "À partir de 600€/jour",
            "duration": "Variable",
            "order_index": 4
        }
    ],
    
    "testimonials": [
        {
            "name": "Marie Dubois",
            "role": "CTO",
            "company": "TechStart Solutions",
            "content": "Jean Yves nous a accompagnés dans la sécurisation de notre infrastructure. Son expertise technique et sa pédagogie ont été essentielles pour notre équipe.",
            "rating": 5,
            "order_index": 1
        },
        {
            "name": "Pierre Martin",
            "role": "Directeur IT",
            "company": "SecureNet Corp",
            "content": "Les scripts d'automatisation développés par Jean Yves ont considérablement amélioré notre efficacité opérationnelle. Travail de qualité professionnelle.",
            "rating": 5,
            "order_index": 2
        },
        {
            "name": "Sophie Laurent",
            "role": "Responsable Sécurité",
            "company": "DataSafe Industries",
            "content": "L'audit de sécurité réalisé par Jean Yves était très complet et les recommandations parfaitement adaptées à nos besoins. Je recommande vivement.",
            "rating": 5,
            "order_index": 3
        }
    ],
    
    "stats": [
        {"title": "Projets réalisés", "value": "18", "suffix": "+", "icon": "Code", "order_index": 1},
        {"title": "Clients satisfaits", "value": "12", "suffix": "", "icon": "Users", "order_index": 2},
        {"title": "Vulnérabilités détectées", "value": "150", "suffix": "+", "icon": "Shield", "order_index": 3},
        {"title": "Heures de développement", "value": "500", "suffix": "+", "icon": "Clock", "order_index": 4}
    ],
    
    "social": [
        {"name": "LinkedIn", "url": "https://linkedin.com/in/jeanyves", "icon": "Linkedin", "order_index": 1},
        {"name": "GitHub", "url": "https://github.com/jeanyves", "icon": "Github", "order_index": 2},
        {"name": "Twitter", "url": "https://twitter.com/jeanyves", "icon": "Twitter", "order_index": 3}
    ],
    
    "process": [
        {
            "step": 1,
            "title": "Analyse des besoins",
            "description": "Étude détaillée de votre problématique et définition des objectifs.",
            "icon": "Search"
        },
        {
            "step": 2,
            "title": "Planification",
            "description": "Élaboration d'un plan d'action avec timeline et livrables.",
            "icon": "Calendar"
        },
        {
            "step": 3,
            "title": "Développement",
            "description": "Réalisation technique avec reporting régulier des avancées.",
            "icon": "Code"
        },
        {
            "step": 4,
            "title": "Tests & Validation",
            "description": "Tests approfondis et validation avec votre équipe.",
            "icon": "CheckCircle"
        },
        {
            "step": 5,
            "title": "Livraison",
            "description": "Déploiement et formation avec documentation complète.",
            "icon": "Package"
        }
    ]
}

# Sample projects (3 examples)
SAMPLE_PROJECTS = [
    {
        "title": "Vérificateur d'Intégrité de Fichiers",
        "category": "Cybersécurité",
        "level": "Débutant",
        "description": "Outil Python pour surveiller l'intégrité des fichiers système et détecter les modifications non autorisées.",
        "technologies": ["Python", "Hashlib", "JSON", "OS"],
        "features": [
            "Calcul de hash MD5/SHA256",
            "Surveillance des changements",
            "Base de données d'empreintes",
            "Notifications en cas de modification",
            "Interface en ligne de commande"
        ],
        "status": "Terminé",
        "duration": "1 semaine",
        "github": "https://github.com/jeanyves/file-integrity-checker",
        "demo": "https://demo.jeanyves.dev/file-checker",
        "order_index": 1
    },
    {
        "title": "Analyseur de Logs de Sécurité",
        "category": "Cybersécurité",
        "level": "Intermédiaire",
        "description": "Script Python pour analyser les logs système et détecter les anomalies de sécurité.",
        "technologies": ["Python", "Pandas", "Matplotlib", "Regex"],
        "features": [
            "Parsing de logs Apache/Nginx",
            "Détection d'attaques courantes",
            "Visualisation des données",
            "Alertes par email",
            "Tableau de bord"
        ],
        "status": "En cours",
        "duration": "2 semaines",
        "github": "https://github.com/jeanyves/log-analyzer",
        "demo": "https://demo.jeanyves.dev/log-analyzer",
        "order_index": 2
    },
    {
        "title": "Scanner de Vulnérabilités Web",
        "category": "Cybersécurité",
        "level": "Avancé",
        "description": "Scanner avancé pour détecter les vulnérabilités web courantes.",
        "technologies": ["Python", "Requests", "BeautifulSoup", "SQLite"],
        "features": [
            "Détection XSS, SQLi, CSRF",
            "Scan des formulaires",
            "Vérification SSL/TLS",
            "Rapport HTML détaillé",
            "Interface web"
        ],
        "status": "En cours",
        "duration": "4 semaines",
        "github": "https://github.com/jeanyves/web-vuln-scanner",
        "demo": "https://demo.jeanyves.dev/web-scanner",
        "order_index": 3
    }
]


async def migrate_personal_info():
    """Migrate personal information"""
    print("🔄 Migrating personal information...")
    
    # Check if already exists
    existing = await db.personal_info.find_one()
    if existing:
        print("ℹ️ Personal information already exists, skipping...")
        return
    
    personal_obj = PersonalInfo(**MOCK_DATA["personal"])
    await db.personal_info.insert_one(personal_obj.dict())
    print("✅ Personal information migrated successfully")


async def migrate_skills():
    """Migrate skill categories"""
    print("🔄 Migrating skill categories...")
    
    for category_key, category_data in MOCK_DATA["skills"].items():
        existing = await db.skill_categories.find_one({"category_key": category_key})
        if existing:
            print(f"ℹ️ Skill category '{category_key}' already exists, skipping...")
            continue
        
        # Convert skill items
        skill_items = [SkillItem(**item) for item in category_data["items"]]
        
        skill_category = SkillCategory(
            title=category_data["title"],
            icon=category_data["icon"],
            category_key=category_key,
            items=skill_items
        )
        
        await db.skill_categories.insert_one(skill_category.dict())
        print(f"✅ Skill category '{category_key}' migrated successfully")


async def migrate_technologies():
    """Migrate technologies"""
    print("🔄 Migrating technologies...")
    
    for tech_data in MOCK_DATA["technologies"]:
        existing = await db.technologies.find_one({"name": tech_data["name"]})
        if existing:
            print(f"ℹ️ Technology '{tech_data['name']}' already exists, skipping...")
            continue
        
        tech_obj = Technology(**tech_data)
        await db.technologies.insert_one(tech_obj.dict())
        print(f"✅ Technology '{tech_data['name']}' migrated successfully")


async def migrate_projects():
    """Migrate sample projects"""
    print("🔄 Migrating sample projects...")
    
    for project_data in SAMPLE_PROJECTS:
        existing = await db.projects.find_one({"title": project_data["title"]})
        if existing:
            print(f"ℹ️ Project '{project_data['title']}' already exists, skipping...")
            continue
        
        project_obj = Project(**project_data)
        await db.projects.insert_one(project_obj.dict())
        print(f"✅ Project '{project_data['title']}' migrated successfully")


async def migrate_services():
    """Migrate services"""
    print("🔄 Migrating services...")
    
    for service_data in MOCK_DATA["services"]:
        existing = await db.services.find_one({"title": service_data["title"]})
        if existing:
            print(f"ℹ️ Service '{service_data['title']}' already exists, skipping...")
            continue
        
        service_obj = Service(**service_data)
        await db.services.insert_one(service_obj.dict())
        print(f"✅ Service '{service_data['title']}' migrated successfully")


async def migrate_testimonials():
    """Migrate testimonials"""
    print("🔄 Migrating testimonials...")
    
    for testimonial_data in MOCK_DATA["testimonials"]:
        existing = await db.testimonials.find_one({"name": testimonial_data["name"]})
        if existing:
            print(f"ℹ️ Testimonial from '{testimonial_data['name']}' already exists, skipping...")
            continue
        
        testimonial_obj = Testimonial(**testimonial_data)
        await db.testimonials.insert_one(testimonial_obj.dict())
        print(f"✅ Testimonial from '{testimonial_data['name']}' migrated successfully")


async def migrate_statistics():
    """Migrate statistics"""
    print("🔄 Migrating statistics...")
    
    for stat_data in MOCK_DATA["stats"]:
        existing = await db.statistics.find_one({"title": stat_data["title"]})
        if existing:
            print(f"ℹ️ Statistic '{stat_data['title']}' already exists, skipping...")
            continue
        
        
        stat_obj = Statistic(**stat_data)
        await db.statistics.insert_one(stat_obj.dict())
        print(f"✅ Statistic '{stat_data['title']}' migrated successfully")


async def migrate_social_links():
    """Migrate social links"""
    print("🔄 Migrating social links...")
    
    for social_data in MOCK_DATA["social"]:
        existing = await db.social_links.find_one({"name": social_data["name"]})
        if existing:
            print(f"ℹ️ Social link '{social_data['name']}' already exists, skipping...")
            continue
        
        social_obj = SocialLink(**social_data)
        await db.social_links.insert_one(social_obj.dict())
        print(f"✅ Social link '{social_data['name']}' migrated successfully")


async def migrate_process_steps():
    """Migrate process steps"""
    print("🔄 Migrating process steps...")
    
    for process_data in MOCK_DATA["process"]:
        existing = await db.process_steps.find_one({"step": process_data["step"]})
        if existing:
            print(f"ℹ️ Process step {process_data['step']} already exists, skipping...")
            continue
        
        process_obj = ProcessStep(**process_data)
        await db.process_steps.insert_one(process_obj.dict())
        print(f"✅ Process step {process_data['step']} migrated successfully")


async def main():
    """Main migration function"""
    print("🚀 Starting migration of mock data to MongoDB...")
    print(f"📍 MongoDB URL: {mongo_url}")
    print(f"📍 Database: {os.environ.get('DB_NAME', 'test_database')}")
    print()
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        print()
        
        # Run migrations
        await migrate_personal_info()
        await migrate_skills()
        await migrate_technologies()
        await migrate_projects()
        await migrate_services()
        await migrate_testimonials()
        await migrate_statistics()
        await migrate_social_links()
        await migrate_process_steps()
        
        print()
        print("🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)
    
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())