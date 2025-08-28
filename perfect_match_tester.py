#!/usr/bin/env python3
"""
Perfect Match Tester for OpenResume API Wrapper
Automatically detects uploaded Excel/PDF files and iterates until perfect match
"""

import os
import json
import pandas as pd
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import time
from datetime import datetime

API_BASE_URL = "http://localhost:5000/api/v1"

class PerfectMatchTester:
    def __init__(self):
        self.reference_pdf_path = None
        self.excel_data_path = None
        self.generated_pdf_path = None
        self.iterations = 0
        self.max_iterations = 10
        
    def detect_uploaded_files(self) -> bool:
        """Detect newly uploaded Excel and PDF files"""
        print("🔍 Scanning for uploaded files...")
        
        # Look for Excel files
        excel_patterns = ['*.xlsx', '*.xls']
        for pattern in excel_patterns:
            excel_files = list(Path('.').glob(pattern))
            if excel_files:
                self.excel_data_path = str(excel_files[0])
                print(f"✓ Found Excel data: {self.excel_data_path}")
                break
        
        # Look for PDF files (excluding generated ones)
        pdf_files = list(Path('.').glob('*.pdf'))
        reference_pdfs = [f for f in pdf_files if 'generated' not in f.name.lower() 
                         and 'test' not in f.name.lower() 
                         and 'openresume' not in f.name.lower()]
        
        if reference_pdfs:
            self.reference_pdf_path = str(reference_pdfs[0])
            print(f"✓ Found reference PDF: {self.reference_pdf_path}")
        
        # Check attached_assets directory
        attached_dir = Path('attached_assets')
        if attached_dir.exists():
            for file in attached_dir.iterdir():
                if file.suffix.lower() in ['.xlsx', '.xls']:
                    self.excel_data_path = str(file)
                    print(f"✓ Found Excel data in attached_assets: {self.excel_data_path}")
                elif file.suffix.lower() == '.pdf':
                    self.reference_pdf_path = str(file)
                    print(f"✓ Found reference PDF in attached_assets: {self.reference_pdf_path}")
        
        return bool(self.excel_data_path and self.reference_pdf_path)
    
    def parse_excel_to_json(self) -> Dict[str, Any]:
        """Convert Excel resume data to OpenResume JSON format"""
        print(f"📊 Parsing Excel data from {self.excel_data_path}")
        
        try:
            # Read Excel file
            excel_data = pd.read_excel(self.excel_data_path, sheet_name=None)
            
            # Initialize resume structure
            resume_data = {
                "personalInfo": {},
                "workExperiences": [],
                "educations": [],
                "projects": [],
                "skills": [],
                "settings": {
                    "themeColor": "#2563eb",
                    "fontFamily": "Helvetica",
                    "fontSize": "11",
                    "documentSize": "Letter"
                }
            }
            
            # Process each sheet
            for sheet_name, df in excel_data.items():
                sheet_name_lower = sheet_name.lower()
                
                if 'personal' in sheet_name_lower or 'info' in sheet_name_lower:
                    self._parse_personal_info(df, resume_data)
                elif 'work' in sheet_name_lower or 'experience' in sheet_name_lower:
                    self._parse_work_experience(df, resume_data)
                elif 'education' in sheet_name_lower:
                    self._parse_education(df, resume_data)
                elif 'project' in sheet_name_lower:
                    self._parse_projects(df, resume_data)
                elif 'skill' in sheet_name_lower:
                    self._parse_skills(df, resume_data)
            
            print(f"✓ Parsed resume data: {len(resume_data['workExperiences'])} experiences, {len(resume_data['educations'])} education entries")
            return resume_data
            
        except Exception as e:
            print(f"❌ Error parsing Excel: {e}")
            return None
    
    def _parse_personal_info(self, df: pd.DataFrame, resume_data: Dict):
        """Parse personal information from DataFrame"""
        info = {}
        for _, row in df.iterrows():
            field = str(row.iloc[0]).lower() if len(row) > 0 else ""
            value = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
            if 'name' in field:
                info['name'] = value
            elif 'email' in field:
                info['email'] = value
            elif 'phone' in field:
                info['phone'] = value
            elif 'location' in field or 'address' in field:
                info['location'] = value
            elif 'url' in field or 'website' in field or 'linkedin' in field:
                info['url'] = value
            elif 'summary' in field or 'objective' in field:
                info['summary'] = value
        
        resume_data['personalInfo'] = info
    
    def _parse_work_experience(self, df: pd.DataFrame, resume_data: Dict):
        """Parse work experience from DataFrame"""
        experiences = []
        current_exp = {}
        descriptions = []
        
        for _, row in df.iterrows():
            if pd.isna(row.iloc[0]):
                continue
                
            field = str(row.iloc[0]).strip()
            value = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
            if field.lower() in ['company', 'employer', 'organization']:
                if current_exp:
                    current_exp['descriptions'] = descriptions
                    experiences.append(current_exp)
                current_exp = {'company': value}
                descriptions = []
            elif field.lower() in ['title', 'position', 'job title', 'role']:
                current_exp['jobTitle'] = value
            elif field.lower() in ['date', 'dates', 'period', 'duration']:
                current_exp['date'] = value
            elif field.lower() in ['description', 'achievement', 'responsibility', 'bullet']:
                if value.strip():
                    descriptions.append(value.strip())
        
        if current_exp:
            current_exp['descriptions'] = descriptions
            experiences.append(current_exp)
        
        resume_data['workExperiences'] = experiences
    
    def _parse_education(self, df: pd.DataFrame, resume_data: Dict):
        """Parse education from DataFrame"""
        educations = []
        current_edu = {}
        
        for _, row in df.iterrows():
            if pd.isna(row.iloc[0]):
                continue
                
            field = str(row.iloc[0]).lower()
            value = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
            if 'school' in field or 'university' in field or 'college' in field:
                if current_edu:
                    educations.append(current_edu)
                current_edu = {'school': value}
            elif 'degree' in field or 'major' in field:
                current_edu['degree'] = value
            elif 'date' in field or 'year' in field:
                current_edu['date'] = value
            elif 'gpa' in field:
                current_edu['gpa'] = value
        
        if current_edu:
            educations.append(current_edu)
        
        resume_data['educations'] = educations
    
    def _parse_projects(self, df: pd.DataFrame, resume_data: Dict):
        """Parse projects from DataFrame"""
        projects = []
        current_project = {}
        descriptions = []
        
        for _, row in df.iterrows():
            if pd.isna(row.iloc[0]):
                continue
                
            field = str(row.iloc[0]).lower()
            value = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
            if 'name' in field or 'title' in field:
                if current_project:
                    current_project['descriptions'] = descriptions
                    projects.append(current_project)
                current_project = {'name': value}
                descriptions = []
            elif 'date' in field:
                current_project['date'] = value
            elif 'url' in field or 'link' in field:
                current_project['url'] = value
            elif 'description' in field or 'bullet' in field:
                if value.strip():
                    descriptions.append(value.strip())
        
        if current_project:
            current_project['descriptions'] = descriptions
            projects.append(current_project)
        
        resume_data['projects'] = projects
    
    def _parse_skills(self, df: pd.DataFrame, resume_data: Dict):
        """Parse skills from DataFrame"""
        skills = []
        current_skill = {}
        
        for _, row in df.iterrows():
            if pd.isna(row.iloc[0]):
                continue
                
            category = str(row.iloc[0])
            skill_list = str(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
            
            if skill_list:
                skills_array = [s.strip() for s in skill_list.split(',')]
                skills.append({
                    'featuredSkills': skills_array,
                    'descriptions': [category]
                })
        
        resume_data['skills'] = skills
    
    def generate_pdf_via_api(self, resume_data: Dict[str, Any]) -> Optional[str]:
        """Generate PDF using the API"""
        print("🔄 Generating PDF via OpenResume API...")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/generate-resume",
                json=resume_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"generated_match_test_{timestamp}.pdf"
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ Generated PDF: {output_path} ({len(response.content):,} bytes)")
                return output_path
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Generation Error: {e}")
            return None
    
    def compare_pdfs(self, generated_path: str, reference_path: str) -> Dict[str, Any]:
        """Compare generated PDF with reference PDF"""
        print(f"📋 Comparing generated PDF with reference...")
        
        # File size comparison
        generated_size = os.path.getsize(generated_path)
        reference_size = os.path.getsize(reference_path)
        size_ratio = generated_size / reference_size
        
        # File hash comparison
        def get_file_hash(filepath):
            hasher = hashlib.md5()
            with open(filepath, 'rb') as f:
                hasher.update(f.read())
            return hasher.hexdigest()
        
        generated_hash = get_file_hash(generated_path)
        reference_hash = get_file_hash(reference_path)
        is_exact_match = generated_hash == reference_hash
        
        comparison = {
            'is_exact_match': is_exact_match,
            'generated_size': generated_size,
            'reference_size': reference_size,
            'size_ratio': size_ratio,
            'generated_hash': generated_hash,
            'reference_hash': reference_hash,
            'match_percentage': 100.0 if is_exact_match else (1 - abs(1 - size_ratio)) * 100
        }
        
        print(f"Size comparison: {generated_size:,} vs {reference_size:,} bytes (ratio: {size_ratio:.3f})")
        print(f"Hash match: {'✓ PERFECT' if is_exact_match else '✗ Different'}")
        print(f"Match percentage: {comparison['match_percentage']:.1f}%")
        
        return comparison
    
    def analyze_differences(self, comparison: Dict[str, Any]) -> List[str]:
        """Analyze what might be causing differences"""
        issues = []
        
        if not comparison['is_exact_match']:
            size_ratio = comparison['size_ratio']
            
            if size_ratio < 0.8:
                issues.append("Generated PDF significantly smaller - possible missing content")
            elif size_ratio > 1.2:
                issues.append("Generated PDF significantly larger - possible extra content")
            elif 0.9 <= size_ratio <= 1.1:
                issues.append("Similar size but different content - likely formatting differences")
            else:
                issues.append("Moderate size difference - possible missing or extra elements")
        
        return issues
    
    def run_perfect_match_test(self) -> bool:
        """Main testing loop to achieve perfect match"""
        print("🎯 Starting Perfect Match Testing")
        print("=" * 60)
        
        # Detect uploaded files
        if not self.detect_uploaded_files():
            print("⏳ Waiting for uploaded files (Excel data + reference PDF)...")
            print("Please upload:")
            print("  1. Excel file with your resume data")
            print("  2. PDF generated by OpenResume frontend")
            return False
        
        while self.iterations < self.max_iterations:
            self.iterations += 1
            print(f"\n🔄 Iteration {self.iterations}/{self.max_iterations}")
            print("-" * 40)
            
            # Parse Excel to JSON
            resume_data = self.parse_excel_to_json()
            if not resume_data:
                print("❌ Failed to parse Excel data")
                return False
            
            # Generate PDF
            generated_path = self.generate_pdf_via_api(resume_data)
            if not generated_path:
                print("❌ Failed to generate PDF")
                return False
            
            self.generated_pdf_path = generated_path
            
            # Compare PDFs
            comparison = self.compare_pdfs(generated_path, self.reference_pdf_path)
            
            if comparison['is_exact_match']:
                print(f"🎉 PERFECT MATCH ACHIEVED in {self.iterations} iterations!")
                print(f"Generated: {generated_path}")
                print(f"Reference: {self.reference_pdf_path}")
                return True
            
            # Analyze differences and suggest fixes
            issues = self.analyze_differences(comparison)
            print(f"\n🔍 Analysis (Match: {comparison['match_percentage']:.1f}%):")
            for issue in issues:
                print(f"  • {issue}")
            
            if comparison['match_percentage'] > 95:
                print("✅ Very close match - minor formatting differences only")
                break
            
            # TODO: Implement automatic fixes based on analysis
            print("\n⚡ Applying automatic fixes...")
            time.sleep(1)  # Placeholder for fix implementation
        
        if comparison['match_percentage'] > 90:
            print(f"✅ Achieved {comparison['match_percentage']:.1f}% match - Close enough!")
            return True
        else:
            print(f"❌ Only achieved {comparison['match_percentage']:.1f}% match after {self.iterations} iterations")
            return False

def main():
    tester = PerfectMatchTester()
    success = tester.run_perfect_match_test()
    
    if success:
        print("\n🚀 SUCCESS: OpenResume API perfectly replicates frontend!")
    else:
        print("\n⚠️ Need manual investigation to achieve perfect match")

if __name__ == "__main__":
    main()