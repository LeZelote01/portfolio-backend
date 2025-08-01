from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any
import os
from datetime import datetime, timedelta
from collections import Counter
import asyncio

from models import AdminUser
from auth import get_current_user

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Create analytics router
analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])


class AutoStatistic:
    def __init__(self, title: str, value: Any, suffix: str = "", description: str = "", 
                 icon: str = "BarChart3", color: str = "#3b82f6", trend: str = "neutral"):
        self.title = title
        self.value = str(value)
        self.suffix = suffix
        self.description = description
        self.icon = icon
        self.color = color
        self.trend = trend  # positive, negative, neutral


class AIRecommendation:
    def __init__(self, title: str, priority: str, description: str, 
                 action: str, impact: str, category: str = "general"):
        self.title = title
        self.priority = priority  # high, medium, low
        self.description = description
        self.action = action
        self.impact = impact
        self.category = category


@analytics_router.get("/dashboard")
async def get_analytics_dashboard(current_user: AdminUser = Depends(get_current_user)):
    """Get comprehensive analytics dashboard with auto-calculated statistics"""
    
    try:
        # Calculer toutes les statistiques en parallèle
        stats_data = await asyncio.gather(
            calculate_content_stats(),
            calculate_engagement_stats(),
            calculate_technical_stats(),
            calculate_business_stats(),
            return_exceptions=True
        )
        
        # Combiner toutes les statistiques
        all_statistics = []
        for stat_group in stats_data:
            if not isinstance(stat_group, Exception):
                all_statistics.extend(stat_group)
        
        # Générer des recommandations IA
        recommendations = await generate_ai_recommendations(all_statistics)
        
        return {
            "statistics": [stat.__dict__ for stat in all_statistics],
            "recommendations": [rec.__dict__ for rec in recommendations],
            "last_updated": datetime.utcnow().isoformat(),
            "total_stats": len(all_statistics)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul des statistiques: {str(e)}")


async def calculate_content_stats() -> List[AutoStatistic]:
    """Calcule les statistiques de contenu"""
    stats = []
    
    # Nombre de projets
    projects_count = await db.projects.count_documents({})
    completed_projects = await db.projects.count_documents({"status": "Terminé"})
    
    stats.append(AutoStatistic(
        title="Projets Totaux",
        value=projects_count,
        description="Nombre total de projets dans le portfolio",
        icon="FolderOpen",
        color="#10b981",
        trend="positive" if projects_count > 5 else "neutral"
    ))
    
    if projects_count > 0:
        completion_rate = (completed_projects / projects_count) * 100
        stats.append(AutoStatistic(
            title="Taux d'Achèvement",
            value=int(completion_rate),
            suffix="%",
            description="Pourcentage de projets terminés",
            icon="CheckCircle",
            color="#f59e0b" if completion_rate < 80 else "#10b981",
            trend="positive" if completion_rate >= 80 else "negative"
        ))
    
    # Articles de blog
    blog_posts = await db.blog_posts.count_documents({"published": True})
    stats.append(AutoStatistic(
        title="Articles Publiés",
        value=blog_posts,
        description="Articles de blog techniques publiés",
        icon="FileText",
        color="#6366f1",
        trend="positive" if blog_posts > 0 else "neutral"
    ))
    
    # Technologies maîtrisées
    tech_count = await db.technologies.count_documents({})
    stats.append(AutoStatistic(
        title="Technologies",
        value=tech_count,
        description="Technologies maîtrisées et utilisées",
        icon="Code",
        color="#8b5cf6"
    ))
    
    return stats


async def calculate_engagement_stats() -> List[AutoStatistic]:
    """Calcule les statistiques d'engagement"""
    stats = []
    
    # Témoignages
    testimonials_count = await db.testimonials.count_documents({})
    pending_testimonials = await db.pending_testimonials.count_documents({"status": "pending"})
    
    stats.append(AutoStatistic(
        title="Témoignages",
        value=testimonials_count,
        description="Témoignages clients validés",
        icon="Star",
        color="#f59e0b",
        trend="positive" if testimonials_count > 0 else "neutral"
    ))
    
    if pending_testimonials > 0:
        stats.append(AutoStatistic(
            title="En Attente",
            value=pending_testimonials,
            description="Témoignages en attente de validation",
            icon="Clock",
            color="#f97316",
            trend="neutral"
        ))
    
    # Note moyenne des témoignages
    testimonials = await db.testimonials.find().to_list(1000)
    if testimonials:
        avg_rating = sum(t.get("rating", 0) for t in testimonials) / len(testimonials)
        stats.append(AutoStatistic(
            title="Note Moyenne",
            value=f"{avg_rating:.1f}",
            suffix="/5",
            description="Satisfaction moyenne des clients",
            icon="Award",
            color="#10b981" if avg_rating >= 4.0 else "#f59e0b",
            trend="positive" if avg_rating >= 4.0 else "neutral"
        ))
    
    # Ressources téléchargées
    total_downloads = 0
    resources = await db.resources.find().to_list(1000)
    for resource in resources:
        total_downloads += resource.get("downloads", 0)
    
    stats.append(AutoStatistic(
        title="Téléchargements",
        value=total_downloads,
        description="Total des ressources téléchargées",
        icon="Download",
        color="#06b6d4",
        trend="positive" if total_downloads > 100 else "neutral"
    ))
    
    return stats


async def calculate_technical_stats() -> List[AutoStatistic]:
    """Calcule les statistiques techniques"""
    stats = []
    
    # Compétences par niveau
    skills = await db.skill_categories.find().to_list(1000)
    total_skills = sum(len(skill.get("items", [])) for skill in skills)
    
    stats.append(AutoStatistic(
        title="Compétences",
        value=total_skills,
        description="Total des compétences répertoriées",
        icon="Zap",
        color="#8b5cf6"
    ))
    
    # Analyse des technologies par catégorie
    technologies = await db.technologies.find().to_list(1000)
    tech_by_level = Counter(tech.get("level", "intermediate") for tech in technologies)
    
    expert_count = tech_by_level.get("expert", 0)
    if expert_count > 0:
        stats.append(AutoStatistic(
            title="Niveau Expert",
            value=expert_count,
            description="Technologies maîtrisées au niveau expert",
            icon="Award",
            color="#dc2626",
            trend="positive"
        ))
    
    # Services proposés
    services_count = await db.services.count_documents({})
    stats.append(AutoStatistic(
        title="Services",
        value=services_count,
        description="Services professionnels proposés",
        icon="Briefcase",
        color="#059669"
    ))
    
    return stats


async def calculate_business_stats() -> List[AutoStatistic]:
    """Calcule les statistiques business"""
    stats = []
    
    # Réservations/bookings
    bookings_count = await db.bookings.count_documents({})
    confirmed_bookings = await db.bookings.count_documents({"status": "confirmed"})
    
    stats.append(AutoStatistic(
        title="Réservations",
        value=bookings_count,
        description="Total des réservations reçues",
        icon="Calendar",
        color="#0ea5e9",
        trend="positive" if bookings_count > 0 else "neutral"
    ))
    
    # Devis demandés
    quotes_count = await db.quotes.count_documents({})
    if quotes_count > 0:
        stats.append(AutoStatistic(
            title="Devis Demandés",
            value=quotes_count,
            description="Demandes de devis reçues",
            icon="FileText",
            color="#7c3aed",
            trend="positive"
        ))
    
    # Newsletter subscribers
    newsletter_count = await db.newsletter_subscriptions.count_documents({"status": "active"})
    stats.append(AutoStatistic(
        title="Abonnés Newsletter",
        value=newsletter_count,
        description="Abonnés à la newsletter",
        icon="Mail",
        color="#0891b2",
        trend="positive" if newsletter_count > 10 else "neutral"
    ))
    
    # Activité récente (derniers 30 jours)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_activity = 0
    
    # Compter l'activité récente dans différentes collections
    recent_bookings = await db.bookings.count_documents({"created_at": {"$gte": thirty_days_ago}})
    recent_testimonials = await db.pending_testimonials.count_documents({"submitted_at": {"$gte": thirty_days_ago}})
    recent_quotes = await db.quotes.count_documents({"created_at": {"$gte": thirty_days_ago}})
    
    recent_activity = recent_bookings + recent_testimonials + recent_quotes
    
    stats.append(AutoStatistic(
        title="Activité (30j)",
        value=recent_activity,
        description="Interactions clients ce mois",
        icon="TrendingUp",
        color="#10b981" if recent_activity > 5 else "#f59e0b",
        trend="positive" if recent_activity > 5 else "neutral"
    ))
    
    return stats


async def generate_ai_recommendations(statistics: List[AutoStatistic]) -> List[AIRecommendation]:
    """Génère des recommandations intelligentes basées sur les statistiques"""
    recommendations = []
    
    # Analyser les statistiques pour générer des recommandations
    stats_dict = {stat.title: stat for stat in statistics}
    
    # Recommandations basées sur le contenu
    projects_count = int(stats_dict.get("Projets Totaux", AutoStatistic("", "0")).value)
    if projects_count < 5:
        recommendations.append(AIRecommendation(
            title="Augmenter le Portfolio de Projets",
            priority="high",
            description=f"Vous avez seulement {projects_count} projets. Un portfolio de 8-12 projets est recommandé pour démontrer votre expertise.",
            action="Ajouter 3-5 nouveaux projets représentatifs de vos compétences",
            impact="Amélioration de la crédibilité et attraction de nouveaux clients",
            category="content"
        ))
    
    # Recommandations basées sur les témoignages
    testimonials_count = int(stats_dict.get("Témoignages", AutoStatistic("", "0")).value)
    if testimonials_count < 3:
        recommendations.append(AIRecommendation(
            title="Collecter Plus de Témoignages",
            priority="high",
            description=f"Seulement {testimonials_count} témoignages visibles. 5-8 témoignages minimum sont recommandés.",
            action="Contacter vos anciens clients satisfaits pour obtenir des témoignages",
            impact="Augmentation de la confiance et du taux de conversion",
            category="engagement"
        ))
    
    # Recommandations basées sur le taux d'achèvement
    if "Taux d'Achèvement" in stats_dict:
        completion_rate = int(stats_dict["Taux d'Achèvement"].value)
        if completion_rate < 80:
            recommendations.append(AIRecommendation(
                title="Améliorer le Taux d'Achèvement des Projets",
                priority="medium",
                description=f"Votre taux d'achèvement est de {completion_rate}%. Un taux de 85%+ est recommandé.",
                action="Finaliser les projets en cours ou les marquer comme terminés",
                impact="Démonstration d'une meilleure gestion de projet",
                category="technical"
            ))
    
    # Recommandations basées sur le blog
    blog_count = int(stats_dict.get("Articles Publiés", AutoStatistic("", "0")).value)
    if blog_count < 5:
        recommendations.append(AIRecommendation(
            title="Développer le Blog Technique",
            priority="medium",
            description=f"Vous avez {blog_count} articles publiés. 8-12 articles améliorent significativement le SEO.",
            action="Publier 1-2 articles techniques par mois sur vos domaines d'expertise",
            impact="Amélioration du référencement et positionnement d'expert",
            category="content"
        ))
    
    # Recommandations basées sur les téléchargements
    downloads = int(stats_dict.get("Téléchargements", AutoStatistic("", "0")).value)
    if downloads < 50:
        recommendations.append(AIRecommendation(
            title="Promouvoir les Ressources Gratuites",
            priority="low",
            description=f"Seulement {downloads} téléchargements. Les ressources gratuites génèrent des leads qualifiés.",
            action="Créer du contenu premium et promouvoir vos ressources sur les réseaux sociaux",
            impact="Génération de leads et construction d'une liste email",
            category="business"
        ))
    
    # Recommandations basées sur l'activité récente
    if "Activité (30j)" in stats_dict:
        recent_activity = int(stats_dict["Activité (30j)"].value)
        if recent_activity < 3:
            recommendations.append(AIRecommendation(
                title="Stimuler l'Engagement Client",
                priority="high",
                description=f"Faible activité récente ({recent_activity} interactions ce mois). Une activité régulière maintient la dynamique commerciale.",
                action="Lancer une campagne marketing ou promouvoir vos services sur LinkedIn",
                impact="Augmentation des opportunités commerciales",
                category="business"
            ))
    
    # Recommandation sur la newsletter
    newsletter_count = int(stats_dict.get("Abonnés Newsletter", AutoStatistic("", "0")).value)
    if newsletter_count < 20:
        recommendations.append(AIRecommendation(
            title="Développer la Liste Email",
            priority="medium",
            description=f"Vous avez {newsletter_count} abonnés. Une liste de 100+ abonnés qualifiés génère des opportunités récurrentes.",
            action="Créer un lead magnet (ebook gratuit) et optimiser l'inscription newsletter",
            impact="Canal de communication direct avec prospects qualifiés",
            category="business"
        ))
    
    # Tri des recommandations par priorité
    priority_order = {"high": 3, "medium": 2, "low": 1}
    recommendations.sort(key=lambda x: priority_order.get(x.priority, 0), reverse=True)
    
    return recommendations[:8]  # Limiter à 8 recommandations max


@analytics_router.get("/export")
async def export_analytics_report(current_user: AdminUser = Depends(get_current_user)):
    """Exporte un rapport d'analyse complet"""
    
    dashboard_data = await get_analytics_dashboard(current_user)
    
    # Calculer des métriques supplémentaires pour le rapport
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "total_statistics": len(dashboard_data["statistics"]),
            "total_recommendations": len(dashboard_data["recommendations"]),
            "high_priority_actions": len([r for r in dashboard_data["recommendations"] if r["priority"] == "high"]),
        },
        "statistics": dashboard_data["statistics"],
        "recommendations": dashboard_data["recommendations"],
        "insights": await generate_insights(dashboard_data["statistics"])
    }
    
    return report


async def generate_insights(statistics: List[Dict]) -> Dict[str, Any]:
    """Génère des insights basés sur les données"""
    
    insights = {
        "strengths": [],
        "areas_for_improvement": [],
        "growth_opportunities": []
    }
    
    # Analyser les forces
    for stat in statistics:
        if stat.get("trend") == "positive" and int(stat["value"]) > 5:
            insights["strengths"].append(f"Excellent {stat['title'].lower()}: {stat['value']}{stat.get('suffix', '')}")
    
    # Analyser les zones d'amélioration
    for stat in statistics:
        if stat.get("trend") == "negative" or (stat.get("trend") == "neutral" and int(stat["value"]) < 3):
            insights["areas_for_improvement"].append(f"{stat['title']}: {stat['description']}")
    
    # Opportunités de croissance
    insights["growth_opportunities"] = [
        "Optimiser le SEO avec plus de contenu technique",
        "Développer des partenariats stratégiques",
        "Créer des formations en ligne",
        "Automatiser le processus de génération de leads"
    ]
    
    return insights