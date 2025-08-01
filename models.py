from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


# Personal Information Model
class PersonalInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    title: str
    subtitle: str
    bio: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PersonalInfoCreate(BaseModel):
    name: str
    title: str
    subtitle: str
    bio: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[str] = None
    website: Optional[str] = None

class PersonalInfoUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[str] = None
    website: Optional[str] = None


# Skill Models
class SkillItem(BaseModel):
    name: str
    level: int  # 0-100

class SkillCategory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    icon: str
    items: List[SkillItem] = []
    category_key: str  # cybersecurity, python, network, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SkillCategoryCreate(BaseModel):
    title: str
    icon: str
    items: List[SkillItem] = []
    category_key: str

class SkillCategoryUpdate(BaseModel):
    title: Optional[str] = None
    icon: Optional[str] = None
    items: Optional[List[SkillItem]] = None


# Technology Model
class Technology(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: str
    level: str = "intermediate"  # beginner, intermediate, advanced, expert
    color: str = "#3b82f6"  # Hex color for display
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TechnologyCreate(BaseModel):
    name: str
    category: str
    level: str = "intermediate"
    color: str = "#3b82f6"

class TechnologyUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    color: Optional[str] = None


# Project Model
class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str
    level: str  # Débutant, Intermédiaire, Avancé
    description: str
    technologies: List[str] = []
    features: List[str] = []
    status: str  # Terminé, En cours, Planifié
    duration: str
    github: Optional[str] = None
    demo: Optional[str] = None
    order_index: Optional[int] = None  # For sorting
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(BaseModel):
    title: str
    category: str
    level: str
    description: str
    technologies: List[str] = []
    features: List[str] = []
    status: str
    duration: str
    github: Optional[str] = None
    demo: Optional[str] = None
    order_index: Optional[int] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    features: Optional[List[str]] = None
    status: Optional[str] = None
    duration: Optional[str] = None
    github: Optional[str] = None
    demo: Optional[str] = None
    order_index: Optional[int] = None


# Service Model
class Service(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    icon: str
    description: str
    features: List[str] = []
    price: str
    duration: str
    order_index: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ServiceCreate(BaseModel):
    title: str
    icon: str
    description: str
    features: List[str] = []
    price: str
    duration: str
    order_index: Optional[int] = None

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    order_index: Optional[int] = None


# Testimonial Model
class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str
    company: str
    content: str
    rating: int  # 1-5 stars
    order_index: Optional[int] = None
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TestimonialCreate(BaseModel):
    name: str
    role: str
    company: str
    content: str
    rating: int
    order_index: Optional[int] = None
    featured: bool = False

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None
    order_index: Optional[int] = None
    featured: Optional[bool] = None


# Statistics Model
class Statistic(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    value: str
    suffix: Optional[str] = None
    description: Optional[str] = None
    icon: str
    color: str = "#3b82f6"
    order_index: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StatisticCreate(BaseModel):
    title: str
    value: str
    suffix: Optional[str] = None
    description: Optional[str] = None
    icon: str
    color: str = "#3b82f6"
    order_index: Optional[int] = None

class StatisticUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[str] = None
    suffix: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    order_index: Optional[int] = None


# Social Link Model
class SocialLink(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    url: str
    icon: str
    order_index: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SocialLinkCreate(BaseModel):
    name: str
    url: str
    icon: str
    order_index: Optional[int] = None

class SocialLinkUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    order_index: Optional[int] = None


# Process Step Model
class ProcessStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step: int
    title: str
    description: str
    icon: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProcessStepCreate(BaseModel):
    step: int
    title: str
    description: str
    icon: str

class ProcessStepUpdate(BaseModel):
    step: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


# Admin User Model (for authentication)
class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class AdminUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# Resource Model (for downloads/guides)
class Resource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str  # Guide, Template, Script, Tool, etc.
    type: str  # PDF, ZIP, DOC, etc.
    size: str  # e.g., "2.5 MB"
    pages: Optional[int] = None
    downloads: int = 0
    rating: float = 0.0
    featured: bool = False
    tags: List[str] = []
    difficulty: Optional[str] = "Débutant"
    download_url: Optional[str] = None
    file_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ResourceCreate(BaseModel):
    title: str
    description: str
    category: str
    type: str
    size: str
    pages: Optional[int] = None
    rating: float = 0.0
    featured: bool = False
    tags: List[str] = []
    difficulty: Optional[str] = "Débutant"
    download_url: Optional[str] = None
    file_path: Optional[str] = None

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    size: Optional[str] = None
    pages: Optional[int] = None
    rating: Optional[float] = None
    featured: Optional[bool] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[str] = None
    download_url: Optional[str] = None
    file_path: Optional[str] = None


# Blog Post Model
class BlogPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str  # URL-friendly version of title
    excerpt: str  # Short description
    content: str  # Full blog content
    category: str  # Cybersécurité, Python, Tutoriel, etc.
    tags: List[str] = []
    featured_image: Optional[str] = None
    published: bool = False
    featured: bool = False
    views: int = 0
    reading_time: int = 5  # minutes
    author: str = "Jean Yves"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None

class BlogPostCreate(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    category: str
    tags: List[str] = []
    featured_image: Optional[str] = None
    published: bool = False
    featured: bool = False
    reading_time: int = 5
    author: str = "Jean Yves"

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    featured_image: Optional[str] = None
    published: Optional[bool] = None
    featured: Optional[bool] = None
    reading_time: Optional[int] = None
    author: Optional[str] = None


# Public Testimonial Submission (for visitors)
class PublicTestimonialSubmission(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    role: Optional[str] = None
    content: str
    rating: int  # 1-5
    service_used: Optional[str] = None  # Which service they used

class PendingTestimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    company: Optional[str] = None
    role: Optional[str] = None
    content: str
    rating: int
    service_used: Optional[str] = None
    status: str = "pending"  # pending, approved, rejected
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None