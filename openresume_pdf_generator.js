#!/usr/bin/env node

/**
 * Standalone OpenResume PDF Generator
 * Uses React PDF to generate ATS-friendly resume PDFs.
 */

const fs = require('fs').promises;
const React = require('react');
const { Document, Page, Text, View, Link, StyleSheet } = require('@react-pdf/renderer');
const { renderToBuffer } = require('@react-pdf/renderer');

const BULLET = '\u2022';
const BLACK = '#000000';

const DEFAULT_SETTINGS = {
  fontFamily: 'Times-Roman',
  fontSize: 11,
  documentSize: 'A4',
  themeColor: BLACK,
  formToHeading: {
    workExperiences: 'PROFESSIONAL EXPERIENCE',
    educations: 'EDUCATION',
    projects: 'PROJECTS',
    skills: 'SKILLS',
    custom: 'ADDITIONAL',
  },
  formToShow: {
    workExperiences: true,
    educations: true,
    projects: true,
    skills: true,
    custom: false,
  },
  formsOrder: ['workExperiences', 'educations', 'projects', 'skills', 'custom'],
  showBulletPoints: {
    workExperiences: true,
    educations: true,
    projects: true,
    skills: true,
    custom: true,
  },
};

const normalizeHeading = (heading, fallback) => {
  if (!heading || heading === 'WORK EXPERIENCE') {
    return fallback;
  }
  return heading;
};

const mergeSettings = (inputSettings = {}) => {
  const formToHeading = {
    ...DEFAULT_SETTINGS.formToHeading,
    ...(inputSettings.formToHeading || {}),
  };

  formToHeading.workExperiences = normalizeHeading(
    formToHeading.workExperiences,
    DEFAULT_SETTINGS.formToHeading.workExperiences
  );

  return {
    ...DEFAULT_SETTINGS,
    ...inputSettings,
    fontFamily: 'Times-Roman',
    documentSize: 'A4',
    themeColor: BLACK,
    formToHeading,
    formToShow: {
      ...DEFAULT_SETTINGS.formToShow,
      ...(inputSettings.formToShow || {}),
    },
    showBulletPoints: {
      ...DEFAULT_SETTINGS.showBulletPoints,
      ...(inputSettings.showBulletPoints || {}),
    },
  };
};

const buildOpenResumeData = (resumeData) => {
  const personalInfo = resumeData.personalInfo || resumeData.profile || {};

  return {
    profile: {
      name: personalInfo.name || '',
      email: personalInfo.email || '',
      phone: personalInfo.phone || '',
      url: personalInfo.url || '',
      github: personalInfo.github || '',
      linkedin: personalInfo.linkedin || '',
      summary: personalInfo.summary || '',
      location: personalInfo.location || '',
    },
    workExperiences: (resumeData.workExperiences || []).map((exp) => ({
      company: exp.company || '',
      jobTitle: exp.jobTitle || '',
      date: exp.date || '',
      location: exp.location || '',
      descriptions: exp.descriptions || [],
    })),
    educations: (resumeData.educations || []).map((edu) => ({
      school: edu.school || '',
      degree: edu.degree || '',
      date: edu.date || '',
      gpa: edu.gpa || '',
      descriptions: edu.descriptions || [],
    })),
    projects: (resumeData.projects || []).map((proj) => ({
      name: proj.name || proj.project || '',
      company: proj.company || '',
      date: proj.date || '',
      descriptions: proj.descriptions || [],
    })),
    skills: Array.isArray(resumeData.skills)
      ? resumeData.skills.map((skillGroup) => ({
          category: skillGroup.category || '',
          skills: skillGroup.skills || [],
        }))
      : [],
    custom: {
      descriptions: resumeData.custom?.descriptions || [],
    },
    publications: (resumeData.publications || []).map((pub) => ({
      name: pub.name || '',
      date: pub.date || '',
      url: pub.url || '',
      descriptions: pub.descriptions || [],
    })),
    certifications: (resumeData.certifications || []).map((cert) => ({
      name: cert.name || '',
      date: cert.date || '',
      org: cert.org || '',
      url: cert.url || '',
      descriptions: cert.descriptions || [],
    })),
    settings: mergeSettings(resumeData.settings || {}),
  };
};

