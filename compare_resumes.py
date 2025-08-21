#!/usr/bin/env python3
"""
Resume Comparison Tool
Compares the original uploaded resume with our generated versions
to ensure content accuracy and formatting consistency.
"""

import json
import os
from typing import Dict, List, Any

def analyze_original_resume():
    """Extract key information from the original resume text"""
    
    # The original resume content (extracted from PDF view)
    original_content = """
PRANAV GUJARATHI
pranavdg1997@gmail.com          (331) 248-7381     Austin, TX    linkedin.com/in/pranav-gujarathi/

EDUCATION
Indiana University - Bloomington
Master's, Data Science                                                        August 2019 - May 2021

WORK EXPERIENCE
Cigna
Senior AI Engineer                                                          September 2024 - Present
• Spearheading the development of a Generative AI-augmented Prior Authorization platform,
  focusing on Agentic AI systems, RAG pipelines, seamless platform integration, and robust ML-Ops
  pipelines.
• Orchestrating cross-functional teams to deliver scalable AI solutions for internal AI platforms,
  ensuring high performance, reliability, and compliance in medical care workflows.

Walmart
AI Engineer                                                               October 2023 - August 2024
• Developing Generative AI based automation solution that carries out exploratory Data analysis
  on complex data types simply based on voice/text commands, removing the learning curve for
  non-programmers to use analytical tools, in some cases removing the need to build dashboards.
  Saved 130,000 associate work hours per week.
• Delivered end-to-end automation solution for extracting item attributes and competitor using a RAG
  system (Retrieval Augmented Generation) to generate structured usable data – in contrast to a
  legacy system based on manual annotation – achieved 80% in cost savings and over 24 times
  improvement in turnaround time.
• Lead ML Engineering - containerization (Docker, configuring Kubernetes and deploying API
  endpoints in tandem with frontend solutions - enforcing high standards for quality, reliability, and
  security in deployed machine learning solutions.

Data Scientist                                                           January 2022 - October 2023
• Deployed and managed large-scale anomaly detection engine with into production with real-time
  user feedback, providing upwards of 70% capture rate.
• Achieved > 80% explained variance and less than 5% global error by contributing to a novel
  causal-inference forecast model, helping make around $1.6 Billion worth of sales, more explainable
  and interpretable.
• Contributed to building a Rest API solution and optimized runtime on deployment on Azure cloud
  with best CI/CD practices.
• Conducted PoCs for Gen AI use-cases such as automated competitor prices mining tool, text-based
  interface for forecast observation (as an alternative to dashboard)

ZS Associates
Data Science Associate                                                    June 2018 - December 2021
• Deployed a product with favorable client feedback and improved performance in the form of a cross
  platform application.
• As part of the project, utilized Python libraries, Deep Learning frameworks and transformer models
  to implement a Natural Language Inference pipeline, i.e., extracting domain-relevant inferences from
  textual data (news articles, publications, etc.).
• Deployed a novel ML based solution for marketing strategy planning with 60% more projected
  efficiency on target reach and market penetration ROI, using multivariate time series models and
  Linear Optimization.

Indiana University - Bloomington
Research Engineer                                                        January 2020 - May 2021
• Building a Mind Lab: Designed and implemented pipelines to successfully conduct experiments
  as part of NSF funded project under the guidance of Professor Justin Wood. The project involved
  working across topics in Computer Vision and Deep Reinforcement Learning.
• IUPUI Data Lab: Conducted research and experiments in Natural Language Processing models and
  architectures towards a successful end to end process from ideation to eventual publication under the guidance of Prof
  Sunandan Chakraborty.
• Kelley School of Business: Successfully deployed an MLOps pipeline starting from a PoC
  formulation to a GUI dashboard using Big Data libraries and cloud-based parallel computation.

PROJECT

SKILLS
"""
    
    return {
        "name": "PRANAV GUJARATHI",
        "email": "pranavdg1997@gmail.com",
        "phone": "(331) 248-7381",
        "location": "Austin, TX",
        "linkedin": "linkedin.com/in/pranav-gujarathi/",
        "education": [
            {
                "school": "Indiana University - Bloomington",
                "degree": "Master's, Data Science",
                "date": "August 2019 - May 2021"
            }
        ],
        "work_experiences": [
            {
                "company": "Cigna",
                "title": "Senior AI Engineer",
                "date": "September 2024 - Present",
                "bullet_count": 2
            },
            {
                "company": "Walmart",
                "title": "AI Engineer",
                "date": "October 2023 - August 2024",
                "bullet_count": 3
            },
            {
                "company": "Walmart",
                "title": "Data Scientist",
                "date": "January 2022 - October 2023",
                "bullet_count": 4
            },
            {
                "company": "ZS Associates",
                "title": "Data Science Associate",
                "date": "June 2018 - December 2021",
                "bullet_count": 3
            },
            {
                "company": "Indiana University - Bloomington",
                "title": "Research Engineer",
                "date": "January 2020 - May 2021",
                "bullet_count": 3
            }
        ],
        "total_work_experiences": 5,
        "total_bullets": 15,
        "has_projects_section": True,
        "has_skills_section": True
    }

