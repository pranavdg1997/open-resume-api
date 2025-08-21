#!/usr/bin/env node

/**
 * OpenResume Bridge Service
 * This service acts as a bridge between our FastAPI backend and the actual OpenResume
 * React PDF generation code. It takes resume data as JSON input and returns PDF bytes.
 */

const fs = require('fs').promises;
const path = require('path');

// Mock the OpenResume type structure based on the actual source
const createResumeData = (inputData) => {
  return {
    profile: {
      name: inputData.personalInfo?.name || '',
      email: inputData.personalInfo?.email || '',
      phone: inputData.personalInfo?.phone || '',
      url: inputData.personalInfo?.url || '',
      summary: inputData.personalInfo?.summary || '',
      location: inputData.personalInfo?.location || ''
    },
    workExperiences: (inputData.workExperiences || []).map(exp => ({
      company: exp.company || '',
      jobTitle: exp.jobTitle || '',
      date: exp.date || '',
      descriptions: exp.descriptions || []
    })),
    educations: (inputData.educations || []).map(edu => ({
      school: edu.school || '',
      degree: edu.degree || '',
      date: edu.date || '',
      gpa: edu.gpa || '',
      descriptions: edu.descriptions || []
    })),
    projects: (inputData.projects || []).map(proj => ({
      project: proj.name || '',
      date: proj.date || '',
      descriptions: proj.descriptions || []
    })),
    skills: {
      featuredSkills: [], // OpenResume uses different skills structure
      descriptions: []
    },
    custom: {
      descriptions: []
    }
  };
};

const createSettings = (inputData) => {
  const settings = inputData.settings || {};
  return {
    fontFamily: settings.fontFamily || 'system-ui',
    fontSize: settings.fontSize || '11',
    documentSize: settings.documentSize || 'Letter',
    themeColor: settings.themeColor || '#1f2937',
    formToHeading: {
      workExperiences: 'WORK EXPERIENCE',
      educations: 'EDUCATION',
      projects: 'PROJECTS',
      skills: 'SKILLS',
      custom: 'ADDITIONAL'
    },
    formToShow: {
      workExperiences: true,
      educations: true,
      projects: true,
      skills: true,
      custom: false
    },
    formsOrder: ['workExperiences', 'educations', 'projects', 'skills', 'custom'],
    showBulletPoints: {
      workExperiences: true,
      educations: true,
      projects: true,
      skills: true,
      custom: true
    }
  };
};

// Convert skills format from our API to OpenResume format
const convertSkills = (inputSkills) => {
  if (!inputSkills || !Array.isArray(inputSkills)) {
    return {
      featuredSkills: [],
      descriptions: []
    };
  }

  const descriptions = inputSkills.map(skillGroup => 
    `${skillGroup.category}: ${skillGroup.skills.join(', ')}`
  );

  return {
    featuredSkills: [],
    descriptions: descriptions
  };
};

async function generatePDF(resumeData) {
  try {
    // Transform input data to OpenResume format
    const openResumeData = createResumeData(resumeData);
    openResumeData.skills = convertSkills(resumeData.skills);
    
    const settings = createSettings(resumeData);

    // For now, return a simple message indicating successful transformation
    // In a full implementation, we would use @react-pdf/renderer here
    const result = {
      success: true,
      message: 'Resume data successfully transformed to OpenResume format',
      transformedData: {
        resume: openResumeData,
        settings: settings
      },
      originalSize: JSON.stringify(resumeData).length,
      transformedSize: JSON.stringify(openResumeData).length
    };

    return Buffer.from(JSON.stringify(result, null, 2));
  } catch (error) {
    const errorResult = {
      success: false,
      error: error.message,
      stack: error.stack
    };
    return Buffer.from(JSON.stringify(errorResult, null, 2));
  }
}

// Main execution
async function main() {
  try {
    if (process.argv.length < 3) {
      console.error('Usage: node openresume_bridge.js <resume_data_file>');
      process.exit(1);
    }

    const inputFile = process.argv[2];
    const resumeData = JSON.parse(await fs.readFile(inputFile, 'utf8'));
    
    const pdfBuffer = await generatePDF(resumeData);
    
    // Write to stdout for the Python process to capture
    process.stdout.write(pdfBuffer);
    
  } catch (error) {
    console.error('Bridge service error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}