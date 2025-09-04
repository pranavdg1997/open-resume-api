"""
Validation utilities for resume data
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError
import logging

from models.resume_models import ResumeData, PersonalInfo, WorkExperience, Education, Project, Skill
from services.config_manager import ConfigManager
import constants

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of validation operation"""
    is_valid: bool
    issues: List[str]
    warnings: List[str]
    sections_validated: List[str]

class ResumeValidator:
    """Comprehensive resume data validator"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.validation_settings = config_manager.get_validation_settings()
    
    def validate_complete_resume(self, resume_data: ResumeData) -> ValidationResult:
        """Validate complete resume data"""
        issues = []
        warnings = []
        sections_validated = []
        
        # Validate personal info (required)
        personal_result = self.validate_personal_info(resume_data.personalInfo)
        issues.extend(personal_result.issues)
        warnings.extend(personal_result.warnings)
        sections_validated.extend(personal_result.sections_validated)
        
        # Validate work experiences
        if resume_data.workExperiences:
            work_result = self.validate_work_experiences(resume_data.workExperiences)
            issues.extend(work_result.issues)
            warnings.extend(work_result.warnings)
            sections_validated.extend(work_result.sections_validated)
        
        # Validate educations
        if resume_data.educations:
            edu_result = self.validate_educations(resume_data.educations)
            issues.extend(edu_result.issues)
            warnings.extend(edu_result.warnings)
            sections_validated.extend(edu_result.sections_validated)
        
        # Validate projects
        if resume_data.projects:
            proj_result = self.validate_projects(resume_data.projects)
            issues.extend(proj_result.issues)
            warnings.extend(proj_result.warnings)
            sections_validated.extend(proj_result.sections_validated)
        
        # Validate skills
        if resume_data.skills:
            skills_result = self.validate_skills(resume_data.skills)
            issues.extend(skills_result.issues)
            warnings.extend(skills_result.warnings)
            sections_validated.extend(skills_result.sections_validated)
        
        # Validate settings
        settings_result = self.validate_settings(resume_data.settings)
        issues.extend(settings_result.issues)
        warnings.extend(settings_result.warnings)
        sections_validated.extend(settings_result.sections_validated)
        
        # Overall content warnings
        if not any([resume_data.workExperiences, resume_data.educations, resume_data.projects]):
            warnings.append("Resume has no work experience, education, or projects sections")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=list(set(sections_validated))
        )
    
    def validate_personal_info(self, personal_info: PersonalInfo) -> ValidationResult:
        """Validate personal information"""
        issues = []
        warnings = []
        
        # Required fields validation
        required_fields = self.validation_settings.get("required_fields", ["name", "email"])
        
        if "name" in required_fields and not personal_info.name.strip():
            issues.append("Name is required")
        
        if "email" in required_fields:
            if not personal_info.email:
                issues.append("Email is required")
            else:
                try:
                    validate_email(personal_info.email)
                except EmailNotValidError as e:
                    issues.append(f"Invalid email address: {str(e)}")
        
        # Phone validation
        if personal_info.phone:
            phone_pattern = re.compile(r'^[\+]?[1-9]?[\d\s\-\(\)\.]{7,15}$')
            if not phone_pattern.match(personal_info.phone.replace(' ', '')):
                warnings.append("Phone number format may not be recognized by all systems")
        
        # URL validation
        if personal_info.url:
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if not url_pattern.match(personal_info.url):
                warnings.append("URL format should include http:// or https://")
        
        # Summary length validation
        if personal_info.summary:
            max_summary_length = constants.MAX_SUMMARY_LENGTH
            if len(personal_info.summary) > max_summary_length:
                issues.append(f"Summary exceeds maximum length of {max_summary_length} characters")
            
            if len(personal_info.summary) < 50:
                warnings.append("Summary is quite short - consider adding more details")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=["personal_info"]
        )
    
    def validate_work_experiences(self, work_experiences: List[WorkExperience]) -> ValidationResult:
        """Validate work experiences"""
        issues = []
        warnings = []
        
        max_experiences = self.validation_settings.get("max_work_experiences", 10)
        max_desc_length = self.validation_settings.get("max_description_length", 200)
        
        if len(work_experiences) > max_experiences:
            issues.append(f"Too many work experiences (max: {max_experiences})")
        
        for i, exp in enumerate(work_experiences):
            prefix = f"Work Experience {i+1}:"
            
            # Required fields
            if not exp.company.strip():
                issues.append(f"{prefix} Company name is required")
            
            if not exp.jobTitle.strip():
                issues.append(f"{prefix} Job title is required")
            
            if not exp.date.strip():
                issues.append(f"{prefix} Date is required")
            
            # Description validation
            if not exp.descriptions:
                warnings.append(f"{prefix} No job descriptions provided")
            else:
                for j, desc in enumerate(exp.descriptions):
                    if len(desc) > max_desc_length:
                        warnings.append(f"{prefix} Description {j+1} exceeds recommended length ({max_desc_length} chars)")
                    if len(desc.strip()) < 10:
                        warnings.append(f"{prefix} Description {j+1} is very short")
            
            # Date format validation
            common_date_patterns = constants.DATE_PATTERNS
            
            if not any(re.match(pattern, exp.date) for pattern in common_date_patterns):
                warnings.append(f"{prefix} Date format may not be standard (consider 'MMM YYYY - MMM YYYY' format)")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=["work_experience"]
        )
    
    def validate_educations(self, educations: List[Education]) -> ValidationResult:
        """Validate education entries"""
        issues = []
        warnings = []
        
        max_educations = self.validation_settings.get("max_educations", 5)
        
        if len(educations) > max_educations:
            issues.append(f"Too many education entries (max: {max_educations})")
        
        for i, edu in enumerate(educations):
            prefix = f"Education {i+1}:"
            
            # Required fields
            if not edu.school.strip():
                issues.append(f"{prefix} School name is required")
            
            if not edu.degree.strip():
                issues.append(f"{prefix} Degree is required")
            
            if not edu.date.strip():
                issues.append(f"{prefix} Date is required")
            
            # GPA validation
            if edu.gpa:
                try:
                    gpa_value = float(edu.gpa.split('/')[0])
                    if gpa_value > constants.MAX_GPA_VALUE:
                        warnings.append(f"{prefix} GPA seems high (>{constants.MAX_GPA_VALUE}) - verify format")
                except (ValueError, IndexError):
                    warnings.append(f"{prefix} GPA format not recognized - consider using 'X.X/4.0' format")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=["education"]
        )
    
    def validate_projects(self, projects: List[Project]) -> ValidationResult:
        """Validate project entries"""
        issues = []
        warnings = []
        
        max_projects = self.validation_settings.get("max_projects", 10)
        max_desc_length = self.validation_settings.get("max_description_length", 200)
        
        if len(projects) > max_projects:
            issues.append(f"Too many projects (max: {max_projects})")
        
        for i, project in enumerate(projects):
            prefix = f"Project {i+1}:"
            
            # Required fields
            if not project.name.strip():
                issues.append(f"{prefix} Project name is required")
            
            if not project.date.strip():
                issues.append(f"{prefix} Date is required")
            
            # Description validation
            if not project.descriptions:
                warnings.append(f"{prefix} No project descriptions provided")
            else:
                for j, desc in enumerate(project.descriptions):
                    if len(desc) > max_desc_length:
                        warnings.append(f"{prefix} Description {j+1} exceeds recommended length ({max_desc_length} chars)")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=["projects"]
        )
    
    def validate_skills(self, skills: List[Skill]) -> ValidationResult:
        """Validate skills section"""
        issues = []
        warnings = []
        
        max_categories = self.validation_settings.get("max_skills_categories", 10)
        
        if len(skills) > max_categories:
            issues.append(f"Too many skill categories (max: {max_categories})")
        
        for i, skill_group in enumerate(skills):
            prefix = f"Skill Category {i+1}:"
            
            if not skill_group.category.strip():
                issues.append(f"{prefix} Category name is required")
            
            if not skill_group.skills:
                issues.append(f"{prefix} No skills listed in category")
            
            if len(skill_group.skills) > 20:
                warnings.append(f"{prefix} Many skills listed - consider grouping or prioritizing")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=["skills"]
        )
    
    def validate_settings(self, settings) -> ValidationResult:
        """Validate resume settings"""
        issues = []
        warnings = []
        
        # Color validation
        if settings.themeColor:
            color_pattern = re.compile(constants.COLOR_PATTERN)
            if not color_pattern.match(settings.themeColor):
                issues.append("Theme color must be a valid hex color (e.g., #1f2937)")
        
        # Font size validation
        if settings.fontSize:
            try:
                font_size = int(settings.fontSize)
                if font_size < constants.MIN_FONT_SIZE or font_size > constants.MAX_FONT_SIZE:
                    warnings.append(f"Font size should be between {constants.MIN_FONT_SIZE} and {constants.MAX_FONT_SIZE} for best results")
            except ValueError:
                issues.append("Font size must be a valid number")
        
        # Document size validation
        if settings.documentSize and settings.documentSize not in constants.VALID_DOCUMENT_SIZES:
            issues.append(f"Document size must be one of: {', '.join(constants.VALID_DOCUMENT_SIZES)}")
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            sections_validated=["settings"]
        )

def validate_resume_data(resume_data: ResumeData, config_manager: ConfigManager) -> ValidationResult:
    """Convenience function for validating resume data"""
    validator = ResumeValidator(config_manager)
    return validator.validate_complete_resume(resume_data)