const createResumeStyles = (settings) => {
  const requestedFontSize = Number(settings.fontSize) || 11;
  const bodyFontSize = Math.max(8, requestedFontSize - 2);
  const smallFontSize = Math.max(7.5, bodyFontSize - 0.5);
  const nameFontSize = Math.max(18, requestedFontSize + 9);
  const sectionFontSize = bodyFontSize + 2;

  return {
    page: {
      fontFamily: 'Times-Roman',
      fontSize: bodyFontSize,
      color: BLACK,
      paddingTop: 40,
      paddingBottom: 40,
      paddingLeft: 40,
      paddingRight: 40,
      backgroundColor: '#ffffff',
      lineHeight: 1.2,
    },
    header: {
      marginBottom: 8,
      alignItems: 'center',
    },
    name: {
      fontFamily: 'Times-Bold',
      fontSize: nameFontSize,
      color: BLACK,
      marginBottom: 12,
      letterSpacing: 0,
      textAlign: 'center',
    },
    contact: {
      fontSize: smallFontSize,
      color: BLACK,
      marginBottom: 2,
      textAlign: 'center',
    },
    contactLink: {
      fontSize: smallFontSize,
      color: BLACK,
      textDecoration: 'underline',
    },
    contactLine: {
      flexDirection: 'row',
      justifyContent: 'center',
      flexWrap: 'wrap',
      marginBottom: 2,
      alignItems: 'center',
    },
    summary: {
      fontSize: bodyFontSize,
      lineHeight: 1.2,
      textAlign: 'justify',
      color: BLACK,
    },
    section: {
      marginBottom: 10,
    },
    sectionTitle: {
      fontFamily: 'Times-Bold',
      fontSize: sectionFontSize,
      color: BLACK,
      marginBottom: 6,
      marginTop: 2,
      letterSpacing: 0,
      borderBottomWidth: 1,
      borderBottomColor: BLACK,
      paddingBottom: 2,
    },
    experienceItem: {
      marginBottom: 9,
    },
    educationItem: {
      marginBottom: 7,
    },
    metadataRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      marginBottom: 1,
    },
    metadataLeftBold: {
      width: '68%',
      fontFamily: 'Times-Bold',
      fontSize: bodyFontSize,
      color: BLACK,
    },
    metadataRightBold: {
      width: '32%',
      fontFamily: 'Times-Bold',
      fontSize: bodyFontSize,
      color: BLACK,
      textAlign: 'right',
    },
    metadataLeftItalic: {
      width: '68%',
      fontFamily: 'Times-Italic',
      fontSize: bodyFontSize,
      color: BLACK,
    },
    metadataRightItalic: {
      width: '32%',
      fontFamily: 'Times-Italic',
      fontSize: bodyFontSize,
      color: BLACK,
      textAlign: 'right',
    },
    bullet: {
      fontSize: smallFontSize,
      lineHeight: 1.18,
      marginBottom: 2,
      marginLeft: 18,
      color: BLACK,
    },
    bulletRow: {
      flexDirection: 'row',
      marginLeft: 18,
      marginBottom: 2,
    },
    bulletMarker: {
      width: 10,
      fontSize: smallFontSize,
      color: BLACK,
    },
    bulletText: {
      flex: 1,
      fontSize: smallFontSize,
      lineHeight: 1.18,
      color: BLACK,
    },
    skillsText: {
      fontSize: smallFontSize,
      lineHeight: 1.18,
      marginBottom: 2,
      color: BLACK,
    },
    publicationItem: {
      marginBottom: 6,
    },
    publicationTitle: {
      fontFamily: 'Times-Bold',
      fontSize: bodyFontSize,
      color: BLACK,
      lineHeight: 1.18,
      marginBottom: 1,
    },
    publicationLink: {
      fontFamily: 'Times-Bold',
      fontSize: bodyFontSize,
      color: BLACK,
      textDecoration: 'underline',
      lineHeight: 1.18,
      marginBottom: 1,
    },
    publicationMeta: {
      fontFamily: 'Times-Italic',
      fontSize: smallFontSize,
      color: BLACK,
      lineHeight: 1.15,
      marginBottom: 2,
    },
  };
};

