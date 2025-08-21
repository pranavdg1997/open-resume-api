#!/usr/bin/env python3
"""
Test script to validate the OpenResume API functionality
"""

import requests
import json
import os
from datetime import datetime

API_BASE_URL = "http://localhost:5000/api/v1"

def test_health_endpoint():
    """Test the health endpoint"""
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_resume_generation():
    """Test resume generation with sample data"""
    
    # Load test data
    with open('test_resume.json', 'r') as f:
        test_data = json.load(f)
    
    print(f"\nTesting resume generation for: {test_data['personalInfo']['name']}")
    
    # Make API request
    response = requests.post(
        f"{API_BASE_URL}/generate-resume",
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        # Save generated PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_resume_{timestamp}.pdf"
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        file_size = os.path.getsize(filename)
        print(f"Generated PDF: {filename} ({file_size} bytes)")
        
        # Basic validation
        if file_size > 1000:  # PDF should be at least 1KB
            print("✓ PDF generation successful")
            return True
        else:
            print("✗ Generated PDF seems too small")
            return False
    else:
        print(f"✗ Error: {response.text}")
        return False

def test_templates_endpoint():
    """Test the templates endpoint"""
    response = requests.get(f"{API_BASE_URL}/templates")
    print(f"\nTemplates endpoint: {response.status_code}")
    if response.status_code == 200:
        templates = response.json()
        print(f"Available templates: {len(templates.get('templates', []))}")
        return True
    return False

def main():
    """Run all tests"""
    print("=== OpenResume API Validation ===")
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Resume Generation", test_resume_generation),
        ("Templates Endpoint", test_templates_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n=== Test Results ===")
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()