from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import os
from datetime import datetime

from models import (
    PersonalInfo, PersonalInfoCreate, PersonalInfoUpdate,
    SkillCategory, SkillCategoryCreate, SkillCategoryUpdate,
    Technology, TechnologyCreate, TechnologyUpdate,
    Project, ProjectCreate, ProjectUpdate,
    Service, ServiceCreate, ServiceUpdate,
    Testimonial, TestimonialCreate, TestimonialUpdate,
    Statistic, StatisticCreate, StatisticUpdate,
    SocialLink, SocialLinkCreate, SocialLinkUpdate,
    ProcessStep, ProcessStepCreate, ProcessStepUpdate,
    Resource, ResourceCreate, ResourceUpdate,
    BlogPost, BlogPostCreate, BlogPostUpdate,
    PendingTestimonial,
    AdminUser
)
from auth import get_current_user

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Create admin router
admin_router = APIRouter(prefix="/admin", tags=["admin"])


# ================== PERSONAL INFO ROUTES ==================

@admin_router.get("/personal", response_model=PersonalInfo)
async def get_personal_info(current_user: AdminUser = Depends(get_current_user)):
    """Get personal information (requires authentication)"""
    personal = await db.personal_info.find_one()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal information not found")
    return PersonalInfo(**personal)

@admin_router.post("/personal", response_model=PersonalInfo)
async def create_personal_info(
    personal_input: PersonalInfoCreate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Create personal information (requires authentication)"""
    # Check if personal info already exists
    existing = await db.personal_info.find_one()
    if existing:
        raise HTTPException(status_code=400, detail="Personal information already exists. Use PUT to update.")
    
    personal_dict = personal_input.dict()
    personal_obj = PersonalInfo(**personal_dict)
    await db.personal_info.insert_one(personal_obj.dict())
    return personal_obj

@admin_router.put("/personal", response_model=PersonalInfo)
async def update_personal_info(
    personal_input: PersonalInfoUpdate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Update personal information (requires authentication) (requires authentication)"""
    existing = await db.personal_info.find_one()
    if not existing:
        raise HTTPException(status_code=404, detail="Personal information not found")
    
    update_dict = personal_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    await db.personal_info.update_one(
        {"id": existing["id"]},
        {"$set": update_dict}
    )
    
    updated_personal = await db.personal_info.find_one({"id": existing["id"]})
    return PersonalInfo(**updated_personal)


# ================== SKILL CATEGORY ROUTES ==================

@admin_router.get("/skills", response_model=List[SkillCategory])
async def get_skill_categories(current_user: AdminUser = Depends(get_current_user)):
    """Get all skill categories (requires authentication)"""
    skills = await db.skill_categories.find().to_list(100)
    return [SkillCategory(**skill) for skill in skills]

@admin_router.get("/skills/{category_key}", response_model=SkillCategory)
async def get_skill_category(category_key: str, current_user: AdminUser = Depends(get_current_user)):
    """Get specific skill category (requires authentication)"""
    skill = await db.skill_categories.find_one({"category_key": category_key})
    if not skill:
        raise HTTPException(status_code=404, detail="Skill category not found")
    return SkillCategory(**skill)

@admin_router.post("/skills", response_model=SkillCategory)
async def create_skill_category(
    skill_input: SkillCategoryCreate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Create new skill category (requires authentication) (requires authentication)"""
    # Check if category_key already exists
    existing = await db.skill_categories.find_one({"category_key": skill_input.category_key})
    if existing:
        raise HTTPException(status_code=400, detail="Skill category with this key already exists")
    
    skill_dict = skill_input.dict()
    skill_obj = SkillCategory(**skill_dict)
    await db.skill_categories.insert_one(skill_obj.dict())
    return skill_obj

@admin_router.put("/skills/{skill_id}", response_model=SkillCategory)
async def update_skill_category(
    skill_id: str, 
    skill_input: SkillCategoryUpdate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Update skill category (requires authentication) (requires authentication)"""
    update_dict = skill_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.skill_categories.update_one(
        {"id": skill_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Skill category not found")
    
    updated_skill = await db.skill_categories.find_one({"id": skill_id})
    return SkillCategory(**updated_skill)

@admin_router.delete("/skills/{skill_id}")
async def delete_skill_category(
    skill_id: str,
    current_user: AdminUser = Depends(get_current_user)
):
    """Delete skill category (requires authentication) (requires authentication)"""
    result = await db.skill_categories.delete_one({"id": skill_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill category not found")
    return {"message": "Skill category deleted successfully"}


# ================== TECHNOLOGY ROUTES ==================

@admin_router.get("/technologies", response_model=List[Technology])
async def get_technologies(current_user: AdminUser = Depends(get_current_user)):
    """Get all technologies (requires authentication)"""
    techs = await db.technologies.find().sort("name", 1).to_list(100)
    return [Technology(**tech) for tech in techs]

@admin_router.post("/technologies", response_model=Technology)
async def create_technology(
    tech_input: TechnologyCreate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Create new technology (requires authentication) (requires authentication)"""
    tech_dict = tech_input.dict()
    tech_obj = Technology(**tech_dict)
    await db.technologies.insert_one(tech_obj.dict())
    return tech_obj

@admin_router.put("/technologies/{tech_id}", response_model=Technology)
async def update_technology(
    tech_id: str, 
    tech_input: TechnologyUpdate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Update technology (requires authentication) (requires authentication)"""
    update_dict = tech_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.technologies.update_one(
        {"id": tech_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Technology not found")
    
    updated_tech = await db.technologies.find_one({"id": tech_id})
    return Technology(**updated_tech)

@admin_router.delete("/technologies/{tech_id}")
async def delete_technology(
    tech_id: str,
    current_user: AdminUser = Depends(get_current_user)
):
    """Delete technology (requires authentication) (requires authentication)"""
    result = await db.technologies.delete_one({"id": tech_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Technology not found")
    return {"message": "Technology deleted successfully"}


# ================== PROJECT ROUTES ==================

@admin_router.get("/projects", response_model=List[Project])
async def get_projects(current_user: AdminUser = Depends(get_current_user)):
    """Get all projects (requires authentication)"""
    projects = await db.projects.find().sort("order_index", 1).to_list(100)
    return [Project(**project) for project in projects]

@admin_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Get specific project (requires authentication)"""
    project = await db.projects.find_one({"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return Project(**project)

@admin_router.post("/projects", response_model=Project)
async def create_project(
    project_input: ProjectCreate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Create new project (requires authentication) (requires authentication)"""
    project_dict = project_input.dict()
    project_obj = Project(**project_dict)
    await db.projects.insert_one(project_obj.dict())
    return project_obj

@admin_router.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: str, 
    project_input: ProjectUpdate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Update project (requires authentication) (requires authentication)"""
    update_dict = project_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.projects.update_one(
        {"id": project_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    updated_project = await db.projects.find_one({"id": project_id})
    return Project(**updated_project)

@admin_router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    current_user: AdminUser = Depends(get_current_user)
):
    """Delete project (requires authentication) (requires authentication)"""
    result = await db.projects.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


# ================== SERVICE ROUTES ==================

@admin_router.get("/services", response_model=List[Service])
async def get_services(current_user: AdminUser = Depends(get_current_user)):
    """Get all services (requires authentication)"""
    services = await db.services.find().sort("order_index", 1).to_list(100)
    return [Service(**service) for service in services]

@admin_router.get("/services/{service_id}", response_model=Service)
async def get_service(service_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Get specific service (requires authentication)"""
    service = await db.services.find_one({"id": service_id})
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return Service(**service)

@admin_router.post("/services", response_model=Service)
async def create_service(service_input: ServiceCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new service (requires authentication)"""
    service_dict = service_input.dict()
    service_obj = Service(**service_dict)
    await db.services.insert_one(service_obj.dict())
    return service_obj

@admin_router.put("/services/{service_id}", response_model=Service)
async def update_service(service_id: str, service_input: ServiceUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update service (requires authentication)"""
    update_dict = service_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.services.update_one(
        {"id": service_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    updated_service = await db.services.find_one({"id": service_id})
    return Service(**updated_service)

@admin_router.delete("/services/{service_id}")
async def delete_service(service_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete service (requires authentication)"""
    result = await db.services.delete_one({"id": service_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}


# ================== TESTIMONIAL ROUTES ==================

# IMPORTANT: Routes plus spécifiques (avec /pending) DOIVENT être avant les routes avec paramètres
@admin_router.get("/testimonials/pending", response_model=List[PendingTestimonial])
async def get_pending_testimonials(current_user: AdminUser = Depends(get_current_user)):
    """Get all pending testimonials (requires authentication)"""
    testimonials = await db.pending_testimonials.find({"status": "pending"}).sort("submitted_at", -1).to_list(100)
    return [PendingTestimonial(**testimonial) for testimonial in testimonials]

@admin_router.put("/testimonials/pending/{testimonial_id}/approve")
async def approve_testimonial(testimonial_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Approve pending testimonial and move to testimonials (requires authentication)"""
    pending = await db.pending_testimonials.find_one({"id": testimonial_id})
    if not pending:
        raise HTTPException(status_code=404, detail="Pending testimonial not found")
    
    # Create testimonial from pending
    testimonial_data = {
        "name": pending["name"],
        "role": pending.get("role", "Client"),
        "company": pending.get("company", ""),
        "content": pending["content"],
        "rating": pending["rating"],
        "featured": False
    }
    
    testimonial_obj = Testimonial(**testimonial_data)
    await db.testimonials.insert_one(testimonial_obj.dict())
    
    # Update pending status
    await db.pending_testimonials.update_one(
        {"id": testimonial_id},
        {"$set": {"status": "approved", "reviewed_at": datetime.utcnow()}}
    )
    
    return {"message": "Testimonial approved and added"}

@admin_router.put("/testimonials/pending/{testimonial_id}/reject")
async def reject_testimonial(testimonial_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Reject pending testimonial (requires authentication)"""
    result = await db.pending_testimonials.update_one(
        {"id": testimonial_id},
        {"$set": {"status": "rejected", "reviewed_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pending testimonial not found")
    
    return {"message": "Testimonial rejected"}

@admin_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials(current_user: AdminUser = Depends(get_current_user)):
    """Get all testimonials (requires authentication)"""
    testimonials = await db.testimonials.find().sort("order_index", 1).to_list(100)
    return [Testimonial(**testimonial) for testimonial in testimonials]

@admin_router.get("/testimonials/{testimonial_id}", response_model=Testimonial)
async def get_testimonial(testimonial_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Get specific testimonial (requires authentication)"""
    testimonial = await db.testimonials.find_one({"id": testimonial_id})
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return Testimonial(**testimonial)

@admin_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial_input: TestimonialCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new testimonial (requires authentication)"""
    testimonial_dict = testimonial_input.dict()
    testimonial_obj = Testimonial(**testimonial_dict)
    await db.testimonials.insert_one(testimonial_obj.dict())
    return testimonial_obj

@admin_router.put("/testimonials/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(testimonial_id: str, testimonial_input: TestimonialUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update testimonial (requires authentication)"""
    update_dict = testimonial_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.testimonials.update_one(
        {"id": testimonial_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    updated_testimonial = await db.testimonials.find_one({"id": testimonial_id})
    return Testimonial(**updated_testimonial)

@admin_router.delete("/testimonials/{testimonial_id}")
async def delete_testimonial(testimonial_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete testimonial (requires authentication)"""
    result = await db.testimonials.delete_one({"id": testimonial_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return {"message": "Testimonial deleted successfully"}


# ================== STATISTICS ROUTES ==================

@admin_router.get("/statistics", response_model=List[Statistic])
async def get_statistics(current_user: AdminUser = Depends(get_current_user)):
    """Get all statistics (requires authentication)"""
    stats = await db.statistics.find().sort("order_index", 1).to_list(100)
    return [Statistic(**stat) for stat in stats]

@admin_router.post("/statistics", response_model=Statistic)
async def create_statistic(stat_input: StatisticCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new statistic (requires authentication)"""
    stat_dict = stat_input.dict()
    stat_obj = Statistic(**stat_dict)
    await db.statistics.insert_one(stat_obj.dict())
    return stat_obj

@admin_router.put("/statistics/{stat_id}", response_model=Statistic)
async def update_statistic(stat_id: str, stat_input: StatisticUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update statistic (requires authentication)"""
    update_dict = stat_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.statistics.update_one(
        {"id": stat_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Statistic not found")
    
    updated_stat = await db.statistics.find_one({"id": stat_id})
    return Statistic(**updated_stat)

@admin_router.delete("/statistics/{stat_id}")
async def delete_statistic(stat_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete statistic (requires authentication)"""
    result = await db.statistics.delete_one({"id": stat_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return {"message": "Statistic deleted successfully"}


# ================== SOCIAL LINKS ROUTES ==================

@admin_router.get("/social-links", response_model=List[SocialLink])
async def get_social_links(current_user: AdminUser = Depends(get_current_user)):
    """Get all social links (requires authentication)"""
    links = await db.social_links.find().sort("order_index", 1).to_list(100)
    return [SocialLink(**link) for link in links]

@admin_router.post("/social-links", response_model=SocialLink)
async def create_social_link(link_input: SocialLinkCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new social link (requires authentication)"""
    link_dict = link_input.dict()
    link_obj = SocialLink(**link_dict)
    await db.social_links.insert_one(link_obj.dict())
    return link_obj

@admin_router.put("/social-links/{link_id}", response_model=SocialLink)
async def update_social_link(link_id: str, link_input: SocialLinkUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update social link (requires authentication)"""
    update_dict = link_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.social_links.update_one(
        {"id": link_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Social link not found")
    
    updated_link = await db.social_links.find_one({"id": link_id})
    return SocialLink(**updated_link)

@admin_router.delete("/social-links/{link_id}")
async def delete_social_link(link_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete social link (requires authentication)"""
    result = await db.social_links.delete_one({"id": link_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Social link not found")
    return {"message": "Social link deleted successfully"}


# ================== PROCESS STEPS ROUTES ==================

@admin_router.get("/process-steps", response_model=List[ProcessStep])
async def get_process_steps(current_user: AdminUser = Depends(get_current_user)):
    """Get all process steps (requires authentication)"""
    steps = await db.process_steps.find().sort("step", 1).to_list(100)
    return [ProcessStep(**step) for step in steps]

@admin_router.post("/process-steps", response_model=ProcessStep)
async def create_process_step(step_input: ProcessStepCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new process step (requires authentication)"""
    step_dict = step_input.dict()
    step_obj = ProcessStep(**step_dict)
    await db.process_steps.insert_one(step_obj.dict())
    return step_obj

@admin_router.put("/process-steps/{step_id}", response_model=ProcessStep)
async def update_process_step(step_id: str, step_input: ProcessStepUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update process step (requires authentication)"""
    update_dict = step_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.process_steps.update_one(
        {"id": step_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Process step not found")
    
    updated_step = await db.process_steps.find_one({"id": step_id})
    return ProcessStep(**updated_step)

@admin_router.delete("/process-steps/{step_id}")
async def delete_process_step(step_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete process step (requires authentication)"""
    result = await db.process_steps.delete_one({"id": step_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Process step not found")
    return {"message": "Process step deleted successfully"}


# ================== RESOURCE ROUTES ==================

@admin_router.get("/resources", response_model=List[Resource])
async def get_resources(current_user: AdminUser = Depends(get_current_user)):
    """Get all resources (requires authentication)"""
    resources = await db.resources.find().sort("created_at", -1).to_list(100)
    return [Resource(**resource) for resource in resources]

@admin_router.get("/resources/{resource_id}", response_model=Resource)
async def get_resource(resource_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Get specific resource (requires authentication)"""
    resource = await db.resources.find_one({"id": resource_id})
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return Resource(**resource)

@admin_router.post("/resources", response_model=Resource)
async def create_resource(resource_input: ResourceCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new resource (requires authentication)"""
    resource_dict = resource_input.dict()
    resource_obj = Resource(**resource_dict)
    await db.resources.insert_one(resource_obj.dict())
    return resource_obj

@admin_router.put("/resources/{resource_id}", response_model=Resource)
async def update_resource(resource_id: str, resource_input: ResourceUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update resource (requires authentication)"""
    update_dict = resource_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.resources.update_one(
        {"id": resource_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    updated_resource = await db.resources.find_one({"id": resource_id})
    return Resource(**updated_resource)

@admin_router.delete("/resources/{resource_id}")
async def delete_resource(resource_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete resource (requires authentication)"""
    result = await db.resources.delete_one({"id": resource_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Resource deleted successfully"}


# ================== BLOG ROUTES ==================

@admin_router.get("/blog", response_model=List[BlogPost])
async def get_blog_posts(current_user: AdminUser = Depends(get_current_user)):
    """Get all blog posts (requires authentication)"""
    posts = await db.blog_posts.find().sort("created_at", -1).to_list(100)
    return [BlogPost(**post) for post in posts]

@admin_router.get("/blog/{post_id}", response_model=BlogPost)
async def get_blog_post(post_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Get specific blog post (requires authentication)"""
    post = await db.blog_posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return BlogPost(**post)

@admin_router.post("/blog", response_model=BlogPost)
async def create_blog_post(post_input: BlogPostCreate, current_user: AdminUser = Depends(get_current_user)):
    """Create new blog post (requires authentication)"""
    post_dict = post_input.dict()
    # Set published_at if publishing
    if post_dict.get("published", False):
        post_dict["published_at"] = datetime.utcnow()
    
    post_obj = BlogPost(**post_dict)
    await db.blog_posts.insert_one(post_obj.dict())
    return post_obj

@admin_router.put("/blog/{post_id}", response_model=BlogPost)
async def update_blog_post(post_id: str, post_input: BlogPostUpdate, current_user: AdminUser = Depends(get_current_user)):
    """Update blog post (requires authentication)"""
    update_dict = post_input.dict(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    
    # Set published_at if publishing for first time
    if update_dict.get("published", False):
        existing_post = await db.blog_posts.find_one({"id": post_id})
        if existing_post and not existing_post.get("published_at"):
            update_dict["published_at"] = datetime.utcnow()
    
    result = await db.blog_posts.update_one(
        {"id": post_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    updated_post = await db.blog_posts.find_one({"id": post_id})
    return BlogPost(**updated_post)

@admin_router.delete("/blog/{post_id}")
async def delete_blog_post(post_id: str, current_user: AdminUser = Depends(get_current_user)):
    """Delete blog post (requires authentication)"""
    result = await db.blog_posts.delete_one({"id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}