const buildContactItems = (profile) => {
  const items = [];
  if (profile.email) {
    items.push({ text: profile.email, href: `mailto:${profile.email}` });
  }
  if (profile.phone) {
    items.push({ text: profile.phone });
  }
  if (profile.location) {
    items.push({ text: profile.location });
  }
  if (profile.url) {
    items.push({ text: profile.url, href: profile.url });
  }
  if (profile.github) {
    items.push({ text: profile.github, href: profile.github });
  }
  if (profile.linkedin) {
    items.push({ text: profile.linkedin, href: profile.linkedin });
  }
  return items;
};

const splitContactItems = (items) => {
  if (items.length <= 5) {
    return [items];
  }
  return [items.slice(0, 5), items.slice(5)];
};

const contactLinesToText = (lines) => lines.map((line) => line.map((item) => item.text).join(' | '));

const getSectionHeadings = (resumeData) => {
  const headings = [];
  const formToHeading = resumeData.settings.formToHeading;

  if (resumeData.profile.summary) {
    headings.push('PROFESSIONAL SUMMARY');
  }
  if (resumeData.educations.length > 0) {
    headings.push(formToHeading.educations);
  }
  if (resumeData.workExperiences.length > 0) {
    headings.push(formToHeading.workExperiences);
  }
  if (resumeData.projects.length > 0) {
    headings.push(formToHeading.projects);
  }
  if (resumeData.skills.length > 0) {
    headings.push(formToHeading.skills);
  }
  if (resumeData.publications.length > 0) {
    headings.push('PUBLICATIONS / ACHIEVEMENTS');
  }
  if (resumeData.certifications.length > 0) {
    headings.push('CERTIFICATIONS');
  }
  if (resumeData.custom.descriptions.length > 0) {
    headings.push(formToHeading.custom);
  }

  return headings;
};

const buildResumeLayoutModel = (resumeData) => {
  const contactLineItems = splitContactItems(buildContactItems(resumeData.profile));

  return {
    pageSize: 'A4',
    styles: createResumeStyles(resumeData.settings),
    profile: {
      ...resumeData.profile,
      name: resumeData.profile.name.toUpperCase(),
      contactLineItems,
      contactLines: contactLinesToText(contactLineItems),
    },
    sectionHeadings: getSectionHeadings(resumeData),
    workExperienceItems: resumeData.workExperiences.map((exp) => ({
      ...exp,
      headerRows: [
        { left: exp.company, right: exp.date, emphasis: 'bold' },
        { left: exp.jobTitle, right: exp.location || '', emphasis: 'italic' },
      ],
    })),
    educationItems: resumeData.educations.map((edu) => {
      const degree = edu.gpa ? `${edu.degree} | GPA: ${edu.gpa}` : edu.degree;
      return {
        ...edu,
        degree,
        headerRows: [
          { left: edu.school, right: edu.date, emphasis: 'bold' },
          { left: degree, right: '', emphasis: 'italic' },
        ],
      };
    }),
  };
};

const renderContactLine = (line, styles, lineIndex) =>
  React.createElement(
    View,
    { key: `contact-${lineIndex}`, style: styles.contactLine },
    ...line.flatMap((item, itemIndex) => {
      const nodes = [];
      if (itemIndex > 0) {
        nodes.push(React.createElement(Text, { key: `sep-${itemIndex}`, style: styles.contact }, ' | '));
      }
      if (item.href) {
        nodes.push(
          React.createElement(Link, { key: `item-${itemIndex}`, style: styles.contactLink, src: item.href }, item.text)
        );
      } else {
        nodes.push(React.createElement(Text, { key: `item-${itemIndex}`, style: styles.contact }, item.text));
      }
      return nodes;
    })
  );

const renderMetadataRows = (rows, styles) =>
  rows.map((row, index) =>
    React.createElement(
      View,
      { key: `row-${index}`, style: styles.metadataRow },
      React.createElement(Text, { style: row.emphasis === 'bold' ? styles.metadataLeftBold : styles.metadataLeftItalic }, row.left),
      React.createElement(Text, { style: row.emphasis === 'bold' ? styles.metadataRightBold : styles.metadataRightItalic }, row.right)
    )
  );

const renderBullet = (desc, index, styles) =>
  React.createElement(
    View,
    { key: index, style: styles.bulletRow },
    React.createElement(Text, { style: styles.bulletMarker }, BULLET),
    React.createElement(Text, { style: styles.bulletText }, desc)
  );

const renderSectionTitle = (title, styles) => React.createElement(Text, { style: styles.sectionTitle }, title);

