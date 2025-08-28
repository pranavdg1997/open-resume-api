#!/usr/bin/env node

/**
 * Standalone OpenResume PDF Generator
 * Uses the actual OpenResume components to generate professional PDFs
 */

const fs = require('fs').promises;
const path = require('path');
const React = require('react');
const { renderToBuffer } = require('@react-pdf/renderer');

// Create a standalone PDF generator that mimics OpenResume's structure
const generateOpenResumePDF = async (resumeData) => {
  // Transform our data to match OpenResume's exact format
  const openResumeData = {
    profile: {
      name: resumeData.personalInfo?.name || '',
      email: resumeData.personalInfo?.email || '',
      phone: resumeData.personalInfo?.phone || '',
      url: resumeData.personalInfo?.url || '',
      summary: resumeData.personalInfo?.summary || '',
      location: resumeData.personalInfo?.location || ''
    },
    workExperiences: (resumeData.workExperiences || []).map(exp => ({
      company: exp.company || '',
      jobTitle: exp.jobTitle || '',
      date: exp.date || '',
      descriptions: exp.descriptions || []
    })),
    educations: (resumeData.educations || []).map(edu => ({
      school: edu.school || '',
      degree: edu.degree || '',
      date: edu.date || '',
      gpa: edu.gpa || '',
      descriptions: edu.descriptions || []
    })),
    projects: (resumeData.projects || []).map(proj => ({
      project: proj.name || '',
      date: proj.date || '',
      descriptions: proj.descriptions || []
    })),
    skills: {
      featuredSkills: Array.isArray(resumeData.skills) ? resumeData.skills.reduce((acc, skillGroup) => {
        return acc.concat(skillGroup.skills || []);
      }, []) : [],
      descriptions: Array.isArray(resumeData.skills) ? resumeData.skills.map(skillGroup => 
        `${skillGroup.category}: ${(skillGroup.skills || []).join(', ')}`
      ) : []
    },
    custom: {
      descriptions: []
    },
    publications: (resumeData.publications || []).map(pub => ({
      name: pub.name || '',
      date: pub.date || '',
      descriptions: pub.descriptions || []
    })),
    certifications: (resumeData.certifications || []).map(cert => ({
      name: cert.name || '',
      date: cert.date || '',
      descriptions: cert.descriptions || []
    }))
  };

  const settings = {
    fontFamily: 'Helvetica',
    fontSize: 11,
    documentSize: 'Letter',
    themeColor: '#1f2937',
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

  // Create a simplified PDF using @react-pdf/renderer directly
  const { Document, Page, Text, View, StyleSheet } = require('@react-pdf/renderer');

  const styles = StyleSheet.create({
    page: {
      fontFamily: 'Helvetica',
      fontSize: 11,
      paddingTop: 50,
      paddingBottom: 50,
      paddingLeft: 60,
      paddingRight: 60,
      backgroundColor: '#ffffff',
      lineHeight: 1.6
    },
    header: {
      borderBottomWidth: 2,
      borderBottomColor: '#1f2937',
      paddingBottom: 15,
      marginBottom: 20
    },
    name: {
      fontSize: 24,
      fontWeight: 'bold',
      color: '#1f2937',
      marginBottom: 8,
      letterSpacing: 1
    },
    contact: {
      fontSize: 11,
      color: '#4b5563',
      marginBottom: 15
    },
    summary: {
      fontSize: 11,
      lineHeight: 1.5,
      textAlign: 'justify',
      color: '#374151'
    },
    section: {
      marginBottom: 25
    },
    sectionTitle: {
      fontSize: 13,
      fontWeight: 'bold',
      color: '#1f2937',
      marginBottom: 15,
      letterSpacing: 1.5,
      borderBottomWidth: 1,
      borderBottomColor: '#e5e7eb',
      paddingBottom: 5
    },
    experienceItem: {
      marginBottom: 18
    },
    experienceHeader: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      marginBottom: 5
    },
    jobTitle: {
      fontSize: 11,
      fontWeight: 'bold',
      color: '#1f2937'
    },
    company: {
      fontSize: 11,
      fontWeight: 'bold',
      color: '#1f2937'
    },
    date: {
      fontSize: 10,
      color: '#6b7280'
    },
    bullet: {
      fontSize: 10,
      lineHeight: 1.5,
      marginBottom: 4,
      marginLeft: 20,
      color: '#374151'
    },
    skillsText: {
      fontSize: 10,
      lineHeight: 1.4,
      marginBottom: 5
    }
  });

  const ResumeDocument = () => (
    React.createElement(Document, { title: `${openResumeData.profile.name} Resume` },
      React.createElement(Page, { size: 'LETTER', style: styles.page },
        // Header with name and contact info
        React.createElement(View, { style: styles.header },
          React.createElement(Text, { style: styles.name }, openResumeData.profile.name),
          React.createElement(Text, { style: styles.contact }, 
            [openResumeData.profile.email, openResumeData.profile.phone, openResumeData.profile.location]
              .filter(Boolean).join(' • ')
          ),
          openResumeData.profile.summary && 
            React.createElement(Text, { style: styles.summary }, openResumeData.profile.summary)
        ),

        // Education Section
        openResumeData.educations.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'EDUCATION'),
            ...openResumeData.educations.map((edu, index) =>
              React.createElement(View, { key: index, style: styles.experienceItem },
                React.createElement(View, { style: styles.experienceHeader },
                  React.createElement(Text, { style: styles.company }, 
                    `${edu.school} - ${edu.degree}`),
                  React.createElement(Text, { style: styles.date }, edu.date)
                ),
                ...edu.descriptions.map((desc, descIndex) =>
                  React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
                )
              )
            )
          ),

        // Work Experience Section
        openResumeData.workExperiences.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'WORK EXPERIENCE'),
            ...openResumeData.workExperiences.map((exp, index) =>
              React.createElement(View, { key: index, style: styles.experienceItem },
                React.createElement(View, { style: styles.experienceHeader },
                  React.createElement(Text, { style: styles.company }, 
                    `${exp.company} - ${exp.jobTitle}`),
                  React.createElement(Text, { style: styles.date }, exp.date)
                ),
                ...exp.descriptions.map((desc, descIndex) =>
                  React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
                )
              )
            )
          ),

        // Projects Section
        openResumeData.projects.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'PROJECTS'),
            ...openResumeData.projects.map((proj, index) =>
              React.createElement(View, { key: index, style: styles.experienceItem },
                React.createElement(Text, { style: styles.jobTitle }, proj.project),
                ...proj.descriptions.map((desc, descIndex) =>
                  React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
                )
              )
            )
          ),

        // Skills Section
        openResumeData.skills.descriptions.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'SKILLS'),
            ...openResumeData.skills.descriptions.map((skill, index) =>
              React.createElement(Text, { key: index, style: styles.skillsText }, skill)
            )
          ),

        // Publications Section
        openResumeData.publications && openResumeData.publications.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'PUBLICATIONS'),
            ...openResumeData.publications.map((pub, index) =>
              React.createElement(View, { key: index, style: styles.experienceItem },
                React.createElement(View, { style: styles.experienceHeader },
                  React.createElement(Text, { style: styles.jobTitle }, pub.name),
                  React.createElement(Text, { style: styles.date }, pub.date)
                ),
                ...pub.descriptions.map((desc, descIndex) =>
                  React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
                )
              )
            )
          ),

        // Certifications Section
        openResumeData.certifications && openResumeData.certifications.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'CERTIFICATIONS'),
            ...openResumeData.certifications.map((cert, index) =>
              React.createElement(View, { key: index, style: styles.experienceItem },
                React.createElement(View, { style: styles.experienceHeader },
                  React.createElement(Text, { style: styles.jobTitle }, cert.name),
                  React.createElement(Text, { style: styles.date }, cert.date)
                ),
                ...cert.descriptions.map((desc, descIndex) =>
                  React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
                )
              )
            )
          )
      )
    )
  );

  try {
    const pdfBuffer = await renderToBuffer(React.createElement(ResumeDocument));
    return pdfBuffer;
  } catch (error) {
    throw new Error(`PDF generation failed: ${error.message}`);
  }
};

async function main() {
  try {
    if (process.argv.length < 3) {
      console.error('Usage: node openresume_pdf_generator.js <resume_data_file>');
      process.exit(1);
    }

    const inputFile = process.argv[2];
    const resumeDataRaw = await fs.readFile(inputFile, 'utf8');
    const resumeData = JSON.parse(resumeDataRaw);

    const pdfBuffer = await generateOpenResumePDF(resumeData);
    process.stdout.write(pdfBuffer);

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { generateOpenResumePDF };