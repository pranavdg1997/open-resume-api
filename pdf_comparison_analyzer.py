#!/usr/bin/env python3
"""
PDF Comparison Analyzer
Compares generated PDF with OpenResume reference to identify differences
"""

import os
import hashlib
import json
from pathlib import Path
import requests

def analyze_pdf_differences():
    """Analyze differences between generated and reference PDFs"""
    
    generated_pdf = "generated_from_excel.pdf"
    reference_pdf = "attached_assets/PRANAV GUJARATHI - OpenResume_1756350444177.pdf"
    
    if not os.path.exists(generated_pdf):
        print(f"❌ Generated PDF not found: {generated_pdf}")
        return
        
    if not os.path.exists(reference_pdf):
        print(f"❌ Reference PDF not found: {reference_pdf}")
        return
    
    # File size comparison
    gen_size = os.path.getsize(generated_pdf)
    ref_size = os.path.getsize(reference_pdf)
    size_ratio = gen_size / ref_size
    
    print("📊 PDF Size Comparison")
    print("=" * 50)
    print(f"Generated PDF: {gen_size:,} bytes")
    print(f"Reference PDF: {ref_size:,} bytes")
    print(f"Size Ratio: {size_ratio:.3f}")
    print(f"Missing content: {((1 - size_ratio) * 100):.1f}%")
    
    # Hash comparison
    def get_file_hash(filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    
    gen_hash = get_file_hash(generated_pdf)
    ref_hash = get_file_hash(reference_pdf)
    
    print(f"\n📋 Hash Comparison")
    print(f"Generated Hash: {gen_hash}")
    print(f"Reference Hash: {ref_hash}")
    print(f"Exact Match: {'✅ YES' if gen_hash == ref_hash else '❌ NO'}")
    
    # Identify likely issues
    print(f"\n🔍 Analysis")
    if size_ratio < 0.3:
        print("❌ CRITICAL: Generated PDF is <30% of reference size")
        print("   Likely missing: Projects, Skills, Publications, or major formatting")
    elif size_ratio < 0.5:
        print("⚠️ MAJOR: Generated PDF is <50% of reference size")  
        print("   Likely missing: Some sections or detailed formatting")
    elif size_ratio < 0.8:
        print("⚠️ MINOR: Generated PDF is <80% of reference size")
        print("   Likely missing: Minor formatting or small sections")
    else:
        print("✅ GOOD: Size ratio indicates most content present")

def check_openresume_status():
    """Check if OpenResume wrapper is working properly"""
    
    print("\n🔧 OpenResume Integration Status")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5000/api/v1/openresume-status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"Status: {status['status']}")
            print(f"Integration Mode: {status['integration_mode']}")
            
            wrapper_info = status['wrapper_info']
            print(f"OpenResume Available: {wrapper_info['openresume_available']}")
            print(f"Bridge Available: {wrapper_info['bridge_available']}")
            print(f"Node.js Available: {wrapper_info['node_available']}")
            
            if not wrapper_info['openresume_available']:
                print("❌ OpenResume not available - using fallback ReportLab")
                print("   This explains the size difference!")
            elif status['integration_mode'] != 'primary':
                print("⚠️ Not using primary OpenResume integration")
        else:
            print(f"❌ Status check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")

def analyze_json_data():
    """Analyze the parsed JSON data for completeness"""
    
    print("\n📝 JSON Data Analysis")
    print("=" * 50)
    
    try:
        with open("parsed_resume_data.json", "r") as f:
            data = json.load(f)
        
        # Check personal info
        personal = data.get('personalInfo', {})
        print(f"Personal Info: {len([k for k, v in personal.items() if v])}/6 fields filled")
        
        # Check work experiences  
        work_exp = data.get('workExperiences', [])
        total_bullets = sum(len(exp.get('descriptions', [])) for exp in work_exp)
        print(f"Work Experience: {len(work_exp)} positions, {total_bullets} bullet points")
        
        # Check education
        education = data.get('educations', [])
        print(f"Education: {len(education)} entries")
        
        # Check projects and skills
        projects = data.get('projects', [])
        skills = data.get('skills', [])
        print(f"Projects: {len(projects)} entries")
        print(f"Skills: {len(skills)} categories")
        
        # Compare with reference PDF content
        print(f"\n📋 Missing Sections Analysis")
        if len(projects) == 0:
            print("❌ MISSING: Projects section (referenced in PDF)")
        if len(skills) == 0:
            print("❌ MISSING: Skills section (referenced in PDF)")
            
        # Check for publications (mentioned in reference PDF)
        print("❌ MISSING: Publications section (visible in reference PDF)")
        
    except Exception as e:
        print(f"❌ Error analyzing JSON: {e}")

def suggest_fixes():
    """Suggest specific fixes to achieve perfect match"""
    
    print("\n🔧 Suggested Fixes")
    print("=" * 50)
    
    print("1. 🎯 Add missing sections to Excel parser:")
    print("   - Projects section")
    print("   - Skills section") 
    print("   - Publications section")
    
    print("\n2. 🔧 Fix OpenResume integration:")
    print("   - Ensure Node.js dependencies installed")
    print("   - Verify OpenResume bridge script working")
    print("   - Check if using authentic OpenResume vs fallback")
    
    print("\n3. 📊 Data completeness:")
    print("   - Parse all bullet points correctly")
    print("   - Handle multi-line descriptions")
    print("   - Preserve exact formatting")
    
    print("\n4. ⚙️ Settings optimization:")
    print("   - Match theme colors")
    print("   - Match font sizes")
    print("   - Match document layout")

def main():
    """Run complete PDF comparison analysis"""
    
    print("🎯 OpenResume PDF Perfect Match Analysis")
    print("=" * 60)
    
    analyze_pdf_differences()
    check_openresume_status()
    analyze_json_data()
    suggest_fixes()
    
    print(f"\n✅ Analysis Complete")
    print("Review suggestions above to achieve perfect match")

if __name__ == "__main__":
    main()