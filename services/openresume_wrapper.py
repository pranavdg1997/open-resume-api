"""
OpenResume Wrapper Service
This service wraps the actual OpenResume codebase, transforming our API data
to OpenResume format and using their PDF generation logic.
"""

import os
import json
import subprocess
import tempfile
import logging
from typing import Dict, Any, List
from models.resume_models import ResumeData

logger = logging.getLogger(__name__)

class OpenResumeWrapper:
    """Wrapper service that integrates with actual OpenResume codebase"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.openresume_path = "openresume-source"
        self.bridge_script = "openresume_pdf_generator.js"
        
        # Verify OpenResume installation
        self._verify_installation()
    
    def _verify_installation(self):
        """Verify that OpenResume source code is available"""
        if not os.path.exists(self.openresume_path):
            logger.warning(f"OpenResume source not found at {self.openresume_path}")
            return False
        
        if not os.path.exists(self.bridge_script):
            logger.warning(f"Bridge script not found at {self.bridge_script}")
            return False
        
        logger.info("OpenResume wrapper initialized successfully")
        return True
    
    def transform_to_openresume_format(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Transform our resume data format to OpenResume format"""
        
        # Personal info mapping
        profile = {
            "name": resume_data.personalInfo.name,
            "email": resume_data.personalInfo.email,
            "phone": resume_data.personalInfo.phone or "",
            "url": resume_data.personalInfo.url or "",
            "summary": resume_data.personalInfo.summary or "",
            "location": resume_data.personalInfo.location or ""
        }
        
        # Work experiences mapping
        work_experiences = []
        for exp in resume_data.workExperiences:
            work_experiences.append({
                "company": exp.company,
                "jobTitle": exp.jobTitle,
                "date": exp.date,
                "descriptions": exp.descriptions
            })
        
        # Education mapping
        educations = []
        for edu in resume_data.educations:
            educations.append({
                "school": edu.school,
                "degree": edu.degree,
                "date": edu.date,
                "gpa": edu.gpa or "",
                "descriptions": edu.descriptions
            })
        
        # Projects mapping
        projects = []
        for proj in resume_data.projects:
            projects.append({
                "project": proj.name,
                "date": proj.date,
                "descriptions": proj.descriptions
            })
        
        # Skills mapping - OpenResume uses different format
        skills = {
            "featuredSkills": [],
            "descriptions": []
        }
        
        if resume_data.skills:
            for skill_group in resume_data.skills:
                skill_desc = f"{skill_group.category}: {', '.join(skill_group.skills)}"
                skills["descriptions"].append(skill_desc)
        
        # Custom section
        custom = {
            "descriptions": resume_data.custom.descriptions if resume_data.custom else []
        }
        
        # Settings mapping
        settings = {
            "fontFamily": resume_data.settings.fontFamily or "system-ui",
            "fontSize": resume_data.settings.fontSize or "11",
            "documentSize": resume_data.settings.documentSize or "Letter",
            "themeColor": resume_data.settings.themeColor or "#1f2937",
            "formToHeading": {
                "workExperiences": "WORK EXPERIENCE",
                "educations": "EDUCATION",
                "projects": "PROJECTS",
                "skills": "SKILLS",
                "custom": "ADDITIONAL"
            },
            "formToShow": {
                "workExperiences": bool(work_experiences),
                "educations": bool(educations),
                "projects": bool(projects),
                "skills": bool(resume_data.skills),
                "custom": bool(custom["descriptions"])
            },
            "formsOrder": ["workExperiences", "educations", "projects", "skills", "custom"],
            "showBulletPoints": {
                "workExperiences": True,
                "educations": True,
                "projects": True,
                "skills": True,
                "custom": True
            }
        }
        
        # Publications mapping (if exists)
        publications = []
        if hasattr(resume_data, 'publications') and resume_data.publications:
            for pub in resume_data.publications:
                publications.append({
                    "name": pub.name,
                    "date": pub.date,
                    "descriptions": pub.descriptions
                })
        
        # Certifications mapping (if exists)
        certifications = []
        if hasattr(resume_data, 'certifications') and resume_data.certifications:
            for cert in resume_data.certifications:
                certifications.append({
                    "name": cert.name,
                    "date": cert.date,
                    "descriptions": cert.descriptions
                })
        
        # Complete OpenResume data structure
        openresume_data = {
            "personalInfo": profile,  # Change to personalInfo to match generator
            "workExperiences": work_experiences,
            "educations": educations,
            "projects": projects,
            "skills": [{"category": cat.split(": ")[0], "skills": cat.split(": ")[1].split(", ")} for cat in skills["descriptions"]] if skills["descriptions"] else [],
            "publications": publications,
            "certifications": certifications,
            "custom": custom,
            "settings": settings
        }
        
        return openresume_data
    
    def generate_pdf_with_openresume(self, resume_data: ResumeData) -> bytes:
        """Generate PDF using actual OpenResume logic"""
        
        try:
            # Transform data to OpenResume format
            openresume_data = self.transform_to_openresume_format(resume_data)
            
            # Write data to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(openresume_data, temp_file, indent=2)
                temp_file_path = temp_file.name
            
            try:
                # Call the bridge service
                result = subprocess.run(
                    ['node', self.bridge_script, temp_file_path],
                    capture_output=True,
                    text=False,  # We want bytes output
                    timeout=30
                )
                
                if result.returncode != 0:
                    error_msg = result.stderr.decode('utf-8') if result.stderr else "Unknown error"
                    logger.error(f"Bridge service failed: {error_msg}")
                    raise Exception(f"OpenResume bridge failed: {error_msg}")
                
                # For now, the bridge returns JSON with transformation info
                # In a full implementation, this would be actual PDF bytes
                pdf_bytes = result.stdout
                
                logger.info(f"OpenResume wrapper generated {len(pdf_bytes)} bytes")
                return pdf_bytes
                
            finally:
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        except subprocess.TimeoutExpired:
            logger.error("OpenResume bridge service timed out")
            raise Exception("PDF generation timed out")
        except Exception as e:
            logger.error(f"OpenResume wrapper error: {str(e)}")
            raise Exception(f"Failed to generate PDF with OpenResume: {str(e)}")
    
    def validate_openresume_data(self, openresume_data: Dict[str, Any]) -> bool:
        """Validate that data conforms to OpenResume structure"""
        
        required_fields = {
            'profile': ['name', 'email'],
            'workExperiences': [],
            'educations': [],
            'projects': [],
            'skills': ['featuredSkills', 'descriptions'],
            'custom': ['descriptions'],
            'settings': ['fontFamily', 'fontSize', 'documentSize']
        }
        
        for section, fields in required_fields.items():
            if section not in openresume_data:
                logger.error(f"Missing required section: {section}")
                return False
            
            if isinstance(openresume_data[section], dict):
                for field in fields:
                    if field not in openresume_data[section]:
                        logger.error(f"Missing required field: {section}.{field}")
                        return False
        
        logger.info("OpenResume data validation passed")
        return True
    
    def get_wrapper_info(self) -> Dict[str, Any]:
        """Get information about the wrapper status"""
        
        return {
            "wrapper_status": "active",
            "openresume_path": self.openresume_path,
            "bridge_script": self.bridge_script,
            "node_available": self._check_node_available(),
            "openresume_available": os.path.exists(self.openresume_path),
            "bridge_available": os.path.exists(self.bridge_script)
        }
    
    def _check_node_available(self) -> bool:
        """Check if Node.js is available"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False