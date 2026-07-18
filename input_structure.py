"""
Pydantic models defining the JSON schema for a resume.

These classes mirror the structure expected by the API for
`POST /api/v1/generate-resume`.

The original models live in `models/resume_models.py`, but a
separate file can be useful for documentation or tooling that
imports only the input structure.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# 1. Personal information
# ---------------------------------------------------------------------------
class PersonalInfo(BaseModel):
    """Personal information section"""
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    url: Optional[str] = Field(None, description="Personal website or portfolio URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    summary: Optional[str] = Field(None, max_length=500, description="Professional summary")
    location: Optional[str] = Field(None, max_length=100, description="Location (city, state)")

# ---------------------------------------------------------------------------
# 2. Work experience
# ---------------------------------------------------------------------------
class WorkExperience(BaseModel):
    """Work experience entry"""
    company: str = Field(..., min_length=1, max_length=100, description="Company name")
    jobTitle: str = Field(..., min_length=1, max_length=100, description="Job title")
    date: str = Field(..., description="Date range (e.g., 'Jan 2020 - Present')")
    location: Optional[str] = Field(None, max_length=100, description="Job location (e.g., 'San Jose, CA')")
    descriptions: List[str] = Field(default_factory=list, description="Job responsibilities and achievements")

# ---------------------------------------------------------------------------
# 3. Education
# ---------------------------------------------------------------------------
class Education(BaseModel):
    """Education entry"""
    school: str = Field(..., min_length=1, max_length=100, description="School name")
    degree: str = Field(..., min_length=1, max_length=100, description="Degree and major")
    date: str = Field(..., description="Date range or graduation date")
    gpa: Optional[str] = Field(None, description="GPA (optional)")
    descriptions: List[str] = Field(default_factory=list, description="Additional details")

# ---------------------------------------------------------------------------
# 4. Project
# ---------------------------------------------------------------------------
class Project(BaseModel):
    """Project entry with structured format similar to work experience"""
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    company: Optional[str] = Field(None, max_length=100, description="Company or organization (optional)")
    date: str = Field(..., description="Project date or date range")
    descriptions: List[str] = Field(default_factory=list, description="Project details and achievements")

# ---------------------------------------------------------------------------
# 5. Skill category
# ---------------------------------------------------------------------------
class Skill(BaseModel):
    """Skill category"""
    category: str = Field(..., min_length=1, max_length=50, description="Skill category name")
    skills: List[str] = Field(..., description="List of skills in this category")

# ---------------------------------------------------------------------------
# 6. Publication
# ---------------------------------------------------------------------------
class Publication(BaseModel):
    """Publication entry"""
    name: str = Field(..., min_length=1, max_length=200, description="Publication title")
    date: str = Field(..., description="Publication date")
    descriptions: List[str] = Field(default_factory=list, description="Publication details")

# ---------------------------------------------------------------------------
# 7. Certification
# ---------------------------------------------------------------------------
class Certification(BaseModel):
    """Certification entry"""
    name: str = Field(..., min_length=1, max_length=100, description="Certification name")
    date: str = Field(..., description="Certification date")
    url: Optional[str] = Field(None, description="Certification verification URL")
    org: Optional[str] = Field(None, max_length=100, description="Awarding organization")
    descriptions: List[str] = Field(default_factory=list, description="Certification details")

# ---------------------------------------------------------------------------
# 8. Custom section
# ---------------------------------------------------------------------------
class Custom(BaseModel):
    """Custom section"""
    descriptions: List[str] = Field(default_factory=list, description="Custom section content")

# ---------------------------------------------------------------------------
# 9. Resume settings
# ---------------------------------------------------------------------------
class ResumeSettings(BaseModel):
    """Resume styling and formatting settings"""
    themeColor: Optional[str] = Field("#1f2937", description="Theme color (hex)")
    fontFamily: Optional[str] = Field("OpenSans", description="Font family")
    fontSize: Optional[str] = Field("11", description="Font size")
    documentSize: Optional[str] = Field("Letter", description="Document size")
    formToHeading: Optional[Dict[str, str]] = Field(
        default_factory=lambda: {
            "workExperiences": "WORK EXPERIENCE",
            "educations": "EDUCATION",
            "projects": "PROJECTS",
            "skills": "SKILLS",
            "custom": "ADDITIONAL",
        },
        description="Section headings mapping",
    )
    formToShow: Optional[Dict[str, bool]] = Field(
        default_factory=lambda: {
            "workExperiences": True,
            "educations": True,
            "projects": True,
            "skills": True,
            "custom": True,
        },
        description="Section visibility settings",
    )

# ---------------------------------------------------------------------------
# 10. Full resume data structure
# ---------------------------------------------------------------------------
class ResumeData(BaseModel):
    """Complete resume data structure"""
    personalInfo: PersonalInfo
    workExperiences: List[WorkExperience] = Field(default_factory=list)
    educations: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    publications: List[Publication] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    custom: Custom = Field(default_factory=Custom)
    settings: ResumeSettings = Field(default_factory=lambda: ResumeSettings())

# ---------------------------------------------------------------------------
# 11. Response models (optional but useful for completeness)
# ---------------------------------------------------------------------------
class ResumeResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    size: Optional[int] = None
    generated_at: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    details: Optional[Dict] = None

__all__ = [
    "PersonalInfo",
    "WorkExperience",
    "Education",
    "Project",
    "Skill",
    "Publication",
    "Certification",
    "Custom",
    "ResumeSettings",
    "ResumeData",
    "ResumeResponse",
    "ErrorResponse",
]
