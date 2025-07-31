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
    icon: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TechnologyCreate(BaseModel):
    name: str
    category: str
    icon: str

class TechnologyUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None


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
    label: str
    value: str
    icon: str
    order_index: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StatisticCreate(BaseModel):
    label: str
    value: str
    icon: str
    order_index: Optional[int] = None

class StatisticUpdate(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    icon: Optional[str] = None
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None