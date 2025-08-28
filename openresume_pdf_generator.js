#!/usr/bin/env node

/**
 * Standalone OpenResume PDF Generator
 * Uses the actual OpenResume components to generate professional PDFs
 */

const fs = require('fs').promises;
const path = require('path');
const React = require('react');  
const { Document, Page, Text, View, Link, StyleSheet, pdf } = require('@react-pdf/renderer');
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

  // Components already imported above

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
      paddingBottom: 20,
      marginBottom: 25,
      alignItems: 'center'
    },
    name: {
      fontSize: 24,
      fontWeight: 'bold',
      color: '#1f2937',
      marginBottom: 15,
      letterSpacing: 1,
      textAlign: 'center'
    },
    contact: {
      fontSize: 11,
      color: '#4b5563',
      marginBottom: 4,
      textAlign: 'center'
    },
    contactLine: {
      flexDirection: 'row',
      justifyContent: 'center',
      flexWrap: 'wrap',
      marginBottom: 8
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
        // Header with name and contact info (with hyperlinks and better spacing)
        React.createElement(View, { style: styles.header },
          React.createElement(Text, { style: styles.name }, openResumeData.profile.name),
          
          // First line: Email and Phone
          React.createElement(View, { style: styles.contactLine },
            openResumeData.profile.email && React.createElement(Link, { 
              style: { ...styles.contact, color: '#2563eb', textDecoration: 'underline' },
              src: `mailto:${openResumeData.profile.email}`
            }, openResumeData.profile.email),
            
            openResumeData.profile.phone && React.createElement(Text, null,
              React.createElement(Text, { style: { ...styles.contact, marginLeft: 8, marginRight: 8 } }, ' • '),
              React.createElement(Text, { style: styles.contact }, openResumeData.profile.phone)
            )
          ),
          
          // Second line: Location and URLs
          React.createElement(View, { style: styles.contactLine },
            openResumeData.profile.location && React.createElement(Text, { style: styles.contact }, openResumeData.profile.location),
            
            openResumeData.profile.url && React.createElement(Text, null,
              React.createElement(Text, { style: { ...styles.contact, marginLeft: 8, marginRight: 8 } }, ' • '),
              React.createElement(Link, {
                style: { ...styles.contact, color: '#2563eb', textDecoration: 'underline' },
                src: openResumeData.profile.url
              }, openResumeData.profile.url)
            ),
            
            openResumeData.profile.github && React.createElement(Text, null,
              React.createElement(Text, { style: { ...styles.contact, marginLeft: 8, marginRight: 8 } }, ' • '),
              React.createElement(Link, {
                style: { ...styles.contact, color: '#2563eb', textDecoration: 'underline' },
                src: openResumeData.profile.github
              }, 'GitHub')
            ),
            
            openResumeData.profile.linkedin && React.createElement(Text, null,
              React.createElement(Text, { style: { ...styles.contact, marginLeft: 8, marginRight: 8 } }, ' • '),
              React.createElement(Link, {
                style: { ...styles.contact, color: '#2563eb', textDecoration: 'underline' },
                src: openResumeData.profile.linkedin
              }, 'LinkedIn')
            )
          ),
          
          openResumeData.profile.summary && 
            React.createElement(Text, { style: { ...styles.summary, marginTop: 15 } }, openResumeData.profile.summary)
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

        // Projects Section (with structured format like work experience)
        openResumeData.projects && openResumeData.projects.length > 0 &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'PROJECTS'),
            ...openResumeData.projects.map((proj, index) =>
              React.createElement(View, { key: index, style: styles.experienceItem },
                React.createElement(View, { style: styles.experienceHeader },
                  React.createElement(Text, { style: styles.company }, 
                    proj.company ? `${proj.name} - ${proj.company}` : proj.name),
                  React.createElement(Text, { style: styles.date }, proj.date)
                ),
                ...proj.descriptions.map((desc, descIndex) =>
                  React.createElement(Text, { key: descIndex, style: styles.bullet }, `• ${desc}`)
                )
              )
            )
          ),

        // Skills Section (with bold categories)
        ((openResumeData.skills && openResumeData.skills.length > 0) || 
         (openResumeData.skills && openResumeData.skills.descriptions && openResumeData.skills.descriptions.length > 0)) &&
          React.createElement(View, { style: styles.section },
            React.createElement(Text, { style: styles.sectionTitle }, 'SKILLS'),
            // Handle structured skills format
            ...(openResumeData.skills && Array.isArray(openResumeData.skills) ? 
              openResumeData.skills.map((skillGroup, index) =>
                React.createElement(Text, { key: index, style: styles.skillsText },
                  React.createElement(Text, { style: { fontWeight: 'bold' } }, skillGroup.category + ': '),
                  skillGroup.skills.join(', ')
                )
              ) :
              // Handle legacy descriptions format with bold categories  
              (openResumeData.skills.descriptions || []).map((skill, index) => {
                const colonIndex = skill.indexOf(': ');
                if (colonIndex > 0) {
                  const category = skill.substring(0, colonIndex + 1);
                  const skillList = skill.substring(colonIndex + 2);
                  return React.createElement(Text, { key: index, style: styles.skillsText },
                    React.createElement(Text, { style: { fontWeight: 'bold' } }, category),
                    ' ' + skillList
                  );
                }
                return React.createElement(Text, { key: index, style: styles.skillsText }, skill);
              })
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