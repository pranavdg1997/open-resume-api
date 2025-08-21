"""
Resume template definitions and styling
Based on OpenResume's design principles
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from reportlab.lib.colors import HexColor

@dataclass
class TemplateStyle:
    """Template styling configuration"""
    name: str
    description: str
    theme_color: str
    font_family: str
    font_size: int
    spacing: Dict[str, float]
    margins: Dict[str, float]

class ResumeTemplate:
    """Resume template manager"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, TemplateStyle]:
        """Initialize available resume templates"""
        return {
            "professional": TemplateStyle(
                name="Professional",
                description="Clean, ATS-friendly design based on OpenResume",
                theme_color="#1f2937",
                font_family="OpenSans", 
                font_size=11,
                spacing={
                    "section_spacing": 12,
                    "item_spacing": 6,
                    "line_spacing": 3,
                    "header_spacing": 6
                },
                margins={
                    "top": 0.5,
                    "bottom": 0.5,
                    "left": 0.5,
                    "right": 0.5
                }
            ),
            "modern": TemplateStyle(
                name="Modern",
                description="Contemporary design with bold accents",
                theme_color="#2563eb",
                font_family="OpenSans",
                font_size=11,
                spacing={
                    "section_spacing": 14,
                    "item_spacing": 7,
                    "line_spacing": 3,
                    "header_spacing": 8
                },
                margins={
                    "top": 0.6,
                    "bottom": 0.6,
                    "left": 0.6,
                    "right": 0.6
                }
            ),
            "classic": TemplateStyle(
                name="Classic",
                description="Traditional professional format",
                theme_color="#374151",
                font_family="OpenSans",
                font_size=11,
                spacing={
                    "section_spacing": 10,
                    "item_spacing": 5,
                    "line_spacing": 2,
                    "header_spacing": 5
                },
                margins={
                    "top": 0.75,
                    "bottom": 0.75,
                    "left": 0.75,
                    "right": 0.75
                }
            )
        }
    
    def get_template(self, template_name: str) -> TemplateStyle:
        """Get template by name"""
        return self.templates.get(template_name, self.templates["professional"])
    
    def list_templates(self) -> Dict[str, Dict[str, str]]:
        """List available templates"""
        return {
            name: {
                "name": template.name,
                "description": template.description,
                "theme_color": template.theme_color,
                "font_family": template.font_family
            }
            for name, template in self.templates.items()
        }
    
    def get_color_schemes(self) -> Dict[str, List[str]]:
        """Get available color schemes"""
        return {
            "professional": [
                "#1f2937",  # Dark gray
                "#374151",  # Medium gray  
                "#4b5563",  # Light gray
                "#6b7280",  # Lighter gray
            ],
            "vibrant": [
                "#dc2626",  # Red
                "#ea580c",  # Orange
                "#d97706",  # Amber
                "#65a30d",  # Lime
            ],
            "cool": [
                "#2563eb",  # Blue
                "#7c3aed",  # Violet
                "#c026d3",  # Fuchsia
                "#db2777",  # Pink
            ],
            "earth": [
                "#92400e",  # Brown
                "#a16207",  # Yellow
                "#166534",  # Green
                "#075985",  # Sky
            ]
        }
    
    def validate_customizations(self, customizations: Dict[str, Any]) -> List[str]:
        """Validate template customizations"""
        errors = []
        
        # Validate theme color
        if "theme_color" in customizations:
            import re
            color_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
            if not color_pattern.match(customizations["theme_color"]):
                errors.append("Theme color must be a valid hex color")
        
        # Validate font size
        if "font_size" in customizations:
            try:
                font_size = int(customizations["font_size"])
                if font_size < 8 or font_size > 16:
                    errors.append("Font size must be between 8 and 16")
            except (ValueError, TypeError):
                errors.append("Font size must be a valid integer")
        
        # Validate margins
        if "margins" in customizations:
            for margin_key, margin_value in customizations["margins"].items():
                try:
                    margin_float = float(margin_value)
                    if margin_float < 0.25 or margin_float > 2.0:
                        errors.append(f"Margin '{margin_key}' must be between 0.25 and 2.0 inches")
                except (ValueError, TypeError):
                    errors.append(f"Margin '{margin_key}' must be a valid number")
        
        return errors
    
    def apply_customizations(self, template: TemplateStyle, customizations: Dict[str, Any]) -> TemplateStyle:
        """Apply customizations to a template"""
        # Create a copy of the template
        custom_template = TemplateStyle(
            name=f"{template.name} (Custom)",
            description=template.description,
            theme_color=template.theme_color,
            font_family=template.font_family,
            font_size=template.font_size,
            spacing=template.spacing.copy(),
            margins=template.margins.copy()
        )
        
        # Apply customizations
        if "theme_color" in customizations:
            custom_template.theme_color = customizations["theme_color"]
        
        if "font_family" in customizations:
            custom_template.font_family = customizations["font_family"]
        
        if "font_size" in customizations:
            custom_template.font_size = int(customizations["font_size"])
        
        if "margins" in customizations:
            custom_template.margins.update(customizations["margins"])
        
        if "spacing" in customizations:
            custom_template.spacing.update(customizations["spacing"])
        
        return custom_template

# Global template manager instance
template_manager = ResumeTemplate()