def analyze_generated_data():
    """Analyze our generated resume data"""
    
    with open('test_pranav_resume.json', 'r') as f:
        generated_data = json.load(f)
    
    return {
        "name": generated_data['personalInfo']['name'],
        "email": generated_data['personalInfo']['email'],
        "phone": generated_data['personalInfo']['phone'],
        "location": generated_data['personalInfo']['location'],
        "linkedin": generated_data['personalInfo']['url'],
        "education": [
            {
                "school": edu['school'],
                "degree": edu['degree'],
                "date": edu['date']
            }
            for edu in generated_data['educations']
        ],
        "work_experiences": [
            {
                "company": exp['company'],
                "title": exp['jobTitle'],
                "date": exp['date'],
                "bullet_count": len(exp['descriptions'])
            }
            for exp in generated_data['workExperiences']
        ],
        "total_work_experiences": len(generated_data['workExperiences']),
        "total_bullets": sum(len(exp['descriptions']) for exp in generated_data['workExperiences']),
        "has_projects_section": len(generated_data['projects']) > 0,
        "has_skills_section": len(generated_data['skills']) > 0,
        "projects_count": len(generated_data['projects']),
        "skills_categories": len(generated_data['skills'])
    }

def compare_field(field_name: str, original: Any, generated: Any) -> Dict[str, Any]:
    """Compare a specific field between original and generated"""
    
    matches = original == generated
    return {
        "field": field_name,
        "matches": matches,
        "original": original,
        "generated": generated,
        "status": "✓ MATCH" if matches else "✗ DIFFER"
    }

def compare_work_experiences(original_exps: List[Dict], generated_exps: List[Dict]) -> Dict[str, Any]:
    """Compare work experience details"""
    
    comparison = {
        "total_count": compare_field("Total Work Experiences", len(original_exps), len(generated_exps)),
        "experiences": []
    }
    
    # Compare each work experience
    for i, (orig, gen) in enumerate(zip(original_exps, generated_exps)):
        exp_comparison = {
            "index": i + 1,
            "company": compare_field("Company", orig['company'], gen['company']),
            "title": compare_field("Title", orig['title'], gen['title']),
            "date": compare_field("Date", orig['date'], gen['date']),
            "bullet_count": compare_field("Bullet Count", orig['bullet_count'], gen['bullet_count'])
        }
        comparison["experiences"].append(exp_comparison)
    
    return comparison

def analyze_file_sizes():
    """Analyze the file sizes of different generated versions"""
    
    files_to_check = [
        ('attached_assets/PRANAV GUJARATHI - Resume_1755756003056.pdf', 'Original PDF'),
        ('pranav_generated_resume.pdf', 'Custom Generator'),
        ('pranav_openresume_generated.pdf', 'OpenResume Integration'),
        ('openresume_integrated.pdf', 'Latest OpenResume')
    ]
    
    sizes = {}
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            sizes[description] = {
                "file": file_path,
                "size_bytes": size,
                "size_kb": round(size / 1024, 1)
            }
    
    return sizes

