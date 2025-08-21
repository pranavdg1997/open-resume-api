"""
PDF Generation service using ReportLab
Based on OpenResume's design patterns
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import logging
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any

from models.resume_models import ResumeData, PersonalInfo, WorkExperience, Education, Project, Skill
from services.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class PDFGenerator:
    """PDF generation service for resumes"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.setup_fonts()
        
    def setup_fonts(self):
        """Setup custom fonts for PDF generation"""
        try:
            # Register OpenSans fonts
            font_dir = "static/fonts"
            if os.path.exists(f"{font_dir}/OpenSans-Regular.ttf"):
                pdfmetrics.registerFont(TTFont('OpenSans', f"{font_dir}/OpenSans-Regular.ttf"))
                logger.info("OpenSans regular font registered")
            if os.path.exists(f"{font_dir}/OpenSans-Bold.ttf"):
                pdfmetrics.registerFont(TTFont('OpenSans-Bold', f"{font_dir}/OpenSans-Bold.ttf"))
                logger.info("OpenSans bold font registered")
        except Exception as e:
            logger.warning(f"Could not load custom fonts: {e}. Using default fonts.")
    
    def generate_resume_pdf(self, resume_data: ResumeData) -> bytes:
        """Generate PDF from resume data"""
        try:
            buffer = BytesIO()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=self._get_page_size(resume_data.settings.documentSize or "Letter"),
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            # Build content
            story = []
            
            # Add personal info header
            story.extend(self._build_header(resume_data.personalInfo, resume_data.settings))
            
            # Add sections based on settings
            if (resume_data.settings.formToShow or {}).get("workExperiences", True) and resume_data.workExperiences:
                story.extend(self._build_work_experience_section(
                    resume_data.workExperiences, 
                    resume_data.settings
                ))
            
            if (resume_data.settings.formToShow or {}).get("educations", True) and resume_data.educations:
                story.extend(self._build_education_section(
                    resume_data.educations,
                    resume_data.settings
                ))
            
            if (resume_data.settings.formToShow or {}).get("projects", True) and resume_data.projects:
                story.extend(self._build_projects_section(
                    resume_data.projects,
                    resume_data.settings
                ))
            
            if (resume_data.settings.formToShow or {}).get("skills", True) and resume_data.skills:
                story.extend(self._build_skills_section(
                    resume_data.skills,
                    resume_data.settings
                ))
            
            if (resume_data.settings.formToShow or {}).get("custom", True) and resume_data.custom.descriptions:
                story.extend(self._build_custom_section(
                    resume_data.custom.descriptions,
                    resume_data.settings
                ))
            
            # Build PDF
            doc.build(story)
            
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            logger.info(f"Successfully generated PDF of {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def _get_page_size(self, size: str):
        """Get page size from settings"""
        if size.lower() == "a4":
            return A4
        return letter
    
    def _get_styles(self, settings):
        """Get paragraph styles based on settings"""
        # Check if we already have styles cached for this instance
        if hasattr(self, '_cached_styles') and self._cached_styles:
            return self._cached_styles
        
        styles = getSampleStyleSheet()
        theme_color = HexColor(settings.themeColor)
        font_family = settings.fontFamily if settings.fontFamily in ['OpenSans'] else 'Helvetica'
        font_size = int(settings.fontSize) if settings.fontSize.isdigit() else 11
        
        # Add custom styles only if they don't exist
        if 'Name' not in styles:
            styles.add(ParagraphStyle(
                name='Name',
                parent=styles['Heading1'],
                fontName=f'{font_family}-Bold' if font_family == 'OpenSans' else 'Helvetica-Bold',
                fontSize=20,
                textColor=theme_color,
                alignment=TA_CENTER,
                spaceAfter=6
            ))
        
        # Contact style
        if 'Contact' not in styles:
            styles.add(ParagraphStyle(
                name='Contact',
                parent=styles['Normal'],
                fontName=font_family,
                fontSize=font_size,
                alignment=TA_CENTER,
                spaceAfter=12
            ))
        
        # Section heading style
        if 'SectionHeading' not in styles:
            styles.add(ParagraphStyle(
                name='SectionHeading',
                parent=styles['Heading2'],
                fontName=f'{font_family}-Bold' if font_family == 'OpenSans' else 'Helvetica-Bold',
                fontSize=font_size + 2,
                textColor=theme_color,
                spaceBefore=12,
                spaceAfter=6,
                borderWidth=1,
                borderColor=theme_color,
                borderPadding=2
            ))
        
        # Job title style
        if 'JobTitle' not in styles:
            styles.add(ParagraphStyle(
                name='JobTitle',
                parent=styles['Normal'],
                fontName=f'{font_family}-Bold' if font_family == 'OpenSans' else 'Helvetica-Bold',
                fontSize=font_size,
                spaceBefore=6,
                spaceAfter=2
            ))
        
        # Company style
        if 'Company' not in styles:
            styles.add(ParagraphStyle(
                name='Company',
                parent=styles['Normal'],
                fontName=font_family,
                fontSize=font_size,
                spaceAfter=2
            ))
        
        # Body text style
        if 'BodyText' not in styles:
            styles.add(ParagraphStyle(
                name='BodyText',
                parent=styles['Normal'],
                fontName=font_family,
                fontSize=font_size,
                spaceAfter=3
            ))
        
        # Cache styles for this generation
        self._cached_styles = styles
        return styles
    
    def _build_header(self, personal_info: PersonalInfo, settings):
        """Build personal information header"""
        styles = self._get_styles(settings)
        story = []
        
        # Name
        story.append(Paragraph(personal_info.name, styles['Name']))
        
        # Contact information
        contact_parts = []
        if personal_info.email:
            contact_parts.append(personal_info.email)
        if personal_info.phone:
            contact_parts.append(personal_info.phone)
        if personal_info.url:
            contact_parts.append(f'<link href="{personal_info.url}">{personal_info.url}</link>')
        if personal_info.location:
            contact_parts.append(personal_info.location)
        
        if contact_parts:
            contact_text = " • ".join(contact_parts)
            story.append(Paragraph(contact_text, styles['Contact']))
        
        # Summary
        if personal_info.summary:
            story.append(Spacer(1, 6))
            story.append(Paragraph(personal_info.summary, styles['BodyText']))
        
        story.append(Spacer(1, 12))
        return story
    
    def _build_work_experience_section(self, work_experiences: List[WorkExperience], settings):
        """Build work experience section"""
        styles = self._get_styles(settings)
        story = []
        
        heading = (settings.formToHeading or {}).get("workExperiences", "WORK EXPERIENCE")
        story.append(Paragraph(heading, styles['SectionHeading']))
        
        for exp in work_experiences:
            # Company and job title table
            exp_table = Table([
                [exp.jobTitle, exp.date],
                [exp.company, ""]
            ], colWidths=[4*inch, 2*inch])
            
            exp_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), f"{settings.fontFamily}-Bold" if settings.fontFamily == 'OpenSans' else 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, 0), settings.fontFamily if settings.fontFamily in ['OpenSans'] else 'Helvetica'),
                ('FONTNAME', (0, 1), (0, 1), settings.fontFamily if settings.fontFamily in ['OpenSans'] else 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), int(settings.fontSize) if settings.fontSize.isdigit() else 11),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
            ]))
            
            story.append(exp_table)
            
            # Job descriptions
            for desc in exp.descriptions:
                bullet_para = Paragraph(f"• {desc}", styles['BodyText'])
                story.append(bullet_para)
            
            story.append(Spacer(1, 6))
        
        return story
    
    def _build_education_section(self, educations: List[Education], settings):
        """Build education section"""
        styles = self._get_styles(settings)
        story = []
        
        heading = (settings.formToHeading or {}).get("educations", "EDUCATION")
        story.append(Paragraph(heading, styles['SectionHeading']))
        
        for edu in educations:
            # Education table
            gpa_text = f" | GPA: {edu.gpa}" if edu.gpa else ""
            degree_text = f"{edu.degree}{gpa_text}"
            
            edu_table = Table([
                [degree_text, edu.date],
                [edu.school, ""]
            ], colWidths=[4*inch, 2*inch])
            
            edu_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), f"{settings.fontFamily}-Bold" if settings.fontFamily == 'OpenSans' else 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, 0), settings.fontFamily if settings.fontFamily in ['OpenSans'] else 'Helvetica'),
                ('FONTNAME', (0, 1), (0, 1), settings.fontFamily if settings.fontFamily in ['OpenSans'] else 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), int(settings.fontSize) if settings.fontSize.isdigit() else 11),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
            ]))
            
            story.append(edu_table)
            
            # Education descriptions
            for desc in edu.descriptions:
                bullet_para = Paragraph(f"• {desc}", styles['BodyText'])
                story.append(bullet_para)
            
            story.append(Spacer(1, 6))
        
        return story
    
    def _build_projects_section(self, projects: List[Project], settings):
        """Build projects section"""
        styles = self._get_styles(settings)
        story = []
        
        heading = (settings.formToHeading or {}).get("projects", "PROJECTS")
        story.append(Paragraph(heading, styles['SectionHeading']))
        
        for project in projects:
            # Project table
            proj_table = Table([
                [project.name, project.date]
            ], colWidths=[4*inch, 2*inch])
            
            proj_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, 0), f"{settings.fontFamily}-Bold" if settings.fontFamily == 'OpenSans' else 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, 0), settings.fontFamily if settings.fontFamily in ['OpenSans'] else 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), int(settings.fontSize) if settings.fontSize.isdigit() else 11),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
            ]))
            
            story.append(proj_table)
            
            # Project descriptions
            for desc in project.descriptions:
                bullet_para = Paragraph(f"• {desc}", styles['BodyText'])
                story.append(bullet_para)
            
            story.append(Spacer(1, 6))
        
        return story
    
    def _build_skills_section(self, skills: List[Skill], settings):
        """Build skills section"""
        styles = self._get_styles(settings)
        story = []
        
        heading = (settings.formToHeading or {}).get("skills", "SKILLS")
        story.append(Paragraph(heading, styles['SectionHeading']))
        
        for skill_group in skills:
            skill_text = f"<b>{skill_group.category}:</b> {', '.join(skill_group.skills)}"
            story.append(Paragraph(skill_text, styles['BodyText']))
        
        story.append(Spacer(1, 6))
        return story
    
    def _build_custom_section(self, descriptions: List[str], settings):
        """Build custom section"""
        styles = self._get_styles(settings)
        story = []
        
        heading = (settings.formToHeading or {}).get("custom", "ADDITIONAL")
        story.append(Paragraph(heading, styles['SectionHeading']))
        
        for desc in descriptions:
            story.append(Paragraph(f"• {desc}", styles['BodyText']))
        
        story.append(Spacer(1, 6))
        return story
