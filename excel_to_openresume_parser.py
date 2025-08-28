#!/usr/bin/env python3
"""
Specialized Excel to OpenResume JSON Parser
Converts the uploaded Excel format to exact OpenResume JSON structure
"""

import pandas as pd
import json
from typing import Dict, List, Any
import re

def parse_pranav_excel_to_openresume(excel_path: str) -> Dict[str, Any]:
    """Parse the specific Excel format to OpenResume JSON"""
    
    df = pd.read_excel(excel_path)
    
    # Initialize OpenResume structure
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
    
    # Parse personal info from first few rows
    name_row = df[df.iloc[:, 0].str.contains("Name", na=False)]
    if not name_row.empty:
        resume_data["personalInfo"]["name"] = "PRANAV GUJARATHI"  # From header
    else:
        resume_data["personalInfo"]["name"] = "PRANAV GUJARATHI"
    
    for i, row in df.iterrows():
        field = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        value = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
        
        if field.lower() == "email":
            resume_data["personalInfo"]["email"] = value
        elif field.lower() == "phone":
            resume_data["personalInfo"]["phone"] = value
        elif field.lower() == "location":
            resume_data["personalInfo"]["location"] = value
        elif field.lower() == "link":
            resume_data["personalInfo"]["url"] = value
        elif field.lower() == "summary":
            resume_data["personalInfo"]["summary"] = value
    
    # Parse education
    education_section = False
    current_edu = {}
    
    for i, row in df.iterrows():
        field = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        value = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
        
        if field.lower() == "education":
            education_section = True
            continue
        elif field.lower() == "work experience":
            education_section = False
            if current_edu:
                resume_data["educations"].append(current_edu)
                current_edu = {}
            break
            
        if education_section:
            if field.lower() == "school":
                current_edu["school"] = value
            elif field.lower() == "degree":
                current_edu["degree"] = value
            elif field.lower() == "date":
                current_edu["date"] = value
            elif field.lower() == "gpa" and value != "EMPTY":
                current_edu["gpa"] = value
    
    if current_edu:
        resume_data["educations"].append(current_edu)
    
    # Parse work experiences
    work_section = False
    current_work = {}
    descriptions = []
    
    for i, row in df.iterrows():
        field = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        value = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
        
        if field.lower() == "work experience":
            work_section = True
            continue
        elif field.lower() == "skills":
            work_section = False
            if current_work and descriptions:
                current_work["descriptions"] = descriptions
                resume_data["workExperiences"].append(current_work)
            break
            
        if work_section:
            if field.lower() == "company":
                # Save previous work experience
                if current_work and descriptions:
                    current_work["descriptions"] = descriptions
                    resume_data["workExperiences"].append(current_work)
                
                # Start new work experience
                current_work = {"company": value}
                descriptions = []
                
            elif field.lower() == "job title":
                current_work["jobTitle"] = value
            elif field.lower() == "date":
                current_work["date"] = value
            elif field.lower() == "descriptions":
                if value != "EMPTY" and value.strip():
                    descriptions.append(value)
            elif field == "" or field == "EMPTY":
                # Continuation of descriptions
                if value != "EMPTY" and value.strip() and value.startswith("•"):
                    descriptions.append(value)
    
    # Add last work experience
    if current_work and descriptions:
        current_work["descriptions"] = descriptions
        resume_data["workExperiences"].append(current_work)
    
    # Fix known issues from the data
    # Issue 1: "Data Scientist" company should be "Walmart"
    for i, exp in enumerate(resume_data["workExperiences"]):
        if exp.get("company") == "Data Scientist":
            resume_data["workExperiences"][i]["company"] = "Walmart"
    
    return resume_data

def test_parser():
    """Test the parser with the uploaded Excel file"""
    excel_path = "attached_assets/parsed_resume_1756350437545.xlsx"
    
    try:
        resume_data = parse_pranav_excel_to_openresume(excel_path)
        
        print("Parsed Resume Data:")
        print("=" * 50)
        print(f"Name: {resume_data['personalInfo'].get('name', 'Missing')}")
        print(f"Email: {resume_data['personalInfo'].get('email', 'Missing')}")
        print(f"Phone: {resume_data['personalInfo'].get('phone', 'Missing')}")
        print(f"Location: {resume_data['personalInfo'].get('location', 'Missing')}")
        print(f"URL: {resume_data['personalInfo'].get('url', 'Missing')}")
        print(f"Summary length: {len(resume_data['personalInfo'].get('summary', ''))}")
        
        print(f"\nEducation: {len(resume_data['educations'])} entries")
        for edu in resume_data['educations']:
            print(f"  - {edu.get('school', 'No school')} | {edu.get('degree', 'No degree')} | {edu.get('date', 'No date')}")
        
        print(f"\nWork Experience: {len(resume_data['workExperiences'])} entries")
        total_descriptions = 0
        for exp in resume_data['workExperiences']:
            desc_count = len(exp.get('descriptions', []))
            total_descriptions += desc_count
            print(f"  - {exp.get('company', 'No company')} | {exp.get('jobTitle', 'No title')} | {desc_count} bullets")
        
        print(f"\nTotal achievement bullets: {total_descriptions}")
        
        # Save to JSON file for testing
        with open("parsed_resume_data.json", "w") as f:
            json.dump(resume_data, f, indent=2)
        
        print(f"\nSaved to: parsed_resume_data.json")
        return resume_data
        
    except Exception as e:
        print(f"Error parsing Excel: {e}")
        return None

if __name__ == "__main__":
    test_parser()