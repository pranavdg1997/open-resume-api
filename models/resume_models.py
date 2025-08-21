"""
Resume data models based on OpenResume's structure
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum

class PersonalInfo(BaseModel):
    """Personal information section"""
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    url: Optional[str] = Field(None, description="Personal website or portfolio URL")
    summary: Optional[str] = Field(None, max_length=500, description="Professional summary")
    location: Optional[str] = Field(None, max_length=100, description="Location (city, state)")

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', '').isdigit():
            raise ValueError('Invalid phone number format')
        return v

class WorkExperience(BaseModel):
    """Work experience entry"""
    company: str = Field(..., min_length=1, max_length=100, description="Company name")
    jobTitle: str = Field(..., min_length=1, max_length=100, description="Job title")
    date: str = Field(..., description="Date range (e.g., 'Jan 2020 - Present')")
    descriptions: List[str] = Field(default_factory=list, description="Job responsibilities and achievements")

    @validator('descriptions')
    def validate_descriptions(cls, v):
        return [desc.strip() for desc in v if desc.strip()]

class Education(BaseModel):
    """Education entry"""
    school: str = Field(..., min_length=1, max_length=100, description="School name")
    degree: str = Field(..., min_length=1, max_length=100, description="Degree and major")
    date: str = Field(..., description="Date range or graduation date")
    gpa: Optional[str] = Field(None, description="GPA (optional)")
    descriptions: List[str] = Field(default_factory=list, description="Additional details")

class Project(BaseModel):
    """Project entry"""
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    date: str = Field(..., description="Project date or date range")
    descriptions: List[str] = Field(default_factory=list, description="Project details and achievements")

class Skill(BaseModel):
    """Skill category"""
    category: str = Field(..., min_length=1, max_length=50, description="Skill category name")
    skills: List[str] = Field(..., description="List of skills in this category")

    @validator('skills')
    def validate_skills(cls, v):
        return [skill.strip() for skill in v if skill.strip()]

class Custom(BaseModel):
    """Custom section"""
    descriptions: List[str] = Field(default_factory=list, description="Custom section content")

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
            "custom": "ADDITIONAL"
        },
        description="Section headings mapping"
    )
    formToShow: Optional[Dict[str, bool]] = Field(
        default_factory=lambda: {
            "workExperiences": True,
            "educations": True,
            "projects": True,
            "skills": True,
            "custom": True
        },
        description="Section visibility settings"
    )

class ResumeData(BaseModel):
    """Complete resume data structure"""
    personalInfo: PersonalInfo
    workExperiences: List[WorkExperience] = Field(default_factory=list)
    educations: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    custom: Custom = Field(default_factory=Custom)
    settings: ResumeSettings = Field(default_factory=lambda: ResumeSettings())

    class Config:
        schema_extra = {
            "example": {
                "personalInfo": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1 (555) 123-4567",
                    "url": "https://johndoe.dev",
                    "summary": "Experienced software engineer with expertise in full-stack development",
                    "location": "San Francisco, CA"
                },
                "workExperiences": [
                    {
                        "company": "Tech Corp",
                        "jobTitle": "Senior Software Engineer",
                        "date": "Jan 2020 - Present",
                        "descriptions": [
                            "Led development of microservices architecture",
                            "Reduced system latency by 40%"
                        ]
                    }
                ],
                "educations": [
                    {
                        "school": "University of California",
                        "degree": "Bachelor of Science in Computer Science",
                        "date": "2016 - 2020",
                        "gpa": "3.8/4.0",
                        "descriptions": []
                    }
                ],
                "projects": [
                    {
                        "name": "Resume Builder API",
                        "date": "2023",
                        "descriptions": [
                            "Built REST API using FastAPI",
                            "Integrated PDF generation capabilities"
                        ]
                    }
                ],
                "skills": [
                    {
                        "category": "Programming Languages",
                        "skills": ["Python", "JavaScript", "TypeScript", "Java"]
                    },
                    {
                        "category": "Technologies",
                        "skills": ["React", "FastAPI", "Docker", "AWS"]
                    }
                ],
                "custom": {
                    "descriptions": ["Available for remote work"]
                }
            }
        }

class ResumeResponse(BaseModel):
    """Response model for resume generation"""
    success: bool
    message: str
    filename: Optional[str] = None
    size: Optional[int] = None
    generated_at: Optional[str] = None
    
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str
    status_code: int
    details: Optional[Dict[str, Any]] = None