def main():
    """Run comprehensive resume comparison"""
    
    print("📄 Resume Comparison Analysis")
    print("=" * 60)
    print("Comparing original uploaded resume with generated versions")
    print("=" * 60)
    
    # Analyze both versions
    original = analyze_original_resume()
    generated = analyze_generated_data()
    
    print("\n=== PERSONAL INFORMATION ===")
    personal_comparisons = [
        compare_field("Name", original['name'], generated['name']),
        compare_field("Email", original['email'], generated['email']),
        compare_field("Phone", original['phone'], generated['phone']),
        compare_field("Location", original['location'], generated['location'])
    ]
    
    for comp in personal_comparisons:
        print(f"{comp['status']} {comp['field']}")
        if not comp['matches']:
            print(f"  Original: {comp['original']}")
            print(f"  Generated: {comp['generated']}")
    
    print("\n=== EDUCATION ===")
    if original['education'] and generated['education']:
        orig_edu = original['education'][0]
        gen_edu = generated['education'][0]
        
        edu_comparisons = [
            compare_field("School", orig_edu['school'], gen_edu['school']),
            compare_field("Degree", orig_edu['degree'], gen_edu['degree']),
            compare_field("Date", orig_edu['date'], gen_edu['date'])
        ]
        
        for comp in edu_comparisons:
            print(f"{comp['status']} {comp['field']}")
            if not comp['matches']:
                print(f"  Original: {comp['original']}")
                print(f"  Generated: {comp['generated']}")
    
    print("\n=== WORK EXPERIENCE ===")
    work_comparison = compare_work_experiences(original['work_experiences'], generated['work_experiences'])
    
    print(f"{work_comparison['total_count']['status']} Total Work Experiences: {original['total_work_experiences']} vs {generated['total_work_experiences']}")
    
    total_bullet_comparison = compare_field("Total Bullets", original['total_bullets'], generated['total_bullets'])
    print(f"{total_bullet_comparison['status']} Total Achievement Bullets: {original['total_bullets']} vs {generated['total_bullets']}")
    
    # Check each work experience
    for exp_comp in work_comparison['experiences']:
        exp_num = exp_comp['index']
        print(f"\nWork Experience #{exp_num}:")
        print(f"  {exp_comp['company']['status']} Company: {exp_comp['company']['original']} vs {exp_comp['company']['generated']}")
        print(f"  {exp_comp['title']['status']} Title: {exp_comp['title']['original']} vs {exp_comp['title']['generated']}")
        print(f"  {exp_comp['date']['status']} Date: {exp_comp['date']['original']} vs {exp_comp['date']['generated']}")
        print(f"  {exp_comp['bullet_count']['status']} Bullets: {exp_comp['bullet_count']['original']} vs {exp_comp['bullet_count']['generated']}")
    
    print("\n=== ADDITIONAL SECTIONS ===")
    projects_comp = compare_field("Has Projects", original['has_projects_section'], generated['has_projects_section'])
    skills_comp = compare_field("Has Skills", original['has_skills_section'], generated['has_skills_section'])
    
    print(f"{projects_comp['status']} Projects Section")
    print(f"{skills_comp['status']} Skills Section")
    print(f"✓ Generated Projects Count: {generated['projects_count']}")
    print(f"✓ Generated Skills Categories: {generated['skills_categories']}")
    
    print("\n=== FILE SIZE COMPARISON ===")
    sizes = analyze_file_sizes()
    
    for description, info in sizes.items():
        print(f"{description}: {info['size_kb']} KB ({info['size_bytes']:,} bytes)")
    
    # Calculate accuracy score
    print("\n=== ACCURACY SUMMARY ===")
    
    total_checks = 0
    passed_checks = 0
    
    # Count personal info checks
    for comp in personal_comparisons:
        total_checks += 1
        if comp['matches']:
            passed_checks += 1
    
    # Count education checks
    for comp in edu_comparisons:
        total_checks += 1
        if comp['matches']:
            passed_checks += 1
    
    # Count work experience structure checks
    total_checks += 2  # total count and total bullets
    if work_comparison['total_count']['matches']:
        passed_checks += 1
    if total_bullet_comparison['matches']:
        passed_checks += 1
    
    # Count section checks
    total_checks += 2
    if projects_comp['matches']:
        passed_checks += 1
    if skills_comp['matches']:
        passed_checks += 1
    
    accuracy = (passed_checks / total_checks) * 100
    print(f"\nOverall Accuracy: {passed_checks}/{total_checks} checks passed ({accuracy:.1f}%)")
    
    if accuracy >= 90:
        print("🎉 EXCELLENT: Generated resume matches original very closely")
    elif accuracy >= 80:
        print("✅ GOOD: Generated resume matches original well with minor differences")
    elif accuracy >= 70:
        print("⚠️ ACCEPTABLE: Generated resume has some differences from original")
    else:
        print("❌ NEEDS IMPROVEMENT: Generated resume differs significantly from original")
    
    print(f"\n📊 File Size Analysis:")
    if 'Original PDF' in sizes and 'OpenResume Integration' in sizes:
        original_size = sizes['Original PDF']['size_bytes']
        generated_size = sizes['OpenResume Integration']['size_bytes']
        ratio = generated_size / original_size
        print(f"Generated/Original size ratio: {ratio:.2f}")
        
        if 0.2 <= ratio <= 0.5:
            print("✅ Size ratio indicates efficient, well-formatted PDF generation")
        elif ratio < 0.2:
            print("⚠️ Generated PDF may be missing content or formatting")
        else:
            print("⚠️ Generated PDF may have extra content or different formatting")

if __name__ == "__main__":
    main()