// Create a standalone PDF generator that mimics OpenResume's structure
const generateOpenResumePDF = async (resumeData) => {
  const openResumeData = buildOpenResumeData(resumeData);
  const layout = buildResumeLayoutModel(openResumeData);
  const styles = StyleSheet.create(layout.styles);

  const ResumeDocument = () =>
    React.createElement(
      Document,
      { title: `${openResumeData.profile.name} Resume` },
      React.createElement(
        Page,
        { size: layout.pageSize, style: styles.page },
        React.createElement(
          View,
          { style: styles.header },
          React.createElement(Text, { style: styles.name }, layout.profile.name),
          ...layout.profile.contactLineItems.map((line, index) => renderContactLine(line, styles, index))
        ),

        openResumeData.profile.summary &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle('PROFESSIONAL SUMMARY', styles),
            React.createElement(Text, { style: styles.summary }, openResumeData.profile.summary)
          ),

        openResumeData.educations.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle(openResumeData.settings.formToHeading.educations, styles),
            ...layout.educationItems.map((edu, index) =>
              React.createElement(
                View,
                { key: index, style: styles.educationItem },
                ...renderMetadataRows(edu.headerRows, styles),
                ...edu.descriptions.map((desc, descIndex) => renderBullet(desc, descIndex, styles))
              )
            )
          ),

        openResumeData.workExperiences.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle(openResumeData.settings.formToHeading.workExperiences, styles),
            ...layout.workExperienceItems.map((exp, index) =>
              React.createElement(
                View,
                { key: index, style: styles.experienceItem },
                ...renderMetadataRows(exp.headerRows, styles),
                ...exp.descriptions.map((desc, descIndex) => renderBullet(desc, descIndex, styles))
              )
            )
          ),

        openResumeData.projects.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle(openResumeData.settings.formToHeading.projects, styles),
            ...openResumeData.projects.map((proj, index) =>
              React.createElement(
                View,
                { key: index, style: styles.experienceItem },
                ...renderMetadataRows(
                  [
                    { left: proj.name, right: proj.date, emphasis: 'bold' },
                    { left: proj.company || '', right: '', emphasis: 'italic' },
                  ],
                  styles
                ),
                ...proj.descriptions.map((desc, descIndex) => renderBullet(desc, descIndex, styles))
              )
            )
          ),

        openResumeData.skills.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle(openResumeData.settings.formToHeading.skills, styles),
            ...openResumeData.skills.map((skillGroup, index) =>
              React.createElement(
                Text,
                { key: index, style: styles.skillsText },
                React.createElement(Text, { style: { fontFamily: 'Times-Bold' } }, `${skillGroup.category}: `),
                skillGroup.skills.join(', ')
              )
            )
          ),

        openResumeData.publications.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle('PUBLICATIONS / ACHIEVEMENTS', styles),
            ...openResumeData.publications.map((pub, index) =>
              React.createElement(
                View,
                { key: index, style: styles.publicationItem },
                pub.url
                  ? React.createElement(Link, { style: styles.publicationLink, src: pub.url }, pub.name)
                  : React.createElement(Text, { style: styles.publicationTitle }, pub.name),
                pub.date && React.createElement(Text, { style: styles.publicationMeta }, pub.date),
                ...pub.descriptions.map((desc, descIndex) => renderBullet(desc, descIndex, styles))
              )
            )
          ),

        openResumeData.certifications.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle('CERTIFICATIONS', styles),
            ...openResumeData.certifications.map((cert, index) =>
              React.createElement(
                View,
                { key: index, style: styles.experienceItem },
                ...renderMetadataRows(
                  [
                    { left: cert.name, right: cert.date, emphasis: 'bold' },
                    { left: cert.org || '', right: '', emphasis: 'italic' },
                  ],
                  styles
                ),
                ...cert.descriptions.map((desc, descIndex) => renderBullet(desc, descIndex, styles))
              )
            )
          ),

        openResumeData.custom.descriptions.length > 0 &&
          React.createElement(
            View,
            { style: styles.section },
            renderSectionTitle(openResumeData.settings.formToHeading.custom, styles),
            ...openResumeData.custom.descriptions.map((desc, descIndex) => renderBullet(desc, descIndex, styles))
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

module.exports = {
  buildOpenResumeData,
  buildResumeLayoutModel,
  generateOpenResumePDF,
};